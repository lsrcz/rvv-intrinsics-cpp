from typing import Callable

from codegen import constraints, func
from codegen.param_list import function
from codegen.typing import elem, misc, vl, vreg


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


def widening_vx_or_wx_op(
    inst: str, is_vx: bool, signed: bool
) -> Callable[[str], func.Function]:
    return func.template_elem_ratio(
        lambda elem_type, ratio: vreg.ConcreteVRegType(
            elem_type=elem.WidenElemType(base_type=elem_type), ratio=ratio
        ),
        inst,
        lambda variant, elem_type, ratio: func.elem_ratio_extend_param_list(
            elem.WidenElemType(base_type=elem_type),
            ratio,
            variant,
            function.FunctionTypedParamList(
                function.TypedParam(
                    type=vreg.ConcreteVRegType(
                        elem_type=(
                            elem_type
                            if is_vx
                            else elem.WidenElemType(base_type=elem_type)
                        ),
                        ratio=ratio,
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
                f"__riscv_{inst}"
                + ("" if signed else "u")
                + ("_vx" if is_vx else "_wx")
                + func.rv_postfix(variant, overloaded=True),
                param_list,
            )
            + ";"
        ),
        require_clauses=lambda elem_type, ratio: elem_require_clauses(
            "signed" if signed else "unsigned", elem_type, ratio, widening=True
        ),
    )


def widening_vx_op(inst: str, signed: bool) -> Callable[[str], func.Function]:
    return widening_vx_or_wx_op(inst, True, signed)


def widening_wx_op(inst: str, signed: bool) -> Callable[[str], func.Function]:
    return widening_vx_or_wx_op(inst, False, signed)


def widening_vv_or_wv_op(
    inst: str, is_vv: bool, signed: bool
) -> Callable[[str], func.Function]:
    return func.template_vreg_ratio(
        lambda vreg_type, ratio: vreg.WidenVRegType(base_type=vreg_type),
        inst,
        lambda variant, vreg_type, ratio: func.vreg_ratio_extend_param_list(
            vreg.WidenVRegType(base_type=vreg_type),
            ratio,
            variant,
            function.FunctionTypedParamList(
                function.TypedParam(
                    type=(
                        vreg_type
                        if is_vv
                        else vreg.WidenVRegType(base_type=vreg_type)
                    ),
                    name="vs2",
                ),
                function.TypedParam(type=vreg_type, name="vs1"),
                function.TypedParam(type=vl.VLType(ratio=ratio), name="vl"),
            ),
        ),
        lambda variant, elem_type, ratio, param_list: (
            "  return "
            + func.apply_function(
                f"__riscv_{inst}"
                + ("" if signed else "u")
                + ("_vv" if is_vv else "_wv")
                + func.rv_postfix(variant, overloaded=True),
                param_list,
            )
            + ";"
        ),
        require_clauses=lambda vreg_type, ratio: vreg_require_clauses(
            "signed" if signed else "unsigned", vreg_type, ratio, widening=True
        ),
    )


def widening_vv_op(inst: str, signed: bool) -> Callable[[str], func.Function]:
    return widening_vv_or_wv_op(inst, True, signed)


def widening_wv_op(inst: str, signed: bool) -> Callable[[str], func.Function]:
    return widening_vv_or_wv_op(inst, False, signed)


def widening_op(inst: str, signed: bool) -> Callable[[str], func.Function]:
    return func.template_vreg_ratio(
        lambda vreg_type, ratio: vreg.WidenVRegType(base_type=vreg_type),
        inst,
        lambda variant, vreg_type, ratio: func.vreg_ratio_extend_param_list(
            vreg.WidenVRegType(base_type=vreg_type),
            ratio,
            variant,
            function.FunctionTypedParamList(
                function.TypedParam(
                    type=vreg_type,
                    name="vs2",
                ),
                function.TypedParam(type=vl.VLType(ratio=ratio), name="vl"),
            ),
        ),
        lambda variant, elem_type, ratio, param_list: (
            "  return "
            + func.apply_function(
                f"__riscv_{inst}"
                + ("" if signed else "u")
                + "_x"
                + func.rv_postfix(variant, overloaded=True),
                param_list,
            )
            + ";"
        ),
        require_clauses=lambda vreg_type, ratio: vreg_require_clauses(
            "signed" if signed else "unsigned", vreg_type, ratio, widening=True
        ),
    )


def extending_op(
    inst: str, signed: bool
) -> Callable[[str, int], func.Function]:
    def inner(variant: str, n: int) -> func.Function:
        return func.template_vreg_ratio(
            lambda vreg_type, ratio: vreg.WidenNVRegType(
                n=n, base_type=vreg_type
            ),
            f"{inst}{n}",
            lambda variant, vreg_type, ratio: func.vreg_ratio_extend_param_list(
                vreg.WidenNVRegType(n=n, base_type=vreg_type),
                ratio,
                variant,
                function.FunctionTypedParamList(
                    function.TypedParam(
                        type=vreg_type,
                        name="vs2",
                    ),
                    function.TypedParam(type=vl.VLType(ratio=ratio), name="vl"),
                ),
            ),
            lambda variant, elem_type, ratio, param_list: (
                "  return "
                + func.apply_function(
                    f"__riscv_{inst}"
                    + f"_vf{n}"
                    + func.rv_postfix(variant, overloaded=True),
                    param_list,
                )
                + ";"
            ),
            require_clauses=lambda vreg_type, ratio: vreg_require_clauses(
                "signed" if signed else "unsigned", vreg_type, ratio, widening=n
            ),
        )(variant)

    return inner
