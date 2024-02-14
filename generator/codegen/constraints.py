from codegen.typing import base, elem, lmul, misc, vreg, vmask


def supported_ratio(ratio: misc.SizeTValue) -> str:
    return f"SupportedRatio<{ratio.cpp_repr}>"


def compatible_elem_ratio(
    elem_type: elem.ElemType, ratio: misc.SizeTValue
) -> str:
    return f"CompatibleElemRatio<{elem_type.cpp_repr}, {ratio.cpp_repr}>"


def compatible_elem_ratio_tuple_size(
    elem_type: elem.ElemType,
    ratio: misc.SizeTValue,
    tuple_size: misc.SizeTValue,
) -> str:
    return f"CompatibleElemRatioTupleSize<{elem_type.cpp_repr}, {ratio.cpp_repr}, {tuple_size.cpp_repr}>"


def compatible_vreg_ratio(
    vreg_type: vreg.VRegType, ratio: misc.SizeTValue
) -> str:
    return f"CompatibleVRegRatio<{vreg_type.cpp_repr}, {ratio.cpp_repr}>"


def compatible_elem_lmul(elem_type: elem.ElemType, l: lmul.LMulValue) -> str:
    return f"CompatibleElemLMul<{elem_type.cpp_repr}, {l.cpp_repr}>"


def has_width(elem_type: elem.ElemType, width: int) -> str:
    return f"(sizeof({elem_type.cpp_repr}) == {width // 8})"


def does_not_have_width(elem_type: elem.ElemType, width: int) -> str:
    return f"(sizeof({elem_type.cpp_repr}) != {width // 8})"


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


def supported_vreg(vreg_type: vreg.VRegType) -> str:
    return f"SupportedVReg<{vreg_type.cpp_repr}>"


def supported_vmask(vmask_type: vmask.VMaskType) -> str:
    return f"SupportedVMask<{vmask_type.cpp_repr}>"


def supported_vreg_or_supported_vmask(ty: base.Type) -> str:
    return f"(SupportedVReg<{ty.cpp_repr}> || SupportedVMask<{ty.cpp_repr}>)"


def supported_vreg_or_supported_vtuple(ty: base.Type) -> str:
    return f"(SupportedVReg<{ty.cpp_repr}> || SupportedVTuple<{ty.cpp_repr}>)"


def supported_vxrm(vxrm: base.Type) -> str:
    return f"SupportedVXRM<{vxrm.cpp_repr}>"


def supported_frm(frm: base.Type) -> str:
    return f"SupportedFRM<{frm.cpp_repr}>"


def same_width(elem_type1: elem.ElemType, elem_type2: elem.ElemType) -> str:
    return f"(sizeof({elem_type1.cpp_repr}) == sizeof({elem_type2.cpp_repr}))"


def same_ratio(ratio1: misc.SizeTValue, ratio2: misc.SizeTValue) -> str:
    return f"({ratio1.cpp_repr} == {ratio2.cpp_repr})"


def not_same_type(type1: base.Type, type2: base.Type) -> str:
    return f"(!std::is_same_v<{type1.cpp_repr}, {type2.cpp_repr}>)"


def doesnt_have_width(elem_type: elem.ElemType, width: int) -> str:
    return f"(sizeof({elem_type.cpp_repr}) != {width // 8})"


def same_lmul(lmul1: lmul.LMulValue, lmul2: lmul.LMulValue) -> str:
    return f"({lmul1.cpp_repr} == {lmul2.cpp_repr})"


def has_lmul(vreg_type: vreg.VRegType, l: lmul.LMulValue) -> str:
    return same_lmul(vreg.get_lmul(vreg_type), l)


def valid_index(
    v_large: base.Type, v_small: base.Type, index: misc.SizeTValue
) -> str:
    return (
        f"ValidIndex<{v_large.cpp_repr}, {v_small.cpp_repr}, {index.cpp_repr}>"
    )
