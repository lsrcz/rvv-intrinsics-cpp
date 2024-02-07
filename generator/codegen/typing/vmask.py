from dataclasses import dataclass

from codegen.typing import base, misc


@dataclass(frozen=True, kw_only=True)
class VMaskType(base.Type):
    ratio: misc.SizeTValue

    @property
    def cpp_repr(self) -> str:
        return f"vmask_t<{self.ratio}>"


def vmask(ratio: misc.SizeTValue) -> VMaskType:
    return VMaskType(ratio=ratio)
