from math import inf
from typing import Union, Type


class BaseLimits:
    upper: Union[int, float, str]
    lower: Union[int, float, str]
    valid: callable
    value_type: Type[Union[int, float, str]]
    help_text = str

    def __init__(self, lower, upper):
        self.lower = lower
        self.upper = upper
        self.valid = self.validate_cif_key

    def __repr__(self):
        return (f"<{self.__class__.__name__}(lower bound: {self.lower}, upper bound: {self.upper}, "
                f"type: {self.value_type})> )>")

    def validate_cif_key(self, value: str):
        valid = False
        if value in ('', '?', '.'):
            return True
        try:
            value = self.value_type(value)
        except Exception:
            return False
        if self.lower <= value <= self.upper:
            valid = True
        return valid


class Integerlimits(BaseLimits):
    value_type = int

    def __init__(self, lower: int, upper: int):
        super().__init__(lower, upper)

    def validate_cif_key(self, value: str):
        valid = super().validate_cif_key(value)
        if not value.replace('-', '').isdigit() and value not in ('', '?', '.'):
            valid = False
        return valid


class Floatlimits(BaseLimits):
    value_type = float

    def __init__(self, lower: float, upper: float):
        super().__init__(lower, upper)


validators: dict[str, BaseLimits] = {
    '_cell_measurement_reflns_used': Integerlimits(lower=0, upper=10 ** 12),
    '_chemical_melting_point'      : Floatlimits(lower=0.0, upper=1.0 * 10 ** 12),
    '_diffrn_reflns_number'        : Integerlimits(lower=0, upper=10 ** 12),

}

if __name__ == '__main__':
    limits = validators['_chemical_melting_point']
    print(limits.valid(5))
