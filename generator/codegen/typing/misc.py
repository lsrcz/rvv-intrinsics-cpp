import abc
from dataclasses import dataclass

from codegen.typing import base


@dataclass(frozen=True, kw_only=True)
class PtrType(base.Type):
    base_type: base.Type
    is_const: bool

    @property
    def cpp_repr(self) -> str:
        if isinstance(self.base_type, PtrType):
            raise ValueError("Nested pointers are not supported and not needed")
        quantifier: str = f"{'const ' if self.is_const else ''}"
        return f"{quantifier}{self.base_type.cpp_repr} *"


@dataclass(frozen=True, kw_only=True)
class VoidType(base.Type):
    @property
    def cpp_repr(self) -> str:
        return "void"


@dataclass(frozen=True, kw_only=True)
class SizeTType(base.Type):
    @property
    def cpp_repr(self) -> str:
        return "size_t"


size_t_kind: base.DataKind = base.DataKind(data_type=SizeTType())


@dataclass(frozen=True, kw_only=True)
class SizeTValue(base.Type, metaclass=abc.ABCMeta):
    pass


@dataclass(frozen=True, kw_only=True)
class LitSizeTValue(SizeTValue):
    value: int

    @property
    def cpp_repr(self) -> str:
        return str(self.value)


ALL_RATIO: list[LitSizeTValue] = [
    LitSizeTValue(value=1),
    LitSizeTValue(value=2),
    LitSizeTValue(value=4),
    LitSizeTValue(value=8),
    LitSizeTValue(value=16),
    LitSizeTValue(value=32),
    LitSizeTValue(value=64),
]


@dataclass(frozen=True, kw_only=True)
class ParamSizeTValue(SizeTValue, base.TypeParam):
    @property
    def kind(self) -> base.DataKind:
        return size_t_kind


@dataclass(frozen=True, kw_only=True)
class PtrdiffTType(base.Type):
    @property
    def cpp_repr(self) -> str:
        return "ptrdiff_t"
