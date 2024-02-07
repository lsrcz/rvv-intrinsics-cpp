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
    elif narrowing:
        ret.append(constraints.narrowable_type(vreg_type))
        ret.append(
            constraints.is_compatible_vreg_ratio(
                vreg.NarrowVRegType(base_type=vreg_type), ratio
            )
        )
    return ret


def binary_op_template_on_elem(
    inst: str | tuple[str, str],
    allowed_type_category: str,
    *,
    op_variant: str = "",
) -> Callable[[str], func.Function]:
    assert op_variant in ["", "use_carry", "use_and_produce_carry", "comparing"]
    match op_variant:
        case "use_carry" | "use_and_produce_carry":
            assert allowed_type_category in ["int", "signed", "unsigned"]
        case _:
            pass
    if isinstance(inst, str):
        rvv_inst = f"__riscv_{inst}"
    else:
        rvv_inst = inst[1]
        inst = inst[0]

    def ret_type(
        elem_type: elem.ParamElemType, ratio: misc.ParamSizeTValue
    ) -> base.Type:
        match op_variant:
            case "use_and_produce_carry" | "comparing":
                return vmask.VMaskType(ratio=ratio)
            case _:
                return vreg.ConcreteVRegType(elem_type=elem_type, ratio=ratio)

    def function_param_list(
        variant: str, elem_type: elem.ParamElemType, ratio: misc.ParamSizeTValue
    ) -> function.FunctionTypedParamList:
        ret: list[function.TypedParam] = []
        ret.append(
            function.TypedParam(
                type=vreg.ConcreteVRegType(elem_type=elem_type, ratio=ratio),
                name="vs2",
            )
        )
        ret.append(
            function.TypedParam(
                type=elem_type,
                name="rs1",
            )
        )
        match op_variant:
            case "use_carry" | "use_and_produce_carry":
                ret.append(
                    function.TypedParam(
                        type=vmask.VMaskType(ratio=ratio), name="v0"
                    )
                )
            case _:
                pass
        ret.append(
            function.TypedParam(type=vl.VLType(ratio=ratio), name="vl"),
        )

        return func.elem_ratio_extend_param_list(
            elem_type,
            ratio,
            variant,
            function.FunctionTypedParamList(*ret),
            comparing=op_variant == "comparing",
        )

    return func.template_elem_ratio(
        ret_type,
        inst,
        function_param_list,
        lambda variant, elem_type, ratio, param_list: (
            "  return "
            + func.apply_function(
                rvv_inst + func.rv_postfix(variant, overloaded=True),
                param_list,
            )
            + ";"
        ),
        require_clauses=lambda elem_type, ratio: elem_require_clauses(
            allowed_type_category, elem_type, ratio
        ),
    )


def binary_op_template_on_vreg(
    inst: str | tuple[str, str],
    allowed_type_category: str,
    *,
    op_variant: str = "",
) -> Callable[[str], func.Function]:
    assert op_variant in [
        "",
        "use_carry",
        "use_and_produce_carry",
        "shifting",
        "shifting_scalar",
        "comparing",
    ]

    match op_variant:
        case (
            "use_carry"
            | "use_and_produce_carry"
            | "shifting"
            | "shifting_scalar"
        ):
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
            case "use_and_produce_carry" | "comparing":
                return vmask.VMaskType(ratio=ratio)
            case _:
                return vreg_type

    def function_param_list(
        variant: str, vreg_type: vreg.ParamVRegType, ratio: misc.ParamSizeTValue
    ) -> function.FunctionTypedParamList:
        ret: list[function.TypedParam] = []
        ret.append(
            function.TypedParam(
                type=vreg_type,
                name="vs2",
            )
        )

        match op_variant:
            case "shifting":
                ret.append(
                    function.TypedParam(
                        type=vreg.ToUnsignedVRegType(base_type=vreg_type),
                        name="vs1",
                    )
                )
            case "shifting_scalar":
                ret.append(
                    function.TypedParam(
                        type=misc.SizeTType(),
                        name="rs1",
                    )
                )
            case _:
                ret.append(
                    function.TypedParam(
                        type=vreg_type,
                        name="vs1",
                    )
                )

        match op_variant:
            case "use_carry" | "use_and_produce_carry":
                ret.append(
                    function.TypedParam(
                        type=vmask.VMaskType(ratio=ratio), name="v0"
                    )
                )
            case _:
                pass
        ret.append(
            function.TypedParam(type=vl.VLType(ratio=ratio), name="vl"),
        )

        return func.vreg_ratio_extend_param_list(
            vreg_type,
            ratio,
            variant,
            function.FunctionTypedParamList(*ret),
            comparing=op_variant == "comparing",
        )

    return func.template_vreg_ratio(
        ret_type,
        inst,
        function_param_list,
        lambda variant, vreg_type, ratio, param_list: (
            "  return "
            + func.apply_function(
                rvv_inst + func.rv_postfix(variant, overloaded=True),
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
