from codegen.type import elem, lmul, misc, vreg, type


def is_supported_ratio(ratio: misc.SizeTValue) -> str:
    return f"is_supported_ratio<{ratio.cpp_repr}>"


def is_compatible_elem_ratio(
    elem_type: elem.ElemType, ratio: misc.SizeTValue
) -> str:
    return f"is_compatible_elem_ratio<{elem_type.cpp_repr}, {ratio.cpp_repr}>"


def is_compatible_vreg_ratio(
    vreg_type: vreg.VRegType, ratio: misc.SizeTValue
) -> str:
    return f"is_compatible_vreg_ratio<{vreg_type.cpp_repr}, {ratio.cpp_repr}>"


def is_compatible_elem_lmul(
    elem_type: elem.ElemType, lmul: lmul.LMulValue
) -> str:
    return f"is_compatible_elem_lmul<{elem_type.cpp_repr}, {lmul.cpp_repr}>"


def has_width(elem_type: elem.ElemType, width: int) -> str:
    return f"(sizeof({elem_type.cpp_repr}) == {width // 8})"


def is_supported_rvv_integral(elem_type: elem.ElemType) -> str:
    return f"is_supported_rvv_integral<{elem_type.cpp_repr}>"


def is_supported_rvv_signed(elem_type: elem.ElemType) -> str:
    return f"is_supported_rvv_signed<{elem_type.cpp_repr}>"


def is_supported_rvv_unsigned(elem_type: elem.ElemType) -> str:
    return f"is_supported_rvv_unsigned<{elem_type.cpp_repr}>"


def is_supported_rvv_floating_point(
    elem_type: elem.ElemType, need_zvfh: bool
) -> str:
    return (
        f"is_supported_rvv_floating_point<{elem_type.cpp_repr}, "
        + f"{'true' if need_zvfh else 'false'}>"
    )


def is_supported_integral_vreg(vreg_type: vreg.VRegType) -> str:
    return f"is_supported_integral_vreg<{vreg_type.cpp_repr}>"


def is_supported_signed_vreg(vreg_type: vreg.VRegType) -> str:
    return f"is_supported_signed_vreg<{vreg_type.cpp_repr}>"


def is_supported_unsigned_vreg(vreg_type: vreg.VRegType) -> str:
    return f"is_supported_unsigned_vreg<{vreg_type.cpp_repr}>"


def is_supported_floating_point_vreg(
    vreg_type: vreg.VRegType, need_zvfh: bool
) -> str:
    return (
        f"is_supported_floating_point_vreg<{vreg_type.cpp_repr}, "
        + f"{'true' if need_zvfh else 'false'}>"
    )


def widenable_type(t: type.Type) -> str:
    return f"widenable<{t.cpp_repr}>"
