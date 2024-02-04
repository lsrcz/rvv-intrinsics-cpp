from . import type
from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class VLType(type.Type):
    ratio: int

    @property
    def cpp_repr(self) -> str:
        return f"vl_t<{self.ratio}>"
