#  ----------------------------------------------------------------------------
#  "THE BEER-WARE LICENSE" (Revision 42):
#  dkratzert@gmx.de> wrote this file.  As long as you retain
#  this notice you can do whatever you want with this stuff. If we meet some day,
#  and you think this stuff is worth it, you can buy me a beer in return.
#  Dr. Daniel Kratzert
#  ----------------------------------------------------------------------------
"""
Regenerate ``finalcif/cif/cif_keyword_mapping.py``.

This script downloads the upstream DDLm CIF dictionaries from the COMCIFS
GitHub repositories, parses every ``save_`` frame, and extracts the mapping
from the DDLm/CIF2 dotted name (``_definition.id``) to its preferred CIF 1.1
legacy alias (the first ``_alias.definition_id`` that uses underscore-only
notation, i.e. does not contain a dot).

Only mappings where the legacy alias is NOT a trivial ``replace('.', '_')`` of
the CIF2 name are kept; the trivial case is handled at runtime in
:func:`finalcif.cif.cif_file_io.CifContainer._translate_keyword_to_cif11`.

DDLm dictionaries covered:

* ``cif_core.dic``       -- COMCIFS/cif_core
* ``cif_pow.dic``        -- COMCIFS/Powder_Dictionary
* ``cif_ms.dic``         -- COMCIFS/Modulated_Structures
* ``ddl.dic``            -- COMCIFS/DDLm (DDLm reference dictionary)

Twin and restraints dictionaries are intentionally not included because they
only exist as DDL1 dictionaries (no CIF2 dotted names to translate).

Usage::

    uv run python scripts/generate_keyword_mapping.py

The script writes ``finalcif/cif/cif_keyword_mapping.py`` in-place. Cached
dictionary downloads are stored in ``work/dicts/`` and reused on subsequent
runs if the network is unavailable.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Iterable

import requests

REPO_ROOT = Path(__file__).resolve().parent.parent
CACHE_DIR = REPO_ROOT / 'work' / 'dicts'
OUTPUT_PATH = REPO_ROOT / 'finalcif' / 'cif' / 'cif_keyword_mapping.py'

DICTIONARIES: dict[str, str] = {
    'cif_core.dic': 'https://raw.githubusercontent.com/COMCIFS/cif_core/master/cif_core.dic',
    'cif_pow.dic' : 'https://raw.githubusercontent.com/COMCIFS/Powder_Dictionary/master/cif_pow.dic',
    'cif_ms.dic'  : 'https://raw.githubusercontent.com/COMCIFS/Modulated_Structures/master/cif_ms.dic',
    'ddl.dic'     : 'https://raw.githubusercontent.com/COMCIFS/DDLm/refs/heads/main/ddl.dic',
}

# Manual overrides for cases where the current upstream DDLm dictionary either
# has no _alias.definition_id, or where the listed alias is not the legacy
# form actually consumed by the wider crystallographic toolchain (PLATON,
# SHELX, CheckCIF, COD/CCDC deposition). These mappings reflect the most
# widely used CIF 1.1 names historically present in the cif_core 2.x
# dictionary series and are pinned regardless of dictionary regeneration.
# Keep alphabetically sorted by source key.
MANUAL_OVERRIDES: dict[str, str] = {
    '_atom_scat_versus_stol.atom_type'      : '_atom_type_scat_versus_stol_list',
    '_atom_site.refinement_flags_posn'      : '_atom_site_refinement_flags',
    '_atom_sites_cartn_transform.mat_11'    : '_atom_sites_Cartn_tran_matrix_11',
    '_atom_sites_cartn_transform.mat_12'    : '_atom_sites_Cartn_tran_matrix_12',
    '_atom_sites_cartn_transform.mat_13'    : '_atom_sites_Cartn_tran_matrix_13',
    '_atom_sites_cartn_transform.mat_21'    : '_atom_sites_Cartn_tran_matrix_21',
    '_atom_sites_cartn_transform.mat_22'    : '_atom_sites_Cartn_tran_matrix_22',
    '_atom_sites_cartn_transform.mat_23'    : '_atom_sites_Cartn_tran_matrix_23',
    '_atom_sites_cartn_transform.mat_31'    : '_atom_sites_Cartn_tran_matrix_31',
    '_atom_sites_cartn_transform.mat_32'    : '_atom_sites_Cartn_tran_matrix_32',
    '_atom_sites_cartn_transform.mat_33'    : '_atom_sites_Cartn_tran_matrix_33',
    '_atom_sites_cartn_transform.vec_1'     : '_atom_sites_Cartn_tran_vector_1',
    '_atom_sites_cartn_transform.vec_2'     : '_atom_sites_Cartn_tran_vector_2',
    '_atom_sites_cartn_transform.vec_3'     : '_atom_sites_Cartn_tran_vector_3',
    '_diffrn.ambient_temperature'           : '_cell_measurement_temperature',
    '_diffrn_radiation_wavelength.value'    : '_cell_measurement_wavelength',
    '_publ_contact_author.name'             : '_publ_contact_author',
    '_space_group.IT_number'                : '_symmetry_Int_Tables_number',
    '_space_group.crystal_system'           : '_symmetry_cell_setting',
    '_space_group.name_H-M_alt'             : '_symmetry_space_group_name_H-M',
    '_space_group.name_H-M_full'            : '_symmetry_space_group_name_H-M',
    '_space_group.name_Hall'                : '_symmetry_space_group_name_Hall',
    '_space_group_symop.id'                 : '_symmetry_equiv_pos_site_id',
    '_space_group_symop.operation_xyz'      : '_symmetry_equiv_pos_as_xyz',
}

# A CIF data name starts with underscore followed by allowed characters.
_QUOTED_VALUE = re.compile(r"""['"]([^'"]+)['"]""")
_SAVE_OPEN = re.compile(r'^\s*save_(\S+)\s*$', re.IGNORECASE)
_SAVE_CLOSE = re.compile(r'^\s*save_\s*$', re.IGNORECASE)


def download_dictionaries() -> dict[str, str]:
    """Download (or load from cache) all DDLm dictionaries and return their text."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    texts: dict[str, str] = {}
    for filename, url in DICTIONARIES.items():
        cache_file = CACHE_DIR / filename
        text: str | None = None
        try:
            print(f'Downloading {url} ...')
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                text = response.text
                cache_file.write_text(text, encoding='utf-8')
            else:
                print(f'  HTTP {response.status_code}; will try cache.')
        except requests.RequestException as exc:
            print(f'  Download failed ({exc}); will try cache.')
        if text is None:
            if cache_file.exists():
                print(f'  Using cached {cache_file}.')
                text = cache_file.read_text(encoding='utf-8')
            else:
                raise RuntimeError(
                    f'Could not download {url} and no cache at {cache_file}.'
                )
        texts[filename] = text
    return texts


def iter_save_frames(text: str) -> Iterable[list[str]]:
    """Yield the lines (excluding the open/close markers) of each ``save_`` frame."""
    current: list[str] | None = None
    for line in text.splitlines():
        if _SAVE_CLOSE.match(line):
            if current is not None:
                yield current
                current = None
            continue
        if _SAVE_OPEN.match(line):
            current = []
            continue
        if current is not None:
            current.append(line)


def _value_from_line(line: str) -> str | None:
    """Extract the value following a tag on the same line, if any."""
    # Strip the leading tag (whatever it is) and look for the first non-space.
    parts = line.split(None, 1)
    if len(parts) < 2:
        return None
    rest = parts[1].strip()
    if not rest:
        return None
    match = _QUOTED_VALUE.match(rest)
    if match:
        return match.group(1)
    # Unquoted value -- take first whitespace-delimited token.
    return rest.split()[0]


def _collect_loop_values(lines: list[str], start: int) -> tuple[list[str], int]:
    """
    Given that ``lines[start - 1]`` was a ``loop_`` and ``lines[start]`` is the
    first ``_alias.definition_id`` tag in the loop header, scan forward to
    collect the loop values for that single column. The loop is assumed to
    contain only the ``_alias.definition_id`` column (the common case in
    DDLm dictionaries for this tag).
    """
    # Read tag header lines (all starting with '_')
    idx = start
    tag_count = 0
    while idx < len(lines) and lines[idx].strip().startswith('_'):
        tag_count += 1
        idx += 1
    # Then read value rows until we hit a non-value (blank line, tag, or save).
    values: list[str] = []
    while idx < len(lines):
        stripped = lines[idx].strip()
        if not stripped:
            break
        if stripped.startswith('_'):
            break
        if stripped.lower().startswith('loop_'):
            break
        # Collect all whitespace-separated tokens (handling quotes).
        for token in _split_cif_tokens(stripped):
            values.append(token)
        idx += 1
    # If the loop had multiple columns, every Nth value (N=tag_count) belongs
    # to the alias column. We only handle tag_count==1 for safety; otherwise
    # return only the matching column.
    if tag_count <= 1:
        return values, idx
    # Find the column index of _alias.definition_id within the tag block.
    column_index = 0  # By construction start points to the alias tag.
    return values[column_index::tag_count], idx


def _split_cif_tokens(line: str) -> list[str]:
    """Split a CIF data line into tokens, respecting single/double quotes."""
    tokens: list[str] = []
    i = 0
    n = len(line)
    while i < n:
        c = line[i]
        if c.isspace():
            i += 1
            continue
        if c in ("'", '"'):
            quote = c
            j = i + 1
            while j < n and line[j] != quote:
                j += 1
            tokens.append(line[i + 1:j])
            i = j + 1
        else:
            j = i
            while j < n and not line[j].isspace():
                j += 1
            tokens.append(line[i:j])
            i = j
    return tokens


def extract_aliases(text: str) -> dict[str, list[str]]:
    """
    Return a mapping ``{definition_id: [alias, alias, ...]}`` (order preserved
    as found in the dictionary) for every ``save_`` frame in *text*.
    """
    aliases: dict[str, list[str]] = {}
    for frame_lines in iter_save_frames(text):
        definition_id: str | None = None
        frame_aliases: list[str] = []
        i = 0
        while i < len(frame_lines):
            line = frame_lines[i]
            stripped = line.strip()
            if stripped.startswith('_definition.id'):
                value = _value_from_line(stripped)
                if value:
                    definition_id = value
                i += 1
                continue
            if stripped.startswith('_alias.definition_id'):
                value = _value_from_line(stripped)
                if value:
                    frame_aliases.append(value)
                i += 1
                continue
            if stripped.lower().startswith('loop_'):
                # Look ahead to see if this loop's first tag is _alias.definition_id.
                j = i + 1
                while j < len(frame_lines) and not frame_lines[j].strip():
                    j += 1
                if j < len(frame_lines) and frame_lines[j].strip().startswith('_alias.definition_id'):
                    values, new_i = _collect_loop_values(frame_lines, j)
                    frame_aliases.extend(values)
                    i = new_i
                    continue
            i += 1
        if definition_id and frame_aliases:
            aliases[definition_id] = frame_aliases
    return aliases


def choose_preferred_legacy(aliases: list[str]) -> str | None:
    """
    Pick the most widely used CIF 1.1 legacy alias from *aliases*.

    Preference order:

    1. The first alias whose name uses *only* underscores (no dot) -- this is
       the historical DDL1/CIF 1.1 form (e.g. ``_cell_length_a``).
    2. Otherwise ``None`` (the alias is itself a DDLm/mmCIF dotted name and
       provides no CIF 1.1 translation).
    """
    for alias in aliases:
        if '.' not in alias:
            return alias
    return None


def build_mapping_table(texts: dict[str, str]) -> dict[str, str]:
    """Merge alias maps from all dictionaries and filter out trivial mappings."""
    merged: dict[str, str] = {}
    for filename, text in texts.items():
        per_file = extract_aliases(text)
        print(f'  {filename}: {len(per_file)} definitions with aliases.')
        for definition_id, alias_list in per_file.items():
            preferred = choose_preferred_legacy(alias_list)
            if preferred is None:
                continue
            if '.' not in definition_id:
                # Already a legacy-style name; nothing to translate.
                continue
            trivial = definition_id.replace('.', '_')
            if preferred == trivial:
                continue
            # First dictionary wins on conflict (core overrides extensions).
            merged.setdefault(definition_id, preferred)
    return merged


FILE_HEADER = '''\
#  ----------------------------------------------------------------------------
#  "THE BEER-WARE LICENSE" (Revision 42):
#  dkratzert@gmx.de> wrote this file.  As long as you retain
#  this notice you can do whatever you want with this stuff. If we meet some day,
#  and you think this stuff is worth it, you can buy me a beer in return.
#  Dr. Daniel Kratzert
#  ----------------------------------------------------------------------------

# Auto-generated by scripts/generate_keyword_mapping.py -- DO NOT EDIT BY HAND.
#
# Mapping of CIF2/DDLm dotted data names to their preferred CIF 1.1 legacy
# alias, restricted to entries where a plain ``replace('.', '_')`` would NOT
# yield the correct legacy name. Trivial cases are handled at runtime in
# CifContainer._translate_keyword_to_cif11.
#
# Source dictionaries (DDLm):
#   * cif_core.dic  -- https://github.com/COMCIFS/cif_core
#   * cif_pow.dic   -- https://github.com/COMCIFS/Powder_Dictionary
#   * cif_ms.dic    -- https://github.com/COMCIFS/Modulated_Structures
#   * ddl.dic       -- https://github.com/COMCIFS/DDLm
#
# When several legacy aliases are listed in a DDLm definition, the first
# underscore-only (non-dotted) alias is selected as the most widely used form.
# A small set of MANUAL_OVERRIDES (defined in the generator script) pins the
# historically dominant CIF 1.1 names consumed by PLATON / SHELX / CheckCIF
# / COD / CCDC even when the upstream dictionary no longer lists them as
# aliases.
'''


def render_mapping_file(mapping: dict[str, str]) -> str:
    """Render the final ``cif_keyword_mapping.py`` source text."""
    if not mapping:
        raise RuntimeError('Refusing to overwrite mapping with an empty table.')
    keys = sorted(mapping)
    key_width = max(len(repr(k)) for k in keys)
    lines = [FILE_HEADER, 'CIF2_TO_CIF11_KEYWORD_TABLE = {']
    for key in keys:
        value = mapping[key]
        lines.append(f'    {repr(key):<{key_width}}: {value!r},')
    lines.append('}')
    lines.append('')
    return '\n'.join(lines)


def main() -> int:
    texts = download_dictionaries()
    print('Parsing dictionaries ...')
    mapping = build_mapping_table(texts)
    print(f'Dictionary-derived non-trivial mappings: {len(mapping)}')
    # Manual overrides take precedence over dictionary-derived entries because
    # they pin the historically most widely used CIF 1.1 alias.
    mapping.update(MANUAL_OVERRIDES)
    print(f'After applying {len(MANUAL_OVERRIDES)} manual overrides: {len(mapping)}')
    rendered = render_mapping_file(mapping)
    OUTPUT_PATH.write_text(rendered, encoding='utf-8')
    print(f'Wrote {OUTPUT_PATH} ({len(rendered)} bytes).')
    return 0


if __name__ == '__main__':
    sys.exit(main())







