from typing import Callable, Sequence
from codegen import constraints, func, guarded, header, main, validate, func_obj
from codegen import ops
from codegen.param_list import function, template
from codegen.typing import elem, misc, vtuple
import gen_load_store_h


def load_function_body(
    variant: str,
    inst: str,
    width: int,
    tuple_size: misc.LitSizeTValue,
    param_list: function.FunctionTypedParamList,
) -> str:
    func_name = (
        f"__riscv_{inst}{tuple_size.cpp_repr}e{width}"
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
                lambda variant, _, __, width, param_list: load_function_body(
                    variant, inst, width, tuple_size, param_list
                ),
                require_clauses=lambda elem_type, ratio, width: [
                    constraints.has_width(elem_type, width),
                    constraints.compatible_elem_ratio_tuple_size(
                        elem_type, ratio, tuple_size
                    ),
                ],
                modifier="const",
            )(variant, elem_size)
            if f is not None:
                ret.append(f)
        return ret

    call_operators: list[Callable[[str], Sequence[func.Function]]] = [
        filter_variant({""}, base_case),
        filter_variant({"m", "tu", "tum", "tumu", "mu"}, variant_case),
    ]
    return ops.callable_class_with_variant(
        template.TemplateTypeArgumentList(tuple_size), inst, call_operators
    )(variant)


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
                        "// 2.3. Vector Strided Segment Load Intrinsics",
                        load_decl("vlsseg"),
                        header.CrossProduct.variant(
                            load_def,
                            ["vlsseg"],
                            misc.ALL_TUPLE_SIZE,
                            allowed_variants={"", "tu", "mu", "tumu"},
                        ),
                    ]
                )
            ],
        ),
    ]
)

if __name__ == "__main__":
    main.main(rvv_load_store_segment_header)
