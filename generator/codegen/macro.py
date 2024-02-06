from typing import Callable, Generator, Iterable, Optional, TypeVar
from .type import elem
from .type import lmul
from .type import misc
from . import cpp_repr

_T = TypeVar("_T")


def for_all(
    values: Iterable[_T], gen: Callable[[_T], Optional[cpp_repr.HasCppRepr]]
) -> Optional[str]:
    def inner() -> Generator[str, str, None]:
        for value in values:
            generated = gen(value)
            if generated is not None:
                yield cpp_repr.to_cpp_repr(generated)

    generated = list(inner())

    if len(generated) == 0:
        return None
    return "\n".join(generated)


def for_all_elem(
    gen: Callable[[elem.RawElemType], Optional[cpp_repr.HasCppRepr]]
) -> Optional[str]:
    return for_all(elem.ALL_ELEM_TYPES, gen)


def for_all_lmul(
    gen: Callable[[lmul.LitLMulValue], Optional[cpp_repr.HasCppRepr]]
) -> Optional[str]:
    return for_all(lmul.ALL_LMUL, gen)


def for_all_elem_lmul(
    gen: Callable[
        [elem.RawElemType, lmul.LitLMulValue], Optional[cpp_repr.HasCppRepr]
    ]
) -> Optional[str]:
    def inner(e: elem.RawElemType) -> Optional[str]:
        return for_all_lmul(lambda l: gen(e, l))

    return for_all_elem(inner)


def for_all_ratio(
    gen: Callable[[misc.LitSizeTValue], Optional[cpp_repr.HasCppRepr]]
) -> Optional[str]:
    return for_all(misc.ALL_RATIO, gen)


def for_all_elem_ratio(
    gen: Callable[
        [elem.RawElemType, misc.LitSizeTValue], Optional[cpp_repr.HasCppRepr]
    ]
) -> Optional[str]:
    def inner(e: elem.RawElemType) -> Optional[str]:
        return for_all_ratio(lambda r: gen(e, r))

    return for_all_elem(inner)


def for_all_elem_size(
    gen: Callable[[int], Optional[cpp_repr.HasCppRepr]]
) -> Optional[str]:
    return for_all([8, 16, 32, 64], gen)
