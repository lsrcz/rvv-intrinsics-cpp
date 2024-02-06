from . import type
from . import misc
from . import elem
from . import kind as k
from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class VRegType(type.Type):
    pass


@dataclass(frozen=True, kw_only=True)
class ConcreteVRegType(VRegType):
    elem_type: elem.ElemType
    ratio: misc.SizeTValue

    @property
    def cpp_repr(self) -> str:
        return f"vreg_t<{self.elem_type.cpp_repr}, {self.ratio.cpp_repr}>"


@dataclass(frozen=True, kw_only=True)
class RawVRegType(ConcreteVRegType):
    elem_type: elem.RawElemType
    ratio: misc.LitSizeTValue


@dataclass(frozen=True, kw_only=True)
class ParamVRegType(VRegType, type.TypeParam):
    @property
    def kind(self) -> k.TypeKind:
        return k.TypeKind()


@dataclass(frozen=True, kw_only=True)
class WidenVRegType(VRegType):
    base_type: VRegType

    @property
    def cpp_repr(self) -> str:
        return f"widen_t<{self.base_type.cpp_repr}>"
