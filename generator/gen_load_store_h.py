from typing import Callable, Optional

from codegen import constraints, func, header, main, validate
from codegen.param_list import function
from codegen.typing import elem, lmul, misc, vl, vmask, vreg


def load_arguments(
    inst: str, elem_type: elem.ElemType, ratio: misc.SizeTValue, width: int
) -> function.FunctionTypedParamList:
    assert inst in [
        "vle",
        "vlseg",
        "vleff",
        "vlse",
        "vlsseg",
        "vlox",
        "vlux",
        "vloxseg",
        "vluxseg",
    ]
    param_list = function.param_list(
        [misc.ptr(elem_type, is_const=True)], ["rs1"]
    )

    if inst == "vlse" or inst == "vlsseg":
        param_list = param_list + (misc.ptrdiff_t, "rs2")
    if (
        inst == "vlox"
        or inst == "vlux"
        or inst == "vloxseg"
        or inst == "vluxseg"
    ):
        param_list = param_list + (
            vreg.concrete(elem.IntType(width=width, signed=False), ratio),
            "rs2",
        )
    vl_type = vl.vl(ratio)
    if inst == "vleff":
        param_list = param_list + (
            misc.ptr(vl_type, is_const=False),
            "vl",
        )
    else:
        param_list = param_list + (vl_type, "vl")
    return param_list


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
            vreg.concrete,
            inst,
            lambda _, elem_type, ratio: load_arguments(
                inst, elem_type, ratio, 0
            ),
            lambda _, elem_type, ratio, param_list: non_indexed_base_load_function_body(
                inst, elem_type, ratio, param_list
            ),
        )(variant, elem_type, ratio)

    return inner


def load_store_function_body(
    variant: str,
    inst: str,
    width: int,
    param_list: function.FunctionTypedParamList,
) -> str:
    match inst:
        case (
            "vle" | "vlse" | "vlox" | "vlux" | "vse" | "vsse" | "vsox" | "vsux"
        ):
            if (
                inst == "vlox"
                or inst == "vlux"
                or inst == "vsox"
                or inst == "vsux"
            ):
                width_prefix = "ei"
            else:
                width_prefix = ""
            should_return = inst in ["vle", "vlse", "vlox", "vlux"]
            return (
                ("  return " if should_return else "  ")
                + func.apply_function(
                    f"__riscv_{inst}{width_prefix}{width}"
                    + func.rvv_postfix(variant, overloaded=True),
                    param_list,
                )
                + ";"
            )
        case "vleff":
            return (
                "  return "
                + func.apply_function(
                    f"__riscv_vle{width}ff"
                    + func.rvv_postfix(variant, overloaded=True),
                    param_list[0:-1].forward
                    + function.FunctionArgumentList("&vl->vl", "vl->vl"),
                )
                + ";"
            )
        case _:
            raise ValueError(f"Unknown instruction: {inst}")


def load_store_require_clauses(
    inst: str,
    elem_type: elem.ParamElemType,
    ratio: misc.ParamSizeTValue,
    width: int,
) -> list[str]:
    if inst in ["vlux", "vlox", "vsux", "vsox"]:
        return [
            constraints.compatible_elem_ratio(elem_type, ratio),
        ]
    else:
        return [
            constraints.has_width(elem_type, width),
            constraints.compatible_elem_ratio(elem_type, ratio),
        ]


def load_def(inst: str) -> Callable[[str, int], Optional[func.Function]]:
    return func.template_elem_ratio_for_all_size(
        vreg.concrete,
        inst,
        lambda variant, elem_type, ratio, width: func.elem_ratio_extend_param_list(
            elem_type,
            ratio,
            variant,
            load_arguments(inst, elem_type, ratio, width),
        ),
        lambda variant, elem_type, ratio, width, param_list: load_store_function_body(
            variant, inst, width, param_list
        ),
        require_clauses=lambda elem_type, ratio, width: load_store_require_clauses(
            inst, elem_type, ratio, width
        ),
    )


def store_arguments(
    inst: str, elem_type: elem.ElemType, ratio: misc.SizeTValue, width: int
) -> function.FunctionTypedParamList:
    assert inst in ["vse", "vsse", "vsox", "vsux"]
    param_list = function.param_list(
        [misc.ptr(elem_type, is_const=False)], ["rs1"]
    )
    if inst == "vsse":
        param_list = param_list + (misc.ptrdiff_t, "rs2")
    if inst == "vsox" or inst == "vsux":
        param_list = param_list + (
            vreg.concrete(elem.IntType(width=width, signed=False), ratio),
            "rs2",
        )
    param_list = (
        param_list
        + (vreg.concrete(elem_type, ratio), "vs3")
        + (vl.vl(ratio), "vl")
    )
    return param_list


def store_def(
    inst: str,
) -> Callable[[str, int], Optional[func.Function]]:
    return func.template_elem_ratio_for_all_size(
        lambda _, __: misc.void,
        inst,
        lambda variant, elem_type, ratio, width: func.vreg_ratio_extend_param_list(
            misc.void,
            ratio,
            variant,
            store_arguments(inst, elem_type, ratio, width),
            undisturbed_need_dest_arg=False,
        ),
        lambda variant, _, __, width, param_list: load_store_function_body(
            variant, inst, width, param_list
        ),
        require_clauses=lambda elem_type, ratio, width: load_store_require_clauses(
            inst, elem_type, ratio, width
        ),
    )


def vlm_defs(variant: str, ratio: misc.LitSizeTValue) -> func.Function:
    assert variant == ""
    return func.for_all_ratio(
        vmask.concrete,
        "vlm",
        lambda _, ratio: function.param_list(
            [misc.ptr(elem.uint8_t, is_const=True), vl.vl(ratio)],
            ["rs1", "vl"],
        ),
        lambda _, ratio, param_list: "  return "
        + func.apply_function(f"__riscv_vlm_v_b{ratio}", param_list)
        + ";",
    )(variant, ratio)


rvv_load_store_header = header.Header(
    [
        header.Include("rvv/elem.h"),
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
                            load_def("vle"),
                            elem.ALL_ELEM_SIZES,
                            allowed_variants={"m", "mu", "tu", "tum", "tumu"},
                        ),
                        "// 1.2. Vector Unit-Stride Store Intrinsics",
                        header.CrossProduct.variant(
                            store_def("vse"),
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
                            load_def("vlse"),
                            elem.ALL_ELEM_SIZES,
                            allowed_variants={"m", "mu", "tu", "tum", "tumu"},
                        ),
                        "// 1.5. Vector Strided Store Intrinsics",
                        header.CrossProduct.variant(
                            store_def("vsse"),
                            elem.ALL_ELEM_SIZES,
                            allowed_variants={"", "m"},
                        ),
                        "// 1.6 Vector Indexed Load Intrinsics",
                        header.CrossProduct.variant(
                            load_def("vlox"),
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
                            load_def("vlux"),
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
                            store_def("vsox"),
                            elem.ALL_ELEM_SIZES,
                            allowed_variants={"", "m"},
                        ),
                        header.CrossProduct.variant(
                            store_def("vsux"),
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
                            load_def("vleff"),
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
