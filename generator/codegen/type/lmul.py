from typing import Sequence
from dataclasses import dataclass
from . import type


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
class LMulType(type.Type):
    @property
    def cpp_repr(self) -> str:
        return "LMul"


@dataclass(frozen=True, kw_only=True)
class LMulValue(type.Type):
    pass


@dataclass(frozen=True, kw_only=True)
class LitLMulValue(LMulValue):
    lmul: LMul

    @property
    def cpp_repr(self) -> str:
        return self.lmul.qualified_enum_value


ALL_LMUL: Sequence[LitLMulValue] = [
    LitLMulValue(lmul=LMul(lmul=3)),
    LitLMulValue(lmul=LMul(lmul=2)),
    LitLMulValue(lmul=LMul(lmul=1)),
    LitLMulValue(lmul=LMul(lmul=0)),
    LitLMulValue(lmul=LMul(lmul=-1)),
    LitLMulValue(lmul=LMul(lmul=-2)),
    LitLMulValue(lmul=LMul(lmul=-3)),
]


@dataclass(frozen=True, kw_only=True)
class ParamLMulValueType(LMulValue, type.TypeParam):
    @property
    def kind(self) -> type.DataKind:
        return type.DataKind(data_type=LMulType())
