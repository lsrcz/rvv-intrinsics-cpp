import abc
from dataclasses import dataclass

from codegen.typing import base, elem, misc


@dataclass(frozen=True, kw_only=True)
class VTupleType(base.Type, metaclass=abc.ABCMeta):
    pass


@dataclass(frozen=True, kw_only=True)
class ConcreteVTupleType(VTupleType):
    elem_type: elem.ElemType
    ratio: misc.SizeTValue
    tuple_size: misc.SizeTValue

    @property
    def cpp_repr(self) -> str:
        return f"vtuple_t<{self.elem_type.cpp_repr}, {self.ratio.cpp_repr}, {self.tuple_size.cpp_repr}>"


def concrete(
    elem_type: elem.ElemType,
    ratio: misc.SizeTValue,
    tuple_size: misc.SizeTValue,
) -> ConcreteVTupleType:
    return ConcreteVTupleType(
        elem_type=elem_type, ratio=ratio, tuple_size=tuple_size
    )
