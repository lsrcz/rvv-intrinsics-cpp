from codegen.typing import elem, lmul, misc


def elem_ratio_to_lmul(
    elem_type: elem.RawElemType, ratio: misc.LitSizeTValue
) -> lmul.LitLMulValue:
    log_element_width: int = elem_type.element_width.bit_length()
    log_ratio: int = ratio.value.bit_length()
    return lmul.LitLMulValue(lmul=lmul.LMul(lmul=log_element_width - log_ratio))


def elem_lmul_to_ratio(
    elem_type: elem.RawElemType, lmul_value: lmul.LitLMulValue
) -> misc.LitSizeTValue:
    return misc.LitSizeTValue(
        value=elem_type.element_width * (1 << (3 - lmul_value.lmul.lmul)) // 8
    )


def is_valid_elem(elem_type: elem.RawElemType) -> bool:
    if isinstance(elem_type, elem.IntType):
        return elem_type.element_width in [8, 16, 32, 64]
    elif isinstance(elem_type, elem.FloatType):
        return elem_type.element_width in [16, 32, 64]
    else:
        return False


def is_valid_lmul(l: lmul.LitLMulValue) -> bool:
    return l.lmul.lmul in [-3, -2, -1, 0, 1, 2, 3]


def is_valid_elem_ratio(ratio: misc.LitSizeTValue) -> bool:
    return ratio.value in [1, 2, 4, 8, 16, 32, 64]


def is_compatible_elem_ratio_may_under_guards(
    elem_type: elem.RawElemType, ratio: misc.LitSizeTValue
) -> bool:
    return (
        is_valid_elem(elem_type)
        and is_valid_elem_ratio(ratio)
        and is_valid_lmul(elem_ratio_to_lmul(elem_type, ratio))
    )


def is_compatible_elem_lmul_may_under_guards(
    elem_type: elem.RawElemType, lmul_value: lmul.LitLMulValue
) -> bool:
    return (
        is_valid_elem(elem_type)
        and is_valid_lmul(lmul_value)
        and is_valid_elem_ratio(elem_lmul_to_ratio(elem_type, lmul_value))
    )
