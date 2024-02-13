from typing import Callable, Optional

from codegen import constraints, func, func_obj, guarded, header, main, validate
from codegen.param_list import function, template
from codegen.typing import elem, lmul, misc, vl, vmask, vreg


def vsetvl_decl(
    fname: str, has_size_param: bool
) -> Callable[[str], func.Function]:
    return func.template_ratio(
        vl.vl,
        fname,
        lambda _, __: (
            function.param_list([misc.size_t], ["avl"])
            if has_size_param
            else function.param_list()
        ),
        lambda _, __, ___: None,
    )


def vsetvl_defs(
    fname: str, has_size_param: bool
) -> Callable[[str, misc.LitSizeTValue], func.Function]:
    return func.for_all_ratio(
        vl.vl,
        fname,
        lambda _, __: (
            function.param_list([misc.size_t], ["avl"])
            if has_size_param
            else function.param_list()
        ),
        lambda _, ratio, param_list: f"""  return """
        f"""vl_t<{ratio.value}>{{__riscv_{fname}_e8"""
        f"""{validate.elem_ratio_to_lmul(
            elem.uint8_t, 
            ratio
            ).lmul.short_name}{param_list.forward.cpp_repr}}};""",
        template_param_list=template.TemplateTypeParamList(),
    )


def vreinterpret_op_decl() -> func_obj.CallableClass:
    vreg_type = vreg.param("V")
    template_param_list = template.TemplateTypeParamList(vreg_type)
    return func_obj.CallableClass(
        template_param_list,
        "vreinterpret",
        None,
        requires_clauses=[
            constraints.supported_vreg_or_supported_vmask(vreg_type)
        ],
    )


def vreinterpret_mask_op_def(
    ratio: misc.LitSizeTValue,
) -> Optional[func_obj.CallableClass]:
    vmask_type = vmask.concrete(ratio)
    template_param_list = template.TemplateTypeArgumentList(vmask_type)
    inner_vreg_type = vreg.param("V")
    inner_template_param_list = template.TemplateTypeParamList(inner_vreg_type)
    inner_op = func.Function(
        vmask_type,
        "operator()",
        function.param_list([inner_vreg_type], ["src"]),
        f"  return __riscv_vreinterpret_b{ratio.value}(src);",
        template_param_list=inner_template_param_list,
        require_clauses=[
            constraints.supported_vreg(inner_vreg_type),
            constraints.has_lmul(inner_vreg_type, lmul.lit(0)),
        ],
        modifier="const",
    )
    return func_obj.CallableClass(
        template_param_list,
        "vreinterpret",
        [inner_op],
        feature_guards=guarded.ratio_guard(ratio),
    )


def vreinterpret_op_def(
    elem_type: elem.RawElemType, ratio: misc.LitSizeTValue
) -> Optional[func_obj.CallableClass]:
    if not validate.is_compatible_elem_ratio_may_under_guards(elem_type, ratio):
        return None
    vreg_type = vreg.concrete(elem_type, ratio)
    template_param_list = template.TemplateTypeArgumentList(vreg_type)
    lmul_value = validate.elem_ratio_to_lmul(elem_type, ratio)
    inner_vreg_type = vreg.param("V")
    inner_template_param_list = template.TemplateTypeParamList(inner_vreg_type)

    def inner_op(*additional_require_clauses: str) -> func.Function:
        return func.Function(
            vreg_type,
            "operator()",
            function.param_list([inner_vreg_type], ["src"]),
            f"  return __riscv_vreinterpret_{elem_type.short_name}{lmul_value.lmul.short_name}(src);",
            template_param_list=inner_template_param_list,
            require_clauses=[
                constraints.supported_vreg(inner_vreg_type),
                *additional_require_clauses,
            ],
            modifier="const",
        )

    same_sew_lmul_op = inner_op(
        constraints.not_same_type(vreg.get_elem(inner_vreg_type), elem_type),
        constraints.has_width(
            vreg.get_elem(inner_vreg_type), elem_type.element_width
        ),
        constraints.same_ratio(vreg.get_ratio(inner_vreg_type), ratio),
    )

    different_sew_same_lmul_op = inner_op(
        constraints.doesnt_have_width(
            vreg.get_elem(inner_vreg_type), elem_type.element_width
        ),
        constraints.same_lmul(vreg.get_lmul(inner_vreg_type), lmul_value),
    )
    if isinstance(elem_type, elem.IntType) and lmul_value.lmul.lmul == 0:
        from_mask = func.Function(
            vreg_type,
            "operator()",
            function.param_list([vmask.param("M")], ["src"]),
            f"  return __riscv_vreinterpret_{elem_type.short_name}{lmul_value.lmul.short_name}(src);",
            template_param_list=template.TemplateTypeParamList(
                vmask.param("M")
            ),
            require_clauses=[
                constraints.supported_vmask(vmask.param("M")),
            ],
            modifier="const",
        )
        call_operators = [
            same_sew_lmul_op,
            different_sew_same_lmul_op,
            from_mask,
        ]
    else:
        call_operators = [same_sew_lmul_op, different_sew_same_lmul_op]
    return func_obj.CallableClass(
        template_param_list,
        "vreinterpret",
        call_operators,
        feature_guards=guarded.elem_guard(elem_type, True),
    )


rvv_misc_header = header.Header(
    [
        header.Include("rvv/elem.h"),
        header.Include("rvv/type.h"),
        header.Namespace(
            "rvv",
            [
                "// 9. Miscellaneous Vector Utility Intrinsics",
                "// 9.1. Get vl with specific vtype",
                header.WithVariants(vsetvl_decl("vsetvl", True)),
                header.CrossProduct.variant(
                    vsetvl_defs("vsetvl", True), misc.ALL_RATIO
                ),
                """template <typename E, LMul kLMul>
  requires CompatibleElemLMul<E, kLMul>
RVV_ALWAYS_INLINE vl_t<elem_lmul_to_ratio<E, kLMul>> vsetvl(size_t avl) {
  return vsetvl<elem_lmul_to_ratio<E, kLMul>>(avl);
}""",
                "// 9.2. Get VLMAX with specific vtype",
                header.WithVariants(vsetvl_decl("vsetvlmax", False)),
                header.CrossProduct.variant(
                    vsetvl_defs("vsetvlmax", False), misc.ALL_RATIO
                ),
                """template <typename E, LMul kLMul>
  requires CompatibleElemLMul<E, kLMul>
RVV_ALWAYS_INLINE vl_t<elem_lmul_to_ratio<E, kLMul>> vsetvlmax() {
  return vsetvlmax<elem_lmul_to_ratio<E, kLMul>>();
}""",
                "// 9.3. Reinterpret Cast Conversion Intrinsics",
                vreinterpret_op_decl(),
                header.CrossProduct(
                    vreinterpret_op_def, elem.ALL_ELEM_TYPES, misc.ALL_RATIO
                ),
                header.CrossProduct(
                    vreinterpret_mask_op_def,
                    misc.ALL_RATIO,
                ),
            ],
            allowed_variants={""},
        ),
    ],
)

if __name__ == "__main__":
    main.main(rvv_misc_header)
