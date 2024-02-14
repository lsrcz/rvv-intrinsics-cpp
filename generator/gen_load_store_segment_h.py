from typing import Callable, Optional, Sequence

import gen_load_store_h
from codegen import (
    constraints,
    func,
    func_obj,
    guarded,
    header,
    main,
    ops,
    validate,
)
from codegen.param_list import function, template
from codegen.typing import elem, misc, vl, vreg, vtuple


def load_store_function_body(
    variant: str,
    inst: str,
    width: int,
    tuple_size: misc.LitSizeTValue,
    param_list: function.FunctionTypedParamList,
) -> str:
    assert inst in [
        "vlseg",
        "vlsseg",
        "vloxseg",
        "vluxseg",
        "vsseg",
        "vssseg",
        "vsoxseg",
        "vsuxseg",
    ]
    if inst in ["vlseg", "vlsseg", "vsseg", "vssseg"]:
        width_prefix = "e"
    else:
        width_prefix = "ei"
    func_name = (
        f"__riscv_{inst}{tuple_size.cpp_repr}{width_prefix}{width}"
        + func.rvv_postfix(variant, overloaded=True)
    )
    return (
        "  return "
        + func.apply_function(
            func_name,
            param_list,
        )
        + ";"
    )


def load_decl(
    inst: str,
) -> func_obj.CallableClass:
    tuple_size = misc.param_size_t("kTupleSize")
    return func_obj.CallableClass(
        template.TemplateTypeParamList(tuple_size), inst, None
    )


def load_store_require_clauses(
    inst: str,
    elem_type: elem.ParamElemType,
    ratio: misc.ParamSizeTValue,
    tuple_size: misc.LitSizeTValue,
    width: int,
):
    if inst in ["vlseg", "vlsseg", "vsseg", "vssseg"]:
        return [
            constraints.has_width(elem_type, width),
            constraints.compatible_elem_ratio_tuple_size(
                elem_type, ratio, tuple_size
            ),
        ]
    else:
        return [
            constraints.compatible_elem_ratio_tuple_size(
                elem_type, ratio, tuple_size
            ),
        ]


def load_def(
    variant: str, inst: str, tuple_size: misc.LitSizeTValue
) -> func_obj.CallableClass:
    def filter_variant(
        allowed_variants: set[str],
        case: Callable[[str], Sequence[func.Function]],
    ) -> Callable[[str], Sequence[func.Function]]:
        def f(variant: str) -> Sequence[func.Function]:
            if variant in allowed_variants:
                return case(variant)
            return []

        return f

    def base_case(_: str) -> Sequence[func.Function]:
        ret: list[func.Function] = []
        for elem_type in elem.ALL_ELEM_TYPES:
            for ratio in misc.ALL_RATIO:
                if validate.is_compatible_elem_ratio_tuple_size_may_under_guards(
                    elem_type, ratio, tuple_size
                ):
                    param_list = gen_load_store_h.load_arguments(
                        inst, elem_type, ratio, 0
                    )
                    l = validate.elem_ratio_to_lmul(
                        elem_type=elem_type, ratio=ratio
                    )
                    ret.append(
                        func.Function(
                            vtuple.concrete(elem_type, ratio, tuple_size),
                            "operator()",
                            param_list,
                            "  return "
                            + func.apply_function(
                                (
                                    f"__riscv_{inst}{tuple_size.cpp_repr}e{elem_type.element_width}_v_"
                                    + f"{elem_type.short_name}{l.lmul.short_name}x{tuple_size.cpp_repr}"
                                ),
                                param_list,
                            )
                            + ";",
                            feature_guards=guarded.elem_ratio_guard(
                                elem_type, ratio, True
                            ),
                            modifier="const",
                        )
                    )
        return ret

    def variant_case(variant: str) -> Sequence[func.Function]:
        ret: list[func.Function] = []
        for elem_size in elem.ALL_ELEM_SIZES:
            f = func.template_elem_ratio_for_all_size(
                lambda elem_type, ratio: vtuple.concrete(
                    elem_type, ratio, tuple_size
                ),
                "operator()",
                lambda variant, elem_type, ratio, width: func.vreg_ratio_extend_param_list(
                    vtuple.concrete(elem_type, ratio, tuple_size),
                    ratio,
                    variant,
                    gen_load_store_h.load_arguments(
                        inst, elem_type, ratio, width
                    ),
                ),
                lambda variant, _, __, width, param_list: load_store_function_body(
                    variant, inst, width, tuple_size, param_list
                ),
                require_clauses=lambda elem_type, ratio, width: load_store_require_clauses(
                    inst, elem_type, ratio, tuple_size, width
                ),
                modifier="const",
            )(variant, elem_size)
            if f is not None:
                ret.append(f)
        return ret

    if inst == "vlseg" or inst == "vlsseg":
        call_operators: list[Callable[[str], Sequence[func.Function]]] = [
            filter_variant({""}, base_case),
            filter_variant({"m", "tu", "tum", "tumu", "mu"}, variant_case),
        ]
    else:
        call_operators = [variant_case]
    return ops.callable_class_with_variant(
        template.TemplateTypeArgumentList(tuple_size), inst, call_operators
    )(variant)


def store_arguments(
    inst: str,
    elem_type: elem.ElemType,
    ratio: misc.SizeTValue,
    tuple_size: misc.LitSizeTValue,
    width: int,
) -> function.FunctionTypedParamList:
    assert inst in [
        "vsseg",
        "vssseg",
        "vsoxseg",
        "vsuxseg",
    ]
    param_list = function.param_list(
        [misc.ptr(elem_type, is_const=False)], ["rs1"]
    )
    if inst == "vssseg":
        param_list = param_list + (misc.ptrdiff_t, "rs2")
    if inst in ["vsoxseg", "vsuxseg"]:
        param_list = param_list + (
            vreg.concrete(elem.IntType(width=width, signed=False), ratio),
            "rs2",
        )
    param_list = (
        param_list
        + (vtuple.concrete(elem_type, ratio, tuple_size), "vs3")
        + (vl.vl(ratio), "vl")
    )
    return param_list


def store_def(
    variant: str, inst: str, tuple_size: misc.LitSizeTValue, elem_size: int
) -> Optional[func.Function]:
    return func.template_elem_ratio_for_all_size(
        lambda _, __: misc.void,
        inst,
        lambda variant, elem_type, ratio, width: func.vreg_ratio_extend_param_list(
            misc.void,
            ratio,
            variant,
            store_arguments(inst, elem_type, ratio, tuple_size, width),
            undisturbed_need_dest_arg=False,
        ),
        lambda variant, _, __, width, param_list: load_store_function_body(
            variant, inst, width, tuple_size, param_list
        ),
        require_clauses=lambda elem_type, ratio, width: load_store_require_clauses(
            inst, elem_type, ratio, tuple_size, width
        ),
    )(variant, elem_size)


rvv_load_store_segment_header = header.Header(
    [
        header.Include("rvv/elem.h"),
        header.Include("rvv/type.h"),
        header.Namespace(
            "rvv",
            [
                header.VariantNamespace(
                    [
                        "// 2. Vector Loads and Stores Segment Intrinsics",
                        "// 2.1. Vector Unit-Stride Segment Load Intrinsics",
                        load_decl("vlseg"),
                        header.CrossProduct.variant(
                            load_def,
                            ["vlseg"],
                            misc.ALL_TUPLE_SIZE,
                            allowed_variants={"", "tu", "mu", "tumu"},
                        ),
                        "// 2.2. Vector Unit-Stride Segment Store Intrinsics",
                        header.CrossProduct.variant(
                            store_def,
                            ["vsseg"],
                            misc.ALL_TUPLE_SIZE,
                            elem.ALL_ELEM_SIZES,
                            allowed_variants={"", "m"},
                        ),
                        "// 2.3. Vector Strided Segment Load Intrinsics",
                        load_decl("vlsseg"),
                        header.CrossProduct.variant(
                            load_def,
                            ["vlsseg"],
                            misc.ALL_TUPLE_SIZE,
                            allowed_variants={"", "tu", "mu", "tumu"},
                        ),
                        "// 2.4. Vector Strided Segment Store Intrinsics",
                        header.CrossProduct.variant(
                            store_def,
                            ["vssseg"],
                            misc.ALL_TUPLE_SIZE,
                            elem.ALL_ELEM_SIZES,
                            allowed_variants={"", "m"},
                        ),
                        "// 2.5. Vector Indexed Segment Load Intrinsics",
                        load_decl("vloxseg"),
                        load_decl("vluxseg"),
                        header.CrossProduct.variant(
                            load_def,
                            ["vloxseg", "vluxseg"],
                            misc.ALL_TUPLE_SIZE,
                            allowed_variants={"", "tu", "mu", "tumu"},
                        ),
                        "// 2.6. Vector Indexed Segment Store Intrinsics",
                        header.CrossProduct.variant(
                            store_def,
                            ["vsoxseg", "vsuxseg"],
                            misc.ALL_TUPLE_SIZE,
                            elem.ALL_ELEM_SIZES,
                            allowed_variants={"", "m"},
                        ),
                    ]
                )
            ],
        ),
    ]
)

if __name__ == "__main__":
    main.main(rvv_load_store_segment_header)
