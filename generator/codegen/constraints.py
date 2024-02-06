from codegen.type import elem
from codegen.type import misc
from codegen.type import lmul


def is_supported_ratio(ratio: misc.SizeTValue) -> str:
    return f"is_supported_ratio<{ratio.cpp_repr}>"


def is_compatible_elem_ratio(
    elem_type: elem.ElemType, ratio: misc.SizeTValue
) -> str:
    return f"is_compatible_elem_ratio<{elem_type.cpp_repr}, {ratio.cpp_repr}>"


def is_compatible_elem_lmul(
    elem_type: elem.ElemType, lmul: lmul.LMulValue
) -> str:
    return f"is_compatible_elem_lmul<{elem_type.cpp_repr}, {lmul.cpp_repr}>"


def has_width(elem_type: elem.ElemType, width: int) -> str:
    return f"(sizeof({elem_type.cpp_repr}) == {width // 8})"
