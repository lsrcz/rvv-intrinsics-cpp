import abc
from dataclasses import dataclass

from codegen.typing import base, misc
from codegen.typing import kind as k


@dataclass(frozen=True, kw_only=True)
class VMaskType(base.Type, metaclass=abc.ABCMeta):
    pass


@dataclass(frozen=True, kw_only=True)
class ConcreteVMaskType(VMaskType):
    ratio: misc.SizeTValue

    @property
    def cpp_repr(self) -> str:
        return f"vmask_t<{self.ratio}>"


def concrete(ratio: misc.SizeTValue) -> ConcreteVMaskType:
    return ConcreteVMaskType(ratio=ratio)


@dataclass(frozen=True, kw_only=True)
class ParamVMask(VMaskType, base.TypeParam):
    @property
    def kind(self) -> k.TypeKind:
        return k.type_kind


def param(typename: str) -> ParamVMask:
    return ParamVMask(typename=typename)
