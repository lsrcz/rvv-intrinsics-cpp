from typing import Callable, Optional

from codegen import constraints, func, func_obj, guarded, header, main, validate
from codegen.param_list import function, template
from codegen.typing import elem, lmul, misc, vl, vmask, vreg, vtuple


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


def vundefined_decl() -> func.Function:
    type_param = vreg.param("V")
    return func.Function(
        type_param,
        "vundefined",
        function.param_list(),
        function_body=None,
        template_param_list=template.TemplateTypeParamList(type_param),
        require_clauses=[
            constraints.supported_vreg_or_supported_vtuple(type_param)
        ],
    )


def vundefined_vreg_def(
    elem_type: elem.RawElemType, ratio: misc.LitSizeTValue
) -> Optional[func.Function]:
    if not validate.is_compatible_elem_ratio_may_under_guards(elem_type, ratio):
        return None
    vreg_type = vreg.concrete(elem_type, ratio)
    l = validate.elem_ratio_to_lmul(elem_type, ratio)
    template_param_list = template.TemplateTypeArgumentList(vreg_type)
    return func.Function(
        vreg_type,
        "vundefined",
        function.param_list(),
        f"  return __riscv_vundefined_{elem_type.short_name}{l.lmul.short_name}();",
        template_param_list=template_param_list,
        feature_guards=guarded.elem_ratio_guard(elem_type, ratio, True),
    )


def vundefined_vtuple_def(
    elem_type: elem.RawElemType,
    ratio: misc.LitSizeTValue,
    tuple_size: misc.LitSizeTValue,
) -> Optional[func.Function]:
    if not validate.is_compatible_elem_ratio_tuple_size_may_under_guards(
        elem_type, ratio, tuple_size
    ):
        return None
    vtuple_type = vtuple.concrete(elem_type, ratio, tuple_size)
    l = validate.elem_ratio_to_lmul(elem_type, ratio)
    template_param_list = template.TemplateTypeArgumentList(vtuple_type)
    return func.Function(
        vtuple_type,
        "vundefined",
        function.param_list(),
        f"  return __riscv_vundefined_{elem_type.short_name}{l.lmul.short_name}x{tuple_size.cpp_repr}();",
        template_param_list=template_param_list,
        feature_guards=guarded.elem_ratio_guard(elem_type, ratio, True),
    )


def vget_decl() -> func_obj.CallableClass:
    v_small = vreg.param("VSmall")
    idx = misc.param_size_t("kIdx")
    return func_obj.CallableClass(
        template.TemplateTypeParamList(v_small, idx), "vget", None
    )


def vget_def(
    elem_type: elem.RawElemType,
    ratio: misc.LitSizeTValue,
    idx: misc.LitSizeTValue,
) -> Optional[func_obj.CallableClass]:
    v_small = vreg.concrete(elem_type, ratio)
    l = validate.elem_ratio_to_lmul(elem_type, ratio)
    v_large = vreg.param("VLarge")
    if l.lmul.lmul == 3 or (
        not validate.is_compatible_elem_ratio_may_under_guards(elem_type, ratio)
    ):
        return None
    if idx.value < 0:
        return None
    if l.lmul.lmul == 2 and idx.value >= 2:
        return None
    if l.lmul.lmul == 1 and idx.value >= 4:
        return None
    if idx.value >= 8:
        return None
    vget_vec = func.Function(
        v_small,
        "operator()",
        function.param_list([v_large], ["src"]),
        f"  return __riscv_vget_{elem_type.short_name}{l.lmul.short_name}(src, {idx.cpp_repr});",
        template_param_list=template.TemplateTypeParamList(v_large),
        require_clauses=[constraints.valid_index(v_large, v_small, idx)],
        modifier="const",
    )
    return func_obj.CallableClass(
        template.TemplateTypeArgumentList(v_small, idx),
        "vget",
        [vget_vec],
        feature_guards=guarded.elem_ratio_guard(elem_type, ratio, True),
    )


def vlmul_trunc() -> func_obj.CallableClass:
    v_small = vreg.param("VSmall")
    v_large = vreg.param("VLarge")
    return func_obj.CallableClass(
        template.TemplateTypeParamList(v_small),
        "vlmul_trunc",
        [
            func.Function(
                v_small,
                "operator()",
                function.param_list([v_large], ["src"]),
                f"  return rvv::vget<{v_small.cpp_repr}, 0>(src);",
                template_param_list=template.TemplateTypeParamList(v_large),
                require_clauses=[
                    constraints.valid_index(
                        v_large, v_small, misc.lit_size_t(0)
                    ),
                ],
                modifier="const",
            )
        ],
        requires_clauses=[constraints.supported_vreg(v_small)],
    )


def vset_def() -> func_obj.CallableClass:
    v_small = vreg.param("VSmall")
    v_large = vreg.param("VLarge")
    idx = misc.param_size_t("kIdx")
    return func_obj.CallableClass(
        template.TemplateTypeParamList(idx),
        "vset",
        [
            func.Function(
                v_large,
                "operator()",
                function.param_list([v_large, v_small], ["dest", "value"]),
                f"  return __riscv_vset(dest, {idx}, value);",
                template_param_list=template.TemplateTypeParamList(
                    v_large, v_small
                ),
                require_clauses=[
                    constraints.valid_index(
                        v_large,
                        v_small,
                        idx,
                    ),
                ],
                modifier="const",
            )
        ],
    )


def vlmul_ext() -> func_obj.CallableClass:
    v_small = vreg.param("VSmall")
    v_large = vreg.param("VLarge")
    return func_obj.CallableClass(
        template.TemplateTypeParamList(v_large),
        "vlmul_ext",
        [
            func.Function(
                v_large,
                "operator()",
                function.param_list([v_small], ["value"]),
                f"""  auto r = rvv::vundefined<{v_large.cpp_repr}>();
  return rvv::vset<0>(r, value);""",
                template_param_list=template.TemplateTypeParamList(v_small),
                require_clauses=[
                    constraints.valid_index(
                        v_large, v_small, misc.lit_size_t(0)
                    ),
                ],
                modifier="const",
            )
        ],
        requires_clauses=[constraints.supported_vreg(v_large)],
    )


def vcreate_def(has_rvv_1: bool) -> func_obj.CallableClass:
    v_small = vreg.param("VSmall")
    v_large = vreg.param("VLarge")

    def call_operator(n: int) -> func.Function:
        assert n >= 2 and n <= 8

        def insert(i: int) -> str:
            return f"  r = rvv::vset<{i}>(r, v{i});"

        return func.Function(
            v_large,
            "operator()",
            function.param_list([v_small] * n, [f"v{i}" for i in range(n)]),
            f"  auto r = rvv::vundefined<{v_large.cpp_repr}>();"
            + "\n".join(map(insert, range(n)))
            + "\n  return r;",
            template_param_list=template.TemplateTypeParamList(v_small),
            require_clauses=[
                constraints.has_index_bound(
                    v_large, v_small, misc.lit_size_t(n)
                )
            ],
            modifier="const",
        )

    return func_obj.CallableClass(
        template.TemplateTypeParamList(v_large),
        "vcreate",
        [call_operator(i) for i in range(2, 9)],
        requires_clauses=(
            [constraints.supported_vreg(v_large)] if has_rvv_1 else []
        ),
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
                "// 9.4. Vector LMUL Extension Intrinsics",
                "// Generated to the end of this file",
                "// 9.5. Vector LMUL Truncation Intrinsics",
                "// Generated to the end of this file",
                "// 9.6. Vector Initialization Intrinsics",
                """template <typename V>
#if __riscv_v_intrinsic >= 1000000
  requires(SupportedVReg<V> || SupportedVTuple<V>)
#else
  requires SupportedVReg<V>
#endif
RVV_ALWAYS_INLINE V vundefined();
""",
                header.CrossProduct(
                    vundefined_vreg_def, elem.ALL_ELEM_TYPES, misc.ALL_RATIO
                ),
                "#if __riscv_v_intrinsic >= 1000000",
                header.CrossProduct(
                    vundefined_vtuple_def,
                    elem.ALL_ELEM_TYPES,
                    misc.ALL_RATIO,
                    misc.ALL_TUPLE_SIZE,
                ),
                "#endif",
                "// 9.7. Vector Insertion Intrinsics",
                vset_def(),
                "// 9.8. Vector Extraction Intrinsics",
                vget_decl(),
                header.CrossProduct(
                    vget_def,
                    elem.ALL_ELEM_TYPES,
                    misc.ALL_RATIO,
                    misc.ALL_INDEX,
                ),
                "// 9.9. Vector Creation Intrinsics",
                "#if __riscv_v_intrinsic >= 1000000",
                vcreate_def(True),
                "#else",
                vcreate_def(False),
                "#endif",
                "// 9.4. Vector LMUL Extension Intrinsics",
                vlmul_ext(),
                "// 9.5. Vector LMUL Truncation Intrinsics",
                vlmul_trunc(),
            ],
            allowed_variants={""},
        ),
    ],
)

if __name__ == "__main__":
    main.main(rvv_misc_header)
