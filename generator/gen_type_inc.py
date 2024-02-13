from typing import Optional

from codegen import cpp_repr, guarded, header, main, validate
from codegen.typing import elem, lmul, misc


def vreg_specialization_def(
    elem_type: elem.RawElemType, ratio: misc.LitSizeTValue
) -> Optional[cpp_repr.HasCppRepr]:
    if not validate.is_compatible_elem_ratio_may_under_guards(elem_type, ratio):
        return None
    lmul_value: lmul.LitLMulValue = validate.elem_ratio_to_lmul(
        elem_type, ratio
    )
    raw_type: str = f"v{elem_type.long_name}{lmul_value.lmul.short_name}_t"
    return guarded.Guarded(
        guarded.elem_ratio_guard(elem_type, ratio, need_zvfh=False),
        f"""template <>
struct VReg<{elem_type.cpp_repr}, {ratio.cpp_repr}> {{
  using RegType = {raw_type};
}};
template <>
struct VRegTraits<{raw_type}> {{
  using ElemType = {elem_type.cpp_repr};
  constexpr static size_t kRatio = {ratio.cpp_repr};
}};
""",
    )


def vmask_specialization_def(
    ratio: misc.LitSizeTValue,
) -> Optional[cpp_repr.HasCppRepr]:
    raw_type: str = f"vbool{ratio.value}_t"
    return guarded.Guarded(
        guarded.ratio_guard(ratio),
        f"""template <>
struct VMask<{ratio.cpp_repr}> {{
  using MaskType = {raw_type};
}};
template <>
struct VMaskTraits<{raw_type}> {{
  constexpr static size_t kRatio = {ratio.cpp_repr};
}};
""",
    )


rvv_type_header = header.Header(
    [
        header.Namespace(
            "rvv::internal",
            [
                header.CrossProduct(
                    vreg_specialization_def, elem.ALL_ELEM_TYPES, misc.ALL_RATIO
                ),
                header.CrossProduct(vmask_specialization_def, misc.ALL_RATIO),
            ],
            allowed_variants={""},
        )
    ],
    need_include_guard=False,
)

if __name__ == "__main__":
    main.main(rvv_type_header)
