from typing import Callable, Sequence
from codegen import (
    func,
    guarded,
    header,
    main,
    ops,
    constraints,
    func_obj,
    validate,
)
from codegen.typing import base, elem, misc, vmask, vl, vreg
from codegen.param_list import function, template


def parse_type(ratio: misc.SizeTValue, c: str) -> base.Type:
    match c:
        case "m":
            return vmask.vmask(ratio)
        case "uint":
            return misc.c_unsigned_int_t
        case "int":
            return misc.c_int_t
        case _:
            raise ValueError(f"Unknown type specifier: {c}")


def parse_type_list(
    ratio: misc.SizeTValue,
    arg_type_spec: list[str],
) -> function.FunctionTypedParamList:
    types = [parse_type(ratio, c) for c in arg_type_spec]

    return function.param_list(types, ["vs2", "vs1"][0 : len(types)])


def mask_op(
    inst: str,
    ret_type_spec: str,
    arg_type_spec: list[str],
) -> Callable[[str], func.Function]:
    rvv_inst = f"__riscv_{inst}"

    def ret_type(ratio: misc.SizeTValue) -> base.Type:
        return parse_type(ratio, ret_type_spec)

    def function_param_list(
        variant: str, ratio: misc.SizeTValue
    ) -> function.FunctionTypedParamList:
        base_list = parse_type_list(ratio, arg_type_spec) + (vl.vl(ratio), "vl")
        dest_type = ret_type(ratio)
        return func.vreg_ratio_extend_param_list(
            dest_type, ratio, variant, base_list
        )

    return func.template_ratio(
        ret_type,
        inst,
        function_param_list,
        lambda variant, ratio, param_list: "  return "
        + func.apply_function(
            rvv_inst + func.rvv_postfix(variant, overloaded=True),
            param_list,
        )
        + ";",
    )


def mask_nullary_op(
    inst: str,
) -> Callable[[str, misc.LitSizeTValue], func.Function]:
    return func.for_all_ratio(
        vmask.vmask,
        inst,
        lambda variant, ratio: function.param_list([vl.vl(ratio)], ["vl"]),
        lambda variant, ratio, param_list: "  return "
        + func.apply_function(f"__riscv_{inst}_m_b{ratio}", param_list)
        + ";",
    )


def mask_nullary_part(
    inst: str,
    ratio: misc.LitSizeTValue,
) -> header.HeaderPart:
    return header.Verbatim(
        mask_nullary_op(inst)("", ratio), allowed_variants={""}
    )


def mask_unary_op(inst: str) -> Callable[[str], func.Function]:
    return mask_op(inst, "m", ["m"])


def mask_bin_op(inst: str) -> Callable[[str], func.Function]:
    return mask_op(inst, "m", ["m", "m"])


def mask_vec_ret_op_decl(inst: str) -> Callable[[str], func_obj.CallableClass]:
    elem_type = elem.param("E")
    template_param_list = template.TemplateTypeParamList(elem_type)
    requires_clauses = [constraints.supported_unsigned_element(elem_type)]

    return ops.callable_class_with_variant(
        template_param_list,
        inst,
        None,
        requires_clauses=requires_clauses,
    )


def mask_iota_op(
    elem_type: elem.RawElemType,
) -> Callable[[str], func_obj.CallableClass]:
    template_param_list = template.TemplateTypeArgumentList(elem_type)

    def some_operator(
        ratio: misc.LitSizeTValue,
    ) -> Callable[[str], func.Function]:
        def inner(variant: str) -> func.Function:
            return func.for_all_ratio(
                lambda ratio: vreg.concrete(elem_type, ratio),
                "operator()",
                lambda variant, ratio: func.vreg_ratio_param_list(
                    vreg.concrete(elem_type, ratio),
                    ratio,
                    variant,
                    [vmask.vmask(ratio), vl.vl(ratio)],
                    ["vs2", "vl"],
                ),
                lambda variant, ratio, param_list: "  return "
                + func.apply_function(
                    f"__riscv_viota_m_{elem_type.short_name}"
                    + f"{validate.elem_ratio_to_lmul(elem_type, ratio).lmul.short_name}"
                    + func.rvv_postfix(variant, overloaded=False),
                    param_list,
                )
                + ";",
                feature_guards=lambda ratio: guarded.elem_ratio_guard(
                    elem_type, ratio, True
                ),
                modifier="const",
            )(variant, ratio)

        return inner

    call_operators: list[Callable[[str], func.Function]] = []
    for ratio in misc.ALL_RATIO:
        if validate.is_compatible_elem_ratio_may_under_guards(elem_type, ratio):
            call_operators.append(some_operator(ratio))

    return ops.callable_class_with_variant(
        template_param_list,
        "viota",
        call_operators,
        requires_clauses=[],
    )


def mask_iota_op_header_part(
    elem_type: elem.RawElemType,
) -> header.HeaderPart:
    return header.WithVariants(mask_iota_op(elem_type))


rvv_mask_h = header.Header(
    [
        header.Include("rvv/elem.h"),
        header.Include("rvv/conversion.h"),
        header.Include("rvv/type.h"),
        header.Namespace(
            "rvv",
            [
                header.VariantNamespace(
                    [
                        "// 7. Vector Mask operations",
                        "// 7.1. Vector Mask-Register Logical",
                        header.CrossProduct(
                            ops.inferred_type_part,
                            [
                                "vmand",
                                "vmnand",
                                "vmandn",
                                "vmxor",
                                "vmor",
                                "vmnor",
                                "vmorn",
                                "vmxnor",
                            ],
                            [mask_bin_op],
                            allowed_variants={""},
                        ),
                        header.CrossProduct(
                            ops.inferred_type_part,
                            ["vmmv", "vmnot"],
                            [mask_unary_op],
                            allowed_variants={""},
                        ),
                        header.CrossProduct(
                            mask_nullary_part,
                            ["vmclr", "vmset"],
                            misc.ALL_RATIO,
                            allowed_variants={""},
                        ),
                        "// 7.2. Vector count population in mask vcpop.m",
                        header.WithVariants(
                            mask_op("vcpop", "uint", ["m"]),
                            allowed_variants={"", "m"},
                        ),
                        "// 7.3. vfirst find-first-set mask bit",
                        header.WithVariants(
                            mask_op("vfirst", "int", ["m"]),
                            allowed_variants={"", "m"},
                        ),
                        "// 7.4. vmsbf.m set-before-first mask bit",
                        header.WithVariants(
                            mask_op("vmsbf", "m", ["m"]),
                            allowed_variants={"", "m", "mu"},
                        ),
                        "// 7.5. vmsif.m set-including-first mask bit",
                        header.WithVariants(
                            mask_op("vmsif", "m", ["m"]),
                            allowed_variants={"", "m", "mu"},
                        ),
                        "// 7.6. vmsof.m set-only-first mask bit",
                        header.WithVariants(
                            mask_op("vmsof", "m", ["m"]),
                            allowed_variants={"", "m", "mu"},
                        ),
                        "// 7.7. Vector Iota Intrinsics",
                        header.WithVariants(
                            mask_vec_ret_op_decl("viota"),
                            allowed_variants={"", "mu", "tu", "tumu"},
                        ),
                        header.CrossProduct(
                            mask_iota_op_header_part,
                            elem.ALL_UNSIGNED_INT_TYPES,
                            allowed_variants={"", "mu", "tu", "tumu"},
                        ),
                    ]
                )
            ],
        ),
    ]
)

if __name__ == "__main__":
    main.main(rvv_mask_h)
