import abc
from dataclasses import dataclass
from typing import Sequence

from codegen import cpp_repr
from codegen.typing import elem, misc


@dataclass(frozen=True, kw_only=True)
class Guard(metaclass=abc.ABCMeta):
    @property
    def cpp_repr(self) -> str:
        raise NotImplementedError


@dataclass(frozen=True, kw_only=True)
class FlagGuard(Guard):
    flag: str

    @property
    def cpp_repr(self) -> str:
        return self.flag


class Guarded:
    def __init__(
        self, guards: Sequence[Guard], content: cpp_repr.HasCppRepr
    ) -> None:
        self.guards: list[Guard] = list(set(guards))
        self.content: cpp_repr.HasCppRepr = content

    @property
    def cpp_repr(self) -> str:
        if len(self.guards) == 0:
            return cpp_repr.to_cpp_repr(self.content)
        elif len(self.guards) == 1:
            return f"""#if {self.guards[0].cpp_repr}
{cpp_repr.to_cpp_repr(self.content)}
#endif"""
        else:
            guards = " && ".join(map(lambda g: f"{g.cpp_repr}", self.guards))
            return f"""#if {guards}
{cpp_repr.to_cpp_repr(self.content)}
#endif"""


def elem_guard(e: elem.RawElemType, need_zvfh: bool) -> list[Guard]:
    if isinstance(e, elem.IntType):
        match e.width:
            case 64:
                return [FlagGuard(flag="HAS_ZVE64X")]
            case 8 | 16 | 32:
                return []
            case _:
                raise ValueError(f"Unexpected integer width: {e.width}")
    elif isinstance(e, elem.FloatType):
        match e.width:
            case 16:
                if need_zvfh:
                    return [FlagGuard(flag="HAS_ZVFH")]
                else:
                    return [FlagGuard(flag="HAS_ZVFHMIN")]
            case 32:
                return [FlagGuard(flag="HAS_ZVE32F")]
            case 64:
                return [FlagGuard(flag="HAS_ZVE64D")]
            case _:
                raise ValueError(f"Unexpected float width: {e.width}")
    raise ValueError(f"Unexpected element type: {type(e)}")


def ratio_guard(r: misc.LitSizeTValue) -> list[Guard]:
    assert r.value in [1, 2, 4, 8, 16, 32, 64]
    if r.value == 64:
        return [FlagGuard(flag="HAS_ELEN64")]
    else:
        return []


def elem_ratio_guard(
    e: elem.RawElemType, r: misc.LitSizeTValue, need_zvfh: bool
) -> list[Guard]:
    return elem_guard(e, need_zvfh) + ratio_guard(r)
