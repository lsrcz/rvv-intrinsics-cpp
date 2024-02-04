from . import type
from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class VMaskType(type.Type):
    ratio: int

    @property
    def cpp_repr(self) -> str:
        return f"vmask_t<{self.ratio}>"
