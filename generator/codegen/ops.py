from typing import Callable
from codegen.param_list import function
from codegen import func, constraints
from codegen.type import vreg, vl, elem, misc


def elem_require_clauses(
    allowed_type_category: str, elem_type: elem.ElemType, ratio: misc.SizeTValue
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
    return ret


def vreg_require_clauses(
    allowed_type_category: str, vreg_type: vreg.VRegType, ratio: misc.SizeTValue
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
    return ret


def vi_op(
    inst: str, allowed_type_category: str
) -> Callable[[str], func.Function]:
    return func.template_elem_ratio(
        lambda elem_type, ratio: vreg.ConcreteVRegType(
            elem_type=elem_type, ratio=ratio
        ),
        inst,
        lambda variant, elem_type, ratio: func.elem_ratio_extend_param_list(
            elem_type,
            ratio,
            variant,
            function.FunctionTypedParamList(
                function.TypedParam(
                    type=vreg.ConcreteVRegType(
                        elem_type=elem_type, ratio=ratio
                    ),
                    name="vs2",
                ),
                function.TypedParam(type=elem_type, name="rs1"),
                function.TypedParam(type=vl.VLType(ratio=ratio), name="vl"),
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
                    name="vs2",
                ),
                function.TypedParam(type=vreg_type, name="vs1"),
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
