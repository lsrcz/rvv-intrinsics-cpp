from typing import Callable

from codegen import constraints, func
from codegen.param_list import function
from codegen.typing import elem, misc, vl, vmask, vreg, base


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
            constraints.is_compatible_elem_ratio(elem.widen(elem_type), ratio)
        )
    return ret


def vreg_require_clauses(
    allowed_type_category: str,
    vreg_type: vreg.VRegType,
    ratio: misc.SizeTValue,
    widening: bool | int = False,
    narrowing: bool = False,
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
            constraints.is_compatible_vreg_ratio(vreg.widen(vreg_type), ratio)
        )
    elif widening in [2, 4, 8]:
        ret.append(constraints.widenable_n_type(widening, vreg_type))
        ret.append(
            constraints.is_compatible_vreg_ratio(
                vreg.widen_n(widening, vreg_type), ratio
            )
        )
    elif narrowing:
        ret.append(constraints.narrowable_type(vreg_type))
        ret.append(
            constraints.is_compatible_vreg_ratio(vreg.narrow(vreg_type), ratio)
        )
    return ret


def binary_op(
    inst: str | tuple[str, str],
    allowed_type_category: str,
    arg_variant: str,
    *,
    op_variant: str = "",
) -> Callable[[str], func.Function]:
    assert arg_variant in ["vv", "vx"]
    assert op_variant in [
        "",
        "use_carry",
        "use_and_produce_carry",
        "produce_carry",
        "shifting",
        "comparing",
    ]

    match op_variant:
        case "use_carry" | "use_and_produce_carry" | "produce_carry":
            assert allowed_type_category in ["int"]
        case "shifting":
            assert allowed_type_category in ["int", "signed", "unsigned"]
        case _:
            pass

    if isinstance(inst, str):
        rvv_inst = f"__riscv_{inst}"
    else:
        rvv_inst = inst[1]
        inst = inst[0]

    def ret_type(
        vreg_type: vreg.ParamVRegType, ratio: misc.ParamSizeTValue
    ) -> base.Type:
        match op_variant:
            case "use_and_produce_carry" | "comparing" | "produce_carry":
                return vmask.vmask(ratio)
            case _:
                return vreg_type

    def function_param_list(
        variant: str, vreg_type: vreg.ParamVRegType, ratio: misc.ParamSizeTValue
    ) -> function.FunctionTypedParamList:
        if op_variant == "use_carry":
            assert variant in ["", "tu"]
        if (
            op_variant == "use_and_produce_carry"
            or op_variant == "produce_carry"
        ):
            assert variant == ""

        param_list = function.param_list([vreg_type], ["vs2"])

        if arg_variant == "vv":
            arg2_name = "vs1"
            if op_variant == "shifting":
                arg2_type = vreg.to_unsigned(vreg_type)
            else:
                arg2_type = vreg_type
        else:
            arg2_name = "rs1"
            if op_variant == "shifting":
                arg2_type = misc.size_t
            else:
                arg2_type = vreg.get_elem(vreg_type)
        param_list = param_list + (arg2_type, arg2_name)

        match op_variant:
            case "use_carry" | "use_and_produce_carry":
                param_list = param_list + (vmask.vmask(ratio), "v0")
            case _:
                pass
        param_list = param_list + (vl.vl(ratio), "vl")

        return func.vreg_ratio_extend_param_list(
            vreg_type,
            ratio,
            variant,
            param_list,
            comparing=op_variant == "comparing",
        )

    return func.template_vreg_ratio(
        ret_type,
        inst,
        function_param_list,
        lambda variant, vreg_type, ratio, param_list: (
            "  return "
            + func.apply_function(
                rvv_inst + func.rvv_postfix(variant, overloaded=True),
                param_list,
            )
            + ";"
        ),
        require_clauses=lambda vreg_type, ratio: vreg_require_clauses(
            allowed_type_category, vreg_type, ratio
        ),
    )


def unary_op(
    inst: str, allowed_type_category: str
) -> Callable[[str], func.Function]:

    return func.template_vreg_ratio(
        lambda vreg_type, ratio: vreg_type,
        inst,
        lambda variant, vreg_type, ratio: func.vreg_ratio_param_list(
            vreg_type,
            ratio,
            variant,
            [vreg_type, vl.vl(ratio)],
            ["vs", "vl"],
        ),
        lambda variant, vreg_type, ratio, param_list: (
            "  return "
            + func.apply_function(
                f"__riscv_{inst}" + func.rvv_postfix(variant, overloaded=True),
                param_list,
            )
            + ";"
        ),
        require_clauses=lambda vreg_type, ratio: vreg_require_clauses(
            allowed_type_category, vreg_type, ratio
        ),
    )
