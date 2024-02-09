from typing import Optional

from codegen import cpp_repr, guarded, header, main, validate
from codegen.typing import elem, lmul, misc, vreg


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
struct GetElemType<{raw_type}> {{
  using ElemType = {elem_type.cpp_repr};
}};
template <>
struct GetRatio<{raw_type}> {{
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
struct GetRatio<{raw_type}> {{
  constexpr static size_t kRatio = {ratio.cpp_repr};
}};
""",
    )


def widened_type(elem_type: elem.RawElemType) -> Optional[elem.RawElemType]:
    if isinstance(elem_type, elem.IntType) and elem_type.width <= 32:
        return elem.int_type(elem_type.width * 2, elem_type.signed)
    if isinstance(elem_type, elem.FloatType) and elem_type.width <= 32:
        return elem.float_type(elem_type.width * 2)
    return None


def narrowed_type(elem_type: elem.RawElemType) -> Optional[elem.RawElemType]:
    if isinstance(elem_type, elem.IntType) and elem_type.width >= 16:
        return elem.int_type(elem_type.width // 2, elem_type.signed)
    if isinstance(elem_type, elem.FloatType) and elem_type.width >= 32:
        return elem.float_type(elem_type.width // 2)
    return None


def widened_narrowed_scalar_type_specialization_def(
    elem_type: elem.RawElemType,
) -> str:
    ret: list[str] = []
    widened = widened_type(elem_type)
    narrowed = narrowed_type(elem_type)
    if widened:
        ret.append(
            guarded.Guarded(
                guarded.elem_guard(widened, need_zvfh=False),
                f"""template <>
struct WidenedType<{elem_type.cpp_repr}> {{
  using Type = {widened.cpp_repr};
}};""",
            ).cpp_repr
        )
    if narrowed:
        ret.append(
            guarded.Guarded(
                guarded.elem_guard(elem_type, need_zvfh=False),
                f"""template <>
struct NarrowedType<{elem_type.cpp_repr}> {{
  using Type = {narrowed.cpp_repr};
}};""",
            ).cpp_repr
        )

    return "\n".join(ret)


def widened_narrowed_vreg_specialization_def(
    elem_type: elem.RawElemType, ratio: misc.LitSizeTValue
) -> cpp_repr.HasCppRepr:
    if not validate.is_compatible_elem_ratio_may_under_guards(elem_type, ratio):
        return ""
    ret: list[guarded.Guarded] = []
    widened = widened_type(elem_type)
    narrowed = narrowed_type(elem_type)
    if (
        widened is not None
        and validate.is_compatible_elem_ratio_may_under_guards(widened, ratio)
    ):
        ret.append(
            guarded.Guarded(
                guarded.elem_ratio_guard(widened, ratio, need_zvfh=False),
                f"""template <>
struct WidenedType<vreg_t<{elem_type.cpp_repr}, {ratio.cpp_repr}>> {{
  using Type = vreg_t<{widened.cpp_repr}, {ratio.cpp_repr}>;
}};
""",
            )
        )
    if (
        narrowed is not None
        and validate.is_compatible_elem_ratio_may_under_guards(narrowed, ratio)
    ):
        ret.append(
            guarded.Guarded(
                guarded.elem_ratio_guard(narrowed, ratio, need_zvfh=False),
                f"""template <>
struct NarrowedType<vreg_t<{elem_type.cpp_repr}, {ratio.cpp_repr}>> {{
  using Type = vreg_t<{narrowed.cpp_repr}, {ratio.cpp_repr}>;
}};
""",
            )
        )
    if len(ret) == 0:
        return ""
    if len(ret) == 1:
        return guarded.Guarded(
            guarded.elem_ratio_guard(elem_type, ratio, need_zvfh=False)
            + ret[0].guards,
            ret[0].cpp_repr,
        )
    return guarded.Guarded(
        guarded.elem_ratio_guard(elem_type, ratio, need_zvfh=False),
        "\n".join(map(lambda x: x.cpp_repr, ret)),
    )


def to_signed_unsigned_scalar_type_specialization_def(
    elem_type: elem.RawElemType,
) -> cpp_repr.HasCppRepr:
    if not isinstance(elem_type, elem.IntType):
        return ""
    if not elem_type.signed:
        return ""
    unsigned_type = elem.int_type(elem_type.width, False)
    return guarded.Guarded(
        guarded.elem_guard(elem_type, False),
        f"""template <>
struct ToUnsigned<{elem_type.cpp_repr}> {{
  using Type = {unsigned_type.cpp_repr};
}};
template <>
struct ToSigned<{unsigned_type.cpp_repr}> {{
  using Type = {elem_type.cpp_repr};
}};""",
    )


def to_signed_unsigned_vreg_type_specialization_def(
    elem_type: elem.RawElemType, ratio: misc.LitSizeTValue
) -> cpp_repr.HasCppRepr:
    if not isinstance(elem_type, elem.IntType):
        return ""
    if not elem_type.signed:
        return ""
    if not validate.is_compatible_elem_ratio_may_under_guards(elem_type, ratio):
        return ""

    signed_type = vreg.concrete(elem_type, ratio)
    unsigned_type = vreg.concrete(elem.int_type(elem_type.width, False), ratio)
    return guarded.Guarded(
        guarded.elem_ratio_guard(elem_type, ratio, need_zvfh=False),
        f"""template <>
struct ToUnsigned<{signed_type.cpp_repr}> {{
  using Type = {unsigned_type.cpp_repr};
}};
template <>
struct ToSigned<{unsigned_type.cpp_repr}> {{
  using Type = {signed_type.cpp_repr};
}};""",
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
                header.CrossProduct(
                    widened_narrowed_scalar_type_specialization_def,
                    elem.ALL_ELEM_TYPES,
                ),
                header.CrossProduct(
                    widened_narrowed_vreg_specialization_def,
                    elem.ALL_ELEM_TYPES,
                    misc.ALL_RATIO,
                ),
                header.CrossProduct(
                    to_signed_unsigned_scalar_type_specialization_def,
                    elem.ALL_ELEM_TYPES,
                ),
                header.CrossProduct(
                    to_signed_unsigned_vreg_type_specialization_def,
                    elem.ALL_ELEM_TYPES,
                    misc.ALL_RATIO,
                ),
            ],
            allowed_variants={""},
        )
    ],
    need_include_guard=False,
)

if __name__ == "__main__":
    main.main(rvv_type_header)
