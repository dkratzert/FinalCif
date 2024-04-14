import dataclasses
from typing import Union, Callable, Type


@dataclasses.dataclass(frozen=False)
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

    def validate_cif_key(self, value):
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


@dataclasses.dataclass(frozen=False)
class Integerlimits(BaseLimits):
    value_type = int

    def __init__(self, lower: int, upper: int):
        super().__init__(lower, upper)


@dataclasses.dataclass(frozen=False)
class Floatlimits(BaseLimits):
    value_type = float

    def __init__(self, lower: float, upper: float):
        super().__init__(lower, upper)


validators: dict[str, BaseLimits] = {
    '_chemical_melting_point': Floatlimits(lower=0.0, upper=99999999.9),
}

if __name__ == '__main__':
    limits = validators['_chemical_melting_point']
    print(limits.valid(5))
