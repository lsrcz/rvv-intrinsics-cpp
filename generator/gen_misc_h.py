from typing import Callable
from codegen import header, main, func, validate
from codegen.type import misc, vl, elem
from codegen.param_list import function, template


def vsetvl_decl(
    fname: str, has_size_param: bool
) -> Callable[[str], func.Function]:
    return func.template_ratio(
        lambda ratio: vl.VLType(ratio=ratio),
        fname,
        lambda _, __: function.FunctionTypedParamList(
            *(
                [function.TypedParam(type=misc.SizeTType(), name="avl")]
                if has_size_param
                else []
            )
        ),
        lambda _, __, ___: None,
    )


def vsetvl_defs(
    fname: str, has_size_param: bool
) -> Callable[[str, misc.LitSizeTValue], func.Function]:
    return func.for_all_ratio(
        lambda ratio: vl.VLType(ratio=ratio),
        fname,
        lambda _, __: function.FunctionTypedParamList(
            *(
                [function.TypedParam(type=misc.SizeTType(), name="avl")]
                if has_size_param
                else []
            )
        ),
        lambda _, ratio, param_list: f"""  return """
        f"""vl_t<{ratio.value}>{{__riscv_{fname}_e8"""
        f"""{validate.elem_ratio_to_lmul(
            elem.IntType(width=8, signed=False), 
            ratio
            ).lmul.short_name}{param_list.forward.cpp_repr}}};""",
        template_param_list=template.TemplateTypeParamList(),
    )


rvv_misc_header = header.Header(
    [
        header.Include("rvv/type.h"),
        header.Namespace(
            "rvv",
            [
                header.WithVariants(vsetvl_decl("vsetvl", True)),
                header.CrossProduct.variant(
                    vsetvl_defs("vsetvl", True), misc.ALL_RATIO
                ),
                header.WithVariants(vsetvl_decl("vsetvlmax", False)),
                header.CrossProduct.variant(
                    vsetvl_defs("vsetvlmax", False), misc.ALL_RATIO
                ),
                """
template <typename E, LMul kLMul>
  requires is_compatible_elem_lmul<E, kLMul>
RVV_ALWAYS_INLINE vl_t<elem_lmul_to_ratio<E, kLMul>> vsetvl(size_t avl) {
  return vsetvl<elem_lmul_to_ratio<E, kLMul>>(avl);
}
template <typename E, LMul kLMul>
  requires is_compatible_elem_lmul<E, kLMul>
RVV_ALWAYS_INLINE vl_t<elem_lmul_to_ratio<E, kLMul>> vsetvlmax() {
  return vsetvlmax<elem_lmul_to_ratio<E, kLMul>>();
}
""",
            ],
            allowed_variants={""},
        ),
    ],
)

if __name__ == "__main__":
    main.main(rvv_misc_header)
