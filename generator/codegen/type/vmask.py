from . import type
from .. import ident
from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class VMaskType(type.Type):
    ratio: int

    @property
    def cpp_repr(self) -> str:
        return f"{ident.vmask_t}<{self.ratio}>"
