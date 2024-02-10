from codegen.typing import base, elem, lmul, misc, vreg


def supported_ratio(ratio: misc.SizeTValue) -> str:
    return f"SupportedRatio<{ratio.cpp_repr}>"


def compatible_elem_ratio(
    elem_type: elem.ElemType, ratio: misc.SizeTValue
) -> str:
    return f"CompatibleElemRatio<{elem_type.cpp_repr}, {ratio.cpp_repr}>"


def compatible_vreg_ratio(
    vreg_type: vreg.VRegType, ratio: misc.SizeTValue
) -> str:
    return f"CompatibleVRegRatio<{vreg_type.cpp_repr}, {ratio.cpp_repr}>"


def compatible_elem_lmul(elem_type: elem.ElemType, l: lmul.LMulValue) -> str:
    return f"CompatibleElemLMul<{elem_type.cpp_repr}, {l.cpp_repr}>"


def has_width(elem_type: elem.ElemType, width: int) -> str:
    return f"(sizeof({elem_type.cpp_repr}) == {width // 8})"


def supported_integral_element(elem_type: elem.ElemType) -> str:
    return f"SupportedIntegralElement<{elem_type.cpp_repr}>"


def supported_signed_element(elem_type: elem.ElemType) -> str:
    return f"SupportedSignedElement<{elem_type.cpp_repr}>"


def supported_unsigned_element(elem_type: elem.ElemType) -> str:
    return f"SupportedUnsignedElement<{elem_type.cpp_repr}>"


def supported_floating_point_element(
    elem_type: elem.ElemType, need_zvfh: bool
) -> str:
    return (
        f"SupportedFloatingPointElement<{elem_type.cpp_repr}, "
        + f"{'true' if need_zvfh else 'false'}>"
    )


def supported_integral_vreg(vreg_type: vreg.VRegType) -> str:
    return f"SupportedIntegralVReg<{vreg_type.cpp_repr}>"


def supported_signed_vreg(vreg_type: vreg.VRegType) -> str:
    return f"SupportedSignedVReg<{vreg_type.cpp_repr}>"


def supported_unsigned_vreg(vreg_type: vreg.VRegType) -> str:
    return f"SupportedUnsignedVReg<{vreg_type.cpp_repr}>"


def supported_floating_point_vreg(
    vreg_type: vreg.VRegType, need_zvfh: bool
) -> str:
    if need_zvfh:
        return f"SupportedFloatingPointVReg<{vreg_type.cpp_repr}>"
    else:
        return f"SupportedFloatingPointVReg<{vreg_type.cpp_repr}, false>"


def supported_vxrm(vxrm: base.Type) -> str:
    return f"SupportedVXRM<{vxrm.cpp_repr}>"


def supported_frm(frm: base.Type) -> str:
    return f"SupportedFRM<{frm.cpp_repr}>"
