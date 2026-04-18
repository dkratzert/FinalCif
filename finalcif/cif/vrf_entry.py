from __future__ import annotations

from dataclasses import dataclass, field

import gemmi


@dataclass
class VRFEntry:
    """
    Represents a single CIF Validation Response Form (VRF) entry.

    A VRF entry corresponds to a CIF key of the form ``_vrf_PLATXXX_DataName``
    whose value is a semicolon-delimited text block containing a PROBLEM line
    and a RESPONSE line, for example::

        _vrf_PLAT699_DK_zucker2_0m
        ;
        PROBLEM: Missing _exptl_crystal_description Value .......     Please Do !
        RESPONSE: The crystal was a colourless plate.
        ;
    """

    key: str
    data_name: str
    problem: str
    response: str
    alert_num: str
    level: str = field(default='')

    @property
    def value(self) -> str:
        """CIF-format text block content for this VRF entry (without semicolons)."""
        return f"PROBLEM: {self.problem}\nRESPONSE: {self.response}\n"

    @classmethod
    def from_html_form(cls, form: dict[str, str]) -> VRFEntry:
        """Construct a VRFEntry from a response-forms dict parsed from the CheckCIF HTML."""
        return cls(
            key=form['name'],
            data_name=form['data_name'],
            problem=form['problem'],
            response='',
            alert_num=form['alert_num'],
            level=form.get('level', ''),
        )

    @classmethod
    def from_cif_pair(cls, key: str, raw_value: str) -> VRFEntry:
        """
        Construct a VRFEntry from a ``_vrf_*`` key and its raw CIF value.

        The raw CIF value is a semicolon-delimited text block whose content has
        the form::

            PROBLEM: <problem text>
            RESPONSE: <response text>

        Multi-line responses (continuation lines after the ``RESPONSE:`` line)
        are supported.
        """
        text = gemmi.cif.as_string(raw_value).strip()
        # key is like _vrf_PLAT307_DataName → split gives ['', 'vrf', 'PLAT307', 'DataName', ...]
        parts = key.split('_')
        alert_num = parts[2] if len(parts) > 2 else ''
        data_name = '_'.join(parts[3:]) if len(parts) > 3 else ''

        problem = ''
        response_lines: list[str] = []
        in_response = False
        for line in text.splitlines():
            if line.startswith('PROBLEM: '):
                problem = line[9:]
            elif line.startswith('RESPONSE:'):
                in_response = True
                # strip the 'RESPONSE: ' prefix (10 chars) or 'RESPONSE:' (9 chars)
                response_lines.append(line[9:].lstrip(' '))
            elif in_response:
                response_lines.append(line)

        response = '\n'.join(response_lines).strip()
        return cls(
            key=key,
            data_name=data_name,
            problem=problem,
            response=response,
            alert_num=alert_num,
            level='',
        )
