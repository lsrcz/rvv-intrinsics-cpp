from . import type
from . import misc
from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class VLType(type.Type):
    ratio: misc.SizeTValue

    @property
    def cpp_repr(self) -> str:
        return f"vl_t<{self.ratio.cpp_repr}>"
