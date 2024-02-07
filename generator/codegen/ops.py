from typing import Callable

from codegen import constraints, func
from codegen.param_list import function
from codegen.typing import elem, misc, vl, vmask, vreg


def elem_require_clauses(
    allowed_type_category: str,
    elem_type: elem.ElemType,
    ratio: misc.SizeTValue,
    widening: bool = False,
) -> list[str]:
    ret: list[str] = []
    match allowed_type_category:
        case "int":
            ret.append(constraints.is_supported_rvv_integral(elem_type))
        case "signed":
            ret.append(constraints.is_supported_rvv_signed(elem_type))
        case "unsigned":
            ret.append(constraints.is_supported_rvv_unsigned(elem_type))
        case "fp":
            ret.append(
                constraints.is_supported_rvv_floating_point(elem_type, True)
            )
        case "all":
            pass
        case _:
            raise ValueError(
                f"Unknown allowed type category: {allowed_type_category}"
            )
    ret.append(constraints.is_compatible_elem_ratio(elem_type, ratio))
    if widening:
        ret.append(constraints.widenable_type(elem_type))
        ret.append(
            constraints.is_compatible_elem_ratio(
                elem.WidenElemType(base_type=elem_type), ratio
            )
        )
    return ret


def vreg_require_clauses(
    allowed_type_category: str,
    vreg_type: vreg.VRegType,
    ratio: misc.SizeTValue,
    widening: bool | int = False,
) -> list[str]:
    ret: list[str] = []
    match allowed_type_category:
        case "int":
            ret.append(constraints.is_supported_integral_vreg(vreg_type))
        case "signed":
            ret.append(constraints.is_supported_signed_vreg(vreg_type))
        case "unsigned":
            ret.append(constraints.is_supported_unsigned_vreg(vreg_type))
        case "fp":
            ret.append(
                constraints.is_supported_floating_point_vreg(vreg_type, True)
            )
        case "all":
            pass
        case _:
            raise ValueError(
                f"Unknown allowed type category: {allowed_type_category}"
            )
    ret.append(constraints.is_compatible_vreg_ratio(vreg_type, ratio))
    if widening is True:
        ret.append(constraints.widenable_type(vreg_type))
        ret.append(
            constraints.is_compatible_vreg_ratio(
                vreg.WidenVRegType(base_type=vreg_type), ratio
            )
        )
    elif widening in [2, 4, 8]:
        ret.append(constraints.widenable_n_type(widening, vreg_type))
        ret.append(
            constraints.is_compatible_vreg_ratio(
                vreg.WidenNVRegType(n=widening, base_type=vreg_type), ratio
            )
        )
    return ret


def vx_op(
    inst: str,
    allowed_type_category: str,
    *,
    with_carry: bool = False,
    return_carry: bool = False,
    shifting: bool = False,
) -> Callable[[str], func.Function]:
    if return_carry:
        assert with_carry
    if with_carry:
        assert allowed_type_category in ["int", "signed", "unsigned"]
    return func.template_elem_ratio(
        lambda elem_type, ratio: (
            vmask.VMaskType(ratio=ratio)
            if return_carry
            else vreg.ConcreteVRegType(elem_type=elem_type, ratio=ratio)
        ),
        inst,
        lambda variant, elem_type, ratio: func.elem_ratio_extend_param_list(
            elem_type,
            ratio,
            variant,
            (
                function.FunctionTypedParamList(
                    function.TypedParam(
                        type=vreg.ConcreteVRegType(
                            elem_type=elem_type, ratio=ratio
                        ),
                        name="vs2",
                    ),
                    function.TypedParam(
                        type=misc.SizeTType() if shifting else elem_type,
                        name="rs1",
                    ),
                )
                + (
                    function.FunctionTypedParamList(
                        function.TypedParam(
                            type=vmask.VMaskType(ratio=ratio), name="v0"
                        )
                    )
                    if with_carry
                    else function.FunctionTypedParamList()
                )
                + function.FunctionTypedParamList(
                    function.TypedParam(type=vl.VLType(ratio=ratio), name="vl"),
                )
            ),
        ),
        lambda variant, elem_type, ratio, param_list: (
            "  return "
            + func.apply_function(
                f"__riscv_{inst}" + func.rv_postfix(variant, overloaded=True),
                param_list,
            )
            + ";"
        ),
        require_clauses=lambda elem_type, ratio: elem_require_clauses(
            allowed_type_category, elem_type, ratio
        ),
    )


def vv_op(
    inst: str,
    allowed_type_category: str,
    with_carry: bool = False,
    return_carry: bool = False,
    shifting: bool = False,
) -> Callable[[str], func.Function]:

    if return_carry:
        assert with_carry
    if with_carry:
        assert allowed_type_category in ["int", "signed", "unsigned"]
    return func.template_vreg_ratio(
        lambda vreg_type, ratio: (
            vmask.VMaskType(ratio=ratio) if return_carry else vreg_type
        ),
        inst,
        lambda variant, vreg_type, ratio: func.vreg_ratio_extend_param_list(
            vreg_type,
            ratio,
            variant,
            function.FunctionTypedParamList(
                function.TypedParam(
                    type=vreg_type,
                    name="vs2",
                ),
                function.TypedParam(
                    type=(
                        vreg.ToUnsignedVRegType(base_type=vreg_type)
                        if shifting
                        else vreg_type
                    ),
                    name="vs1",
                ),
            )
            + (
                function.FunctionTypedParamList(
                    function.TypedParam(
                        type=vmask.VMaskType(ratio=ratio), name="v0"
                    )
                )
                if with_carry
                else function.FunctionTypedParamList()
            )
            + function.FunctionTypedParamList(
                function.TypedParam(type=vl.VLType(ratio=ratio), name="vl"),
            ),
        ),
        lambda variant, vreg_type, ratio, param_list: (
            "  return "
            + func.apply_function(
                f"__riscv_{inst}" + func.rv_postfix(variant, overloaded=True),
                param_list,
            )
            + ";"
        ),
        require_clauses=lambda vreg_type, ratio: vreg_require_clauses(
            allowed_type_category, vreg_type, ratio
        ),
    )


def v_op(
    inst: str, allowed_type_category: str
) -> Callable[[str], func.Function]:

    return func.template_vreg_ratio(
        lambda vreg_type, ratio: vreg_type,
        inst,
        lambda variant, vreg_type, ratio: func.vreg_ratio_extend_param_list(
            vreg_type,
            ratio,
            variant,
            function.FunctionTypedParamList(
                function.TypedParam(
                    type=vreg_type,
                    name="vs",
                ),
                function.TypedParam(type=vl.VLType(ratio=ratio), name="vl"),
            ),
        ),
        lambda variant, vreg_type, ratio, param_list: (
            "  return "
            + func.apply_function(
                f"__riscv_{inst}" + func.rv_postfix(variant, overloaded=True),
                param_list,
            )
            + ";"
        ),
        require_clauses=lambda vreg_type, ratio: vreg_require_clauses(
            allowed_type_category, vreg_type, ratio
        ),
    )
