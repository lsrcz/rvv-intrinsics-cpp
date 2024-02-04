import pytest
from codegen.type import elem, misc
from codegen import guarded


@pytest.mark.parametrize(
    "e,need_zvfh,expected",
    [
        (elem.IntType(width=8, signed=True), True, []),
        (elem.IntType(width=32, signed=True), True, []),
        (
            elem.IntType(width=64, signed=True),
            True,
            [guarded.FlagGuard(flag="HAS_ZVE64X")],
        ),
        (elem.IntType(width=8, signed=False), True, []),
        (elem.IntType(width=32, signed=False), True, []),
        (
            elem.IntType(width=64, signed=False),
            True,
            [guarded.FlagGuard(flag="HAS_ZVE64X")],
        ),
        (
            elem.FloatType(width=16),
            True,
            [guarded.FlagGuard(flag="HAS_ZVFH")],
        ),
        (
            elem.FloatType(width=16),
            False,
            [guarded.FlagGuard(flag="HAS_ZVFHMIN")],
        ),
        (
            elem.FloatType(width=32),
            True,
            [guarded.FlagGuard(flag="HAS_ZVE32F")],
        ),
        (
            elem.FloatType(width=64),
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
    assert guarded.ratio_guard(misc.LitSizeTValue(value=ratio)) == expected


def test_elem_ratio_guard() -> None:
    assert guarded.elem_ratio_guard(
        elem.FloatType(width=32), misc.LitSizeTValue(value=64), True
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
