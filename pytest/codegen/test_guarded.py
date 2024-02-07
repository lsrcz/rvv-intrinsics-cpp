from codegen import guarded
from codegen.typing import elem, misc

import pytest


@pytest.mark.parametrize(
    "e,need_zvfh,expected",
    [
        (elem.int8_t, True, []),
        (elem.int32_t, True, []),
        (
            elem.int64_t,
            True,
            [guarded.FlagGuard(flag="HAS_ZVE64X")],
        ),
        (elem.uint8_t, True, []),
        (elem.uint32_t, True, []),
        (
            elem.uint64_t,
            True,
            [guarded.FlagGuard(flag="HAS_ZVE64X")],
        ),
        (
            elem.float16_t,
            True,
            [guarded.FlagGuard(flag="HAS_ZVFH")],
        ),
        (
            elem.float16_t,
            False,
            [guarded.FlagGuard(flag="HAS_ZVFHMIN")],
        ),
        (
            elem.float32_t,
            True,
            [guarded.FlagGuard(flag="HAS_ZVE32F")],
        ),
        (
            elem.float64_t,
            True,
            [guarded.FlagGuard(flag="HAS_ZVE64D")],
        ),
    ],
)
def test_elem_guard(
    e: elem.RawElemType, need_zvfh: bool, expected: list[guarded.Guard]
) -> None:
    assert guarded.elem_guard(e, need_zvfh) == expected


@pytest.mark.parametrize(
    "ratio,expected",
    [(1, []), (32, []), (64, [guarded.FlagGuard(flag="HAS_ELEN64")])],
)
def test_ratio_guard(ratio: int, expected: list[guarded.Guard]) -> None:
    assert guarded.ratio_guard(misc.lit_size_t(ratio)) == expected


def test_elem_ratio_guard() -> None:
    assert guarded.elem_ratio_guard(
        elem.float32_t, misc.lit_size_t(64), True
    ) == [
        guarded.FlagGuard(flag="HAS_ZVE32F"),
        guarded.FlagGuard(flag="HAS_ELEN64"),
    ]


def test_guarded() -> None:
    g = guarded.Guarded(
        guards=[
            guarded.FlagGuard(flag="HAS_ZVE32F"),
            guarded.FlagGuard(flag="HAS_ELEN64"),
        ],
        content="abc",
    )
    assert (
        g.cpp_repr
        == """#if HAS_ZVE32F && HAS_ELEN64
abc
#endif"""
    )
