#  ----------------------------------------------------------------------------
#  "THE BEER-WARE LICENSE" (Revision 42):
#  dkratzert@gmx.de> wrote this file.  As long as you retain
#  this notice you can do whatever you want with this stuff. If we meet some day,
#  and you think this stuff is worth it, you can buy me a beer in return.
#  Dr. Daniel Kratzert
#  ----------------------------------------------------------------------------
#
# Settings are stored as a single JSON file in the user's config directory.
# On first launch after the migration, existing QSettings data (Windows registry /
# INI file / macOS plist) is automatically imported into the JSON file.
# The JSON structure uses nested dicts where top-level keys correspond to the
# former QSettings groups (e.g. "MainWindow", "equipment", "property", ...).
# Ungrouped keys sit at the root level.

from __future__ import annotations

import json
import logging
import os
from collections.abc import Iterable
from dataclasses import asdict, fields
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Helpers: default config directory
# ---------------------------------------------------------------------------

def _default_config_dir() -> Path:
    """Return the platform-appropriate config directory for FinalCif."""
    if os.name == 'nt':
        base = Path(os.environ.get('APPDATA', Path.home()))
    elif os.name == 'posix' and 'darwin' in os.uname().sysname.lower():
        base = Path.home() / 'Library' / 'Application Support'
    else:
        base = Path(os.environ.get('XDG_CONFIG_HOME', Path.home() / '.config'))
    return base / 'DK' / 'FinalCif'


_SETTINGS_FILENAME = 'settings.json'


# ---------------------------------------------------------------------------
# JSON encoder / decoder for special types
# ---------------------------------------------------------------------------

def _custom_encoder(obj: Any) -> Any:
    """JSON encoder hook for Qt types, Author dataclass, and enums."""
    # Import lazily so the settings module doesn't hard-depend on Qt at import time
    # when only plain types are stored.
    from finalcif.equip_property.author_loop_templates import Author, AuthorType

    if hasattr(obj, '__class__') and obj.__class__.__name__ == 'QPoint':
        return {'__type__': 'QPoint', 'x': obj.x(), 'y': obj.y()}
    if hasattr(obj, '__class__') and obj.__class__.__name__ == 'QSize':
        return {'__type__': 'QSize', 'width': obj.width(), 'height': obj.height()}
    if isinstance(obj, Author):
        d = asdict(obj)
        d['__type__'] = 'Author'
        d['author_type'] = obj.author_type.value if isinstance(obj.author_type, AuthorType) else str(obj.author_type)
        return d
    if isinstance(obj, AuthorType):
        return obj.value
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def _custom_decoder(d: dict) -> Any:
    """JSON object-hook that reconstitutes tagged dicts back to rich types."""
    if '__type__' not in d:
        return d

    t = d['__type__']
    if t == 'QPoint':
        from qtpy.QtCore import QPoint
        return QPoint(d['x'], d['y'])
    if t == 'QSize':
        from qtpy.QtCore import QSize
        return QSize(d['width'], d['height'])
    if t == 'Author':
        from finalcif.equip_property.author_loop_templates import Author, AuthorType
        kw = {f.name: d.get(f.name) for f in fields(Author)}
        at = kw.get('author_type')
        if isinstance(at, str):
            kw['author_type'] = AuthorType(at)
        return Author(**kw)
    return d


# ---------------------------------------------------------------------------
# One-time QSettings -> JSON migration
# ---------------------------------------------------------------------------

def _migrate_qsettings_to_json(json_path: Path) -> dict:
    """Read all data from the existing QSettings store and return it as a dict.

    The resulting dict is written to *json_path* by the caller.  The original
    QSettings data is **not** deleted so that a downgrade is still possible.
    """
    from qtpy.QtCore import QSettings

    qs = QSettings('DK', 'FinalCif')
    data: dict[str, Any] = {'_migrated_from_qsettings': True}

    # Collect top-level keys (outside any group)
    for key in qs.allKeys():
        if '/' not in key:
            data[key] = _convert_qsettings_value(qs.value(key))

    # Collect grouped keys
    for group in qs.childGroups():
        qs.beginGroup(group)
        group_dict: dict[str, Any] = {}
        for key in qs.allKeys():
            group_dict[key] = _convert_qsettings_value(qs.value(key))
        qs.endGroup()
        data[group] = group_dict

    return data


def _convert_qsettings_value(value: Any) -> Any:  # noqa: PLR0911
    """Best-effort conversion of a QSettings value to a JSON-safe Python type."""
    from finalcif.equip_property.author_loop_templates import Author, AuthorType

    if value is None:
        return None

    # QPoint / QSize
    cls_name = type(value).__name__
    if cls_name == 'QPoint':
        return {'__type__': 'QPoint', 'x': value.x(), 'y': value.y()}
    if cls_name == 'QSize':
        return {'__type__': 'QSize', 'width': value.width(), 'height': value.height()}
    if isinstance(value, Author):
        return _custom_encoder(value)
    if isinstance(value, AuthorType):
        return value.value

    # Recurse into containers
    if isinstance(value, dict):
        return {str(k): _convert_qsettings_value(v) for k, v in value.items()}
    if isinstance(value, list | tuple):
        return [_convert_qsettings_value(v) for v in value]

    # Primitive types that JSON handles natively
    if isinstance(value, str | int | float | bool):
        return value

    # Fallback - store as string
    return str(value)


# ---------------------------------------------------------------------------
# Core JSON-backed settings class
# ---------------------------------------------------------------------------

class FinalCifSettings:
    """Application settings stored as a JSON file.

    Parameters
    ----------
    settings_path : Path | None
        Explicit path to the JSON file.  When *None* the platform default is
        used.  Pass an explicit path in tests for isolation.
    """

    def __init__(self, settings_path: Path | None = None):
        self.software_name = 'FinalCif'
        self.organization = 'DK'

        if settings_path is not None:
            self._path = settings_path
        else:
            self._path = _default_config_dir() / _SETTINGS_FILENAME

        self._data: dict[str, Any] = self._load_json()

        # If the JSON file was empty / missing, attempt a one-time migration
        if not self._data:
            try:
                self._data = _migrate_qsettings_to_json(self._path)
                if self._data:
                    self._flush()
                    logger.info("Migrated QSettings to %s", self._path)
            except Exception:
                logger.debug("No QSettings data to migrate (or Qt not available).", exc_info=True)
                self._data = {}

        # Cached property helpers (same semantics as before)
        self.property_keys_and_values = self.load_property_keys_and_values()
        self.property_keys = self.load_cif_keys_of_properties()

    # ------------------------------------------------------------------
    # Low-level JSON I/O
    # ------------------------------------------------------------------

    def _load_json(self) -> dict:
        if self._path.exists():
            try:
                with open(self._path, encoding='utf-8') as fh:
                    return json.load(fh, object_hook=_custom_decoder)
            except (json.JSONDecodeError, OSError):
                logger.warning("Could not read %s - starting with empty settings.", self._path, exc_info=True)
        return {}

    def _flush(self) -> None:
        """Atomically write the in-memory dict to disk."""
        self._path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self._path.with_suffix('.tmp')
        with open(tmp, 'w', encoding='utf-8') as fh:
            json.dump(self._data, fh, default=_custom_encoder, ensure_ascii=False, indent=2)
        os.replace(tmp, self._path)

    # ------------------------------------------------------------------
    # Internal helpers (replace beginGroup / endGroup pattern)
    # ------------------------------------------------------------------

    def _get_group(self, group: str) -> dict:
        """Return the sub-dict for *group*, creating it if needed."""
        return self._data.setdefault(group, {})

    def _set_in_group(self, group: str, key: str, value: Any) -> None:
        self._get_group(group)[key] = value
        self._flush()

    def _get_from_group(self, group: str, key: str, default: Any = None) -> Any:
        return self._get_group(group).get(key, default)

    # ------------------------------------------------------------------
    # Public API  (unchanged signatures)
    # ------------------------------------------------------------------

    @property
    def property_items(self):
        return self.list_saved_items(property='property')

    def save_window_position(self, position: Any, size: Any, maximized: bool) -> None:
        """Save main-window geometry.  *position* and *size* may be QPoint/QSize or plain dicts."""
        grp = self._get_group('MainWindow')
        grp['position'] = position
        grp['size'] = size
        grp['maximized'] = bool(maximized)
        self._flush()

    def load_window_position(self) -> dict:
        """Load window position information with sensible defaults."""
        from qtpy.QtCore import QPoint, QSize

        grp = self._get_group('MainWindow')
        pos = grp.get('position')
        size = grp.get('size')

        # Ensure we return QPoint / QSize for the caller
        if isinstance(size, dict) and '__type__' in size:
            size = _custom_decoder(size)
        if isinstance(pos, dict) and '__type__' in pos:
            pos = _custom_decoder(pos)

        if not isinstance(size, QSize) or size.width() <= 0:
            size = QSize(900, 850)
        if not isinstance(pos, QPoint) or pos.x() <= 0:
            pos = QPoint(20, 20)

        maximized = grp.get('maximized', False)
        if isinstance(maximized, str):
            maximized = maximized.lower() in ('true', '1', 'yes')

        return {'size': size, 'position': pos, 'maximized': bool(maximized)}

    def save_current_dir(self, directory: str) -> None:
        """Save the current work directory."""
        self._set_in_group('WorkDir', 'dir', directory)

    def load_last_workdir(self) -> str:
        return self._get_from_group('WorkDir', 'dir', '') or ''

    def get_equipment_list(self) -> list:
        return sorted(self.list_saved_items('equipment'))

    def get_properties_list(self) -> list:
        return sorted(self.list_saved_items('property'))

    def load_property_keys_and_values(self) -> list:
        keylist = []
        for p in self.property_items:
            try:
                keylist.append(self.load_settings_list(property='property', item_name=p))
            except TypeError:
                pass
        return keylist

    def load_cif_keys_of_properties(self) -> list[str]:
        return [x[0] for x in self.load_property_keys_and_values()]

    def load_property_values_by_key(self, cif_key: str):
        num_value_pairs = []
        if self.property_keys and cif_key in self.property_keys:
            keys_and_values = self.property_keys_and_values[self.property_keys.index(cif_key)]
            if len(keys_and_values) >= 1:
                property_values = keys_and_values[1]
            else:
                property_values = ['']
            for n, val in enumerate(property_values):
                num_value_pairs.append((n, val))
            return num_value_pairs
        return [(0, '')]

    def save_template_list(self, name: str, items: list):
        """Save a template list at the root level."""
        logger.debug("Saving %s %s", name, items)
        self._data[name] = items
        self._flush()
        self.property_keys_and_values = self.load_property_keys_and_values()
        self.property_keys = self.load_cif_keys_of_properties()

    def save_key_value(self, name: str, item: str | list | tuple | dict | int | bool):
        """Save a single key/value pair at the root level."""
        self._data[name] = item
        self._flush()
        logger.debug("Saving %s %s", name, item)

    def load_value_of_key(self, key: str) -> Iterable | list | int | float | None:
        """Load a root-level value."""
        return self._data.get(key)

    def delete_template(self, property: str, name: str):
        """Delete a template entry from a group."""
        grp = self._get_group(property)
        grp.pop(name, None)
        self._flush()
        if property == 'equipment':
            deleted = self.load_value_of_key(key='deleted_templates') or []
            deleted.append(name)
            deleted = list(set(deleted))
            self.save_key_value(name='deleted_templates', item=deleted)

    @property
    def deleted_equipment(self):
        deleted = self.load_value_of_key(key='deleted_templates')
        return deleted or []

    def empty_deleted_list(self):
        self.save_key_value(name='deleted_templates', item=[])

    def load_options(self) -> dict:
        options = self.load_settings_dict('Options', 'options')
        if not options:
            options = {
                'report_text': True,
                'picture_width': 7.5,
                'without_h': False,
                'report_adp': True,
                'track_changes': False,
                'checkcif_url': 'https://checkcif.iucr.org/cgi-bin/checkcif_hkl.pl',
            }
        options.update({
            'atoms_table': True,
            'bonds_table': True,
            'hydrogen_bonds': True,
        })
        return options

    def save_options(self, options: dict):
        self.save_settings_dict('Options', 'options', options)

    def load_settings_dict(self, property: str = '', item_name: str = '') -> dict:
        settings = self._load_settings(property, item_name)
        return settings if isinstance(settings, dict) else {}

    def load_settings_list(self, property: str = '', item_name: str = '') -> list:
        settings = self._load_settings(property, item_name)
        if isinstance(settings, list):
            return settings
        return []

    def load_settings_list_as_dict(self, property: str, item_name: str):
        setting = self.load_settings_list(property, item_name)
        keydict = {}
        for p in setting:
            try:
                keydict[p[0]] = p[1]
            except (IndexError, TypeError):
                continue
        return keydict

    def _load_settings(self, property: str, item_name: str) -> Any | None:
        grp = self._get_group(property)
        if item_name in grp:
            return grp[item_name]
        return None

    def list_saved_items(self, property: str) -> list:
        return list(self._get_group(property).keys())

    def save_settings_dict(self, property: str, name: str, items) -> None:
        self._set_in_group(property, name, items)

    def _save_settings_value(self, items: Any, name: str, property: str) -> None:
        self._set_in_group(property, name, items)
        logger.debug("Saving %s %s", name, items)

    def save_settings_list(self, property: str, name: str, items: list):
        self._save_settings_value(items, name, property)

    # ------------------------------------------------------------------
    # New convenience wrappers (replace direct QSettings access)
    # ------------------------------------------------------------------

    def load_recent_files(self) -> list[str]:
        """Return the list of recently opened files."""
        val = self._data.get('recent_files')
        if isinstance(val, list):
            return list(val)
        return []

    def save_recent_files(self, recent: list[str]) -> None:
        """Persist the recent-files list."""
        self._data['recent_files'] = recent
        self._flush()

    def load_property_list(self) -> list | None:
        """Return the root-level property_list value (used by properties import)."""
        return self._data.get('property_list')


if __name__ == '__main__':
    s = FinalCifSettings()
    print('load_property_by_key:', s.load_property_values_by_key(cif_key='_diffrn_ambient_environment'))
    print(s.load_cif_keys_of_properties())
