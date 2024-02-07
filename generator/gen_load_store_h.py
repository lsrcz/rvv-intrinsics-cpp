from typing import Callable, Optional

from codegen import constraints, func, header, main, validate
from codegen.param_list import function
from codegen.typing import elem, lmul, misc, vl, vmask, vreg


def non_indexed_ret_type(
    elem_type: elem.ElemType, ratio: misc.SizeTValue
) -> vreg.ConcreteVRegType:
    return vreg.ConcreteVRegType(elem_type=elem_type, ratio=ratio)


def non_indexed_load_arguments(
    inst: str, elem_type: elem.ElemType, ratio: misc.SizeTValue
) -> function.FunctionTypedParamList:
    assert inst in ["vle", "vleff", "vlse"]
    ret = function.FunctionTypedParamList(
        function.TypedParam(
            type=misc.PtrType(base_type=elem_type, is_const=True), name="rs1"
        )
    )
    if inst == "vlse":
        ret += function.FunctionTypedParamList(
            function.TypedParam(type=misc.PtrdiffTType(), name="rs2")
        )
    vl_type = vl.VLType(ratio=ratio)
    if inst == "vleff":
        ret += function.FunctionTypedParamList(
            function.TypedParam(
                type=misc.PtrType(base_type=vl_type, is_const=False), name="vl"
            )
        )
    else:
        ret += function.FunctionTypedParamList(
            function.TypedParam(type=vl_type, name="vl")
        )
    return ret


def non_indexed_base_load_function_body(
    inst: str,
    elem_type: elem.RawElemType,
    ratio: misc.LitSizeTValue,
    param_list: function.FunctionTypedParamList,
) -> str:
    l: lmul.LitLMulValue = validate.elem_ratio_to_lmul(
        elem_type=elem_type, ratio=ratio
    )
    match inst:
        case "vle" | "vlse":
            return (
                "  return "
                + func.apply_function(
                    f"__riscv_{inst}{elem_type.element_width}_v_"
                    + f"{elem_type.short_name}{l.lmul.short_name}",
                    param_list,
                )
                + ";"
            )
        case "vleff":
            return (
                "  return "
                + func.apply_function(
                    f"__riscv_vle{elem_type.element_width}ff_v_"
                    + f"{elem_type.short_name}{l.lmul.short_name}",
                    param_list[0:-1].forward
                    + function.FunctionArgumentList("&vl->vl", "vl->vl"),
                )
                + ";"
            )
        case _:
            raise ValueError(f"Unknown instruction: {inst}")


def non_indexed_load_base_def_template(
    inst: str,
) -> Callable[
    [str, elem.RawElemType, misc.LitSizeTValue], Optional[func.Function]
]:
    def inner(
        variant: str, elem_type: elem.RawElemType, ratio: misc.LitSizeTValue
    ) -> Optional[func.Function]:
        assert variant == ""
        return func.for_all_elem_ratio(
            non_indexed_ret_type,
            inst,
            lambda _, elem_type, ratio: non_indexed_load_arguments(
                inst, elem_type, ratio
            ),
            lambda _, elem_type, ratio, param_list: non_indexed_base_load_function_body(
                inst, elem_type, ratio, param_list
            ),
        )(variant, elem_type, ratio)

    return inner


def non_indexed_variant_load_function_body(
    variant: str,
    inst: str,
    width: int,
    param_list: function.FunctionTypedParamList,
) -> str:
    match inst:
        case "vle" | "vlse":
            return (
                "  return "
                + func.apply_function(
                    f"__riscv_{inst}{width}"
                    + func.rv_postfix(variant, overloaded=True),
                    param_list,
                )
                + ";"
            )
        case "vleff":
            return (
                "  return "
                + func.apply_function(
                    f"__riscv_vle{width}ff"
                    + func.rv_postfix(variant, overloaded=True),
                    param_list[0:-1].forward
                    + function.FunctionArgumentList("&vl->vl", "vl->vl"),
                )
                + ";"
            )
        case _:
            raise ValueError(f"Unknown instruction: {inst}")


def non_indexed_load_variant_def_template(
    inst: str,
) -> Callable[[str, int], Optional[func.Function]]:
    return func.template_elem_ratio_for_all_size(
        non_indexed_ret_type,
        inst,
        lambda variant, elem_type, ratio, _: func.elem_ratio_extend_param_list(
            elem_type,
            ratio,
            variant,
            non_indexed_load_arguments(inst, elem_type, ratio),
        ),
        lambda variant, _, __, width, param_list: non_indexed_variant_load_function_body(
            variant, inst, width, param_list
        ),
    )


def non_indexed_store_arguments(
    inst: str, elem_type: elem.ElemType, ratio: misc.SizeTValue
) -> function.FunctionTypedParamList:
    assert inst in ["vse", "vsse"]
    ret = function.FunctionTypedParamList(
        function.TypedParam(
            type=misc.PtrType(base_type=elem_type, is_const=False), name="rs1"
        )
    )
    if inst == "vsse":
        ret += function.FunctionTypedParamList(
            function.TypedParam(type=misc.PtrdiffTType(), name="rs2")
        )
    ret += function.FunctionTypedParamList(
        function.TypedParam(
            type=vreg.ConcreteVRegType(elem_type=elem_type, ratio=ratio),
            name="vs3",
        ),
        function.TypedParam(type=vl.VLType(ratio=ratio), name="vl"),
    )
    return ret


def non_indexed_store_function_body(
    variant: str,
    inst: str,
    width: int,
    param_list: function.FunctionTypedParamList,
) -> str:
    return (
        func.apply_function(
            f"  __riscv_{inst}{width}"
            + func.rv_postfix(variant, overloaded=True),
            param_list,
        )
        + ";"
    )


def non_indexed_store_def_template(
    inst: str,
) -> Callable[[str, int], Optional[func.Function]]:
    return func.template_elem_ratio_for_all_size(
        lambda _, __: misc.VoidType(),
        inst,
        lambda variant, elem_type, ratio, _: func.elem_ratio_extend_param_list(
            elem_type,
            ratio,
            variant,
            non_indexed_store_arguments(inst, elem_type, ratio),
            undisturbed_need_dest_arg=False,
        ),
        lambda variant, _, __, width, param_list: non_indexed_store_function_body(
            variant, inst, width, param_list
        ),
    )


def vlm_defs(variant: str, ratio: misc.LitSizeTValue) -> func.Function:
    assert variant == ""
    return func.for_all_ratio(
        lambda ratio: vmask.VMaskType(ratio=ratio),
        "vlm",
        lambda _, ratio: function.FunctionTypedParamList(
            function.TypedParam(
                type=misc.PtrType(
                    base_type=elem.IntType(width=8, signed=False), is_const=True
                ),
                name="rs1",
            ),
            function.TypedParam(type=vl.VLType(ratio=ratio), name="vl"),
        ),
        lambda _, ratio, param_list: "  return "
        + func.apply_function(f"__riscv_vlm_v_b{ratio}", param_list)
        + ";",
    )(variant, ratio)


def vlxei_defs(inst: str) -> Callable[[str, int], Optional[func.Function]]:
    return func.template_elem_ratio_for_all_size(
        lambda elem_type, ratio: vreg.ConcreteVRegType(
            elem_type=elem_type, ratio=ratio
        ),
        inst,
        lambda variant, elem_type, ratio, width: func.elem_ratio_extend_param_list(
            elem_type,
            ratio,
            variant,
            function.FunctionTypedParamList(
                function.TypedParam(
                    type=misc.PtrType(base_type=elem_type, is_const=True),
                    name="rs1",
                ),
                function.TypedParam(
                    type=vreg.ConcreteVRegType(
                        elem_type=elem.IntType(width=width, signed=False),
                        ratio=ratio,
                    ),
                    name="rs2",
                ),
                function.TypedParam(type=vl.VLType(ratio=ratio), name="vl"),
            ),
        ),
        lambda variant, elem_type, ratio, width, param_list: (
            "  return "
            + func.apply_function(
                f"__riscv_{inst}{width}{func.rv_postfix(variant, overloaded=True)}",
                param_list,
            )
            + ";"
        ),
        require_clauses=lambda elem_type, ratio, width: [
            constraints.is_compatible_elem_ratio(elem_type, ratio),
        ],
    )


def vsxei_defs(inst: str) -> Callable[[str, int], Optional[func.Function]]:
    return func.template_elem_ratio_for_all_size(
        lambda _, __: misc.VoidType(),
        inst,
        lambda variant, elem_type, ratio, width: func.elem_ratio_extend_param_list(
            elem_type,
            ratio,
            variant,
            function.FunctionTypedParamList(
                function.TypedParam(
                    type=misc.PtrType(base_type=elem_type, is_const=False),
                    name="rs1",
                ),
                function.TypedParam(
                    type=vreg.ConcreteVRegType(
                        elem_type=elem.IntType(width=width, signed=False),
                        ratio=ratio,
                    ),
                    name="rs2",
                ),
                function.TypedParam(
                    type=vreg.ConcreteVRegType(
                        elem_type=elem_type, ratio=ratio
                    ),
                    name="vs3",
                ),
                function.TypedParam(type=vl.VLType(ratio=ratio), name="vl"),
            ),
            undisturbed_need_dest_arg=False,
        ),
        lambda variant, elem_type, ratio, width, param_list: (
            func.apply_function(
                f"  __riscv_{inst}{width}{func.rv_postfix(variant, overloaded=True)}",
                param_list,
            )
            + ";"
        ),
        require_clauses=lambda elem_type, ratio, width: [
            constraints.is_compatible_elem_ratio(elem_type, ratio),
        ],
    )


rvv_load_store_header = header.Header(
    [
        header.Include("rvv/type.h"),
        header.Namespace(
            "rvv",
            [
                header.VariantNamespace(
                    [
                        "// 1. Vector Loads and Stores Intrinsics",
                        "// 1.1. Vector Unit-Stride Load Intrinsics",
                        header.CrossProduct.variant(
                            non_indexed_load_base_def_template("vle"),
                            elem.ALL_ELEM_TYPES,
                            misc.ALL_RATIO,
                            allowed_variants={""},
                        ),
                        header.CrossProduct.variant(
                            non_indexed_load_variant_def_template("vle"),
                            elem.ALL_ELEM_SIZES,
                            allowed_variants={"m", "mu", "tu", "tum", "tumu"},
                        ),
                        "// 1.2. Vector Unit-Stride Store Intrinsics",
                        header.CrossProduct.variant(
                            non_indexed_store_def_template("vse"),
                            elem.ALL_ELEM_SIZES,
                            allowed_variants={"", "m"},
                        ),
                        "// 1.3. Vector Mask Load/Store Intrinsics",
                        header.CrossProduct.variant(
                            vlm_defs, misc.ALL_RATIO, allowed_variants={""}
                        ),
                        header.Verbatim(
                            """template <size_t kRatio>
RVV_ALWAYS_INLINE
vmask_t<kRatio> vsm(uint8_t *rs1, vmask_t<kRatio> vs3, vl_t<kRatio> vl) {
  __riscv_vsm(rs1, vs3, vl);
}""",
                            allowed_variants={""},
                        ),
                        "// 1.4. Vector Strided Load Intrinsics",
                        header.CrossProduct.variant(
                            non_indexed_load_base_def_template("vlse"),
                            elem.ALL_ELEM_TYPES,
                            misc.ALL_RATIO,
                            allowed_variants={""},
                        ),
                        header.CrossProduct.variant(
                            non_indexed_load_variant_def_template("vlse"),
                            elem.ALL_ELEM_SIZES,
                            allowed_variants={"m", "mu", "tu", "tum", "tumu"},
                        ),
                        "// 1.5. Vector Strided Store Intrinsics",
                        header.CrossProduct.variant(
                            non_indexed_store_def_template("vsse"),
                            elem.ALL_ELEM_SIZES,
                            allowed_variants={"", "m"},
                        ),
                        "// 1.6 Vector Indexed Load Intrinsics",
                        header.CrossProduct.variant(
                            vlxei_defs("vloxei"),
                            elem.ALL_ELEM_SIZES,
                            allowed_variants={
                                "",
                                "m",
                                "mu",
                                "tu",
                                "tum",
                                "tumu",
                            },
                        ),
                        header.CrossProduct.variant(
                            vlxei_defs("vluxei"),
                            elem.ALL_ELEM_SIZES,
                            allowed_variants={
                                "",
                                "m",
                                "mu",
                                "tu",
                                "tum",
                                "tumu",
                            },
                        ),
                        "// 1.7 Vector Indexed Store Intrinsics",
                        header.CrossProduct.variant(
                            vsxei_defs("vsoxei"),
                            elem.ALL_ELEM_SIZES,
                            allowed_variants={"", "m"},
                        ),
                        header.CrossProduct.variant(
                            vsxei_defs("vsuxei"),
                            elem.ALL_ELEM_SIZES,
                            allowed_variants={"", "m"},
                        ),
                        "// 1.8. Unit-stride Fault-Only-First Loads Intrinsics",
                        header.CrossProduct.variant(
                            non_indexed_load_base_def_template("vleff"),
                            elem.ALL_ELEM_TYPES,
                            misc.ALL_RATIO,
                            allowed_variants={""},
                        ),
                        header.CrossProduct.variant(
                            non_indexed_load_variant_def_template("vleff"),
                            elem.ALL_ELEM_SIZES,
                            allowed_variants={"m", "mu", "tu", "tum", "tumu"},
                        ),
                    ]
                ),
            ],
        ),
    ]
)

if __name__ == "__main__":
    main.main(rvv_load_store_header)
