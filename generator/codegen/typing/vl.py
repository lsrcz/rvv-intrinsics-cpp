from dataclasses import dataclass

from codegen.typing import base, misc


@dataclass(frozen=True, kw_only=True)
class VLType(base.Type):
    ratio: misc.SizeTValue

    @property
    def cpp_repr(self) -> str:
        return f"vl_t<{self.ratio.cpp_repr}>"
