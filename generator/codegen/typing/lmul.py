import abc
from dataclasses import dataclass
from typing import Sequence

from codegen.typing import base


@dataclass(frozen=True, kw_only=True)
class LMul:
    lmul: int

    @property
    def enum_value(self) -> str:
        return {
            3: "kM8",
            2: "kM4",
            1: "kM2",
            0: "kM1",
            -1: "kMF2",
            -2: "kMF4",
            -3: "kMF8",
        }[self.lmul]

    @property
    def qualified_enum_value(self) -> str:
        return f"LMul::{self.enum_value}"

    @property
    def short_name(self) -> str:
        return {
            3: "m8",
            2: "m4",
            1: "m2",
            0: "m1",
            -1: "mf2",
            -2: "mf4",
            -3: "mf8",
        }[self.lmul]


@dataclass(frozen=True, kw_only=True)
class LMulType(base.Type):
    @property
    def cpp_repr(self) -> str:
        return "LMul"


@dataclass(frozen=True, kw_only=True)
class LMulValue(base.Type, metaclass=abc.ABCMeta):
    pass


@dataclass(frozen=True, kw_only=True)
class LitLMulValue(LMulValue):
    lmul: LMul

    @property
    def cpp_repr(self) -> str:
        return self.lmul.qualified_enum_value


def lit(lmul: int) -> LitLMulValue:
    return LitLMulValue(lmul=LMul(lmul=lmul))


ALL_LMUL: Sequence[LitLMulValue] = [
    lit(3),
    lit(2),
    lit(1),
    lit(0),
    lit(-1),
    lit(-2),
    lit(-3),
]


@dataclass(frozen=True, kw_only=True)
class ParamLMulValueType(LMulValue, base.TypeParam):
    @property
    def kind(self) -> base.DataKind:
        return base.DataKind(data_type=LMulType())


def param(typename: str) -> ParamLMulValueType:
    return ParamLMulValueType(typename=typename)
