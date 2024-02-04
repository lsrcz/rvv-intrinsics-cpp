from typing import Optional
from codegen import header, cpp_repr
from codegen.type import elem, lmul, misc
import tempfile
import os


def test_include() -> None:
    assert (
        header.Include("rvv/type.h").render(["", "m"])
        == "#include <rvv/type.h>"
    )


def test_verbatim() -> None:
    assert header.Verbatim("// abc").render(["", "m"]) == "// abc"


def test_namespace() -> None:
    assert (
        header.Namespace(
            "foo",
            [header.Include("bar.h"), header.Verbatim("// abc")],
        ).render(["", "m"])
        == """namespace foo {
#include <bar.h>
// abc
}  // namespace foo"""
    )


def test_with_variants() -> None:
    assert (
        header.WithVariants(
            lambda variant: variant,
            allowed_variants={"", "m", "tu"},
        ).render(["", "m", "tu", "tum"])
        == f"""
m
tu"""
    )


def test_for_all_elem_lmul() -> None:
    def gen(
        variant: str, e: elem.RawElemType, l: lmul.LitLMulValue
    ) -> Optional[cpp_repr.HasCppRepr]:
        if (e.element_width.bit_count() + l.lmul.lmul.bit_count()) % 2 == 0:
            return None
        return f"{variant}, {e.cpp_repr}, {l.lmul.short_name}"

    expected: list[str] = []
    for v in ["tu", "tum"]:
        for e in elem.ALL_ELEM_TYPES:
            for l in lmul.ALL_LMUL:
                generated = gen(v, e, l)
                if generated is not None:
                    expected.append(cpp_repr.to_cpp_repr(generated))

    assert header.ForAllElemLmul(
        gen, allowed_variants={"m", "tu", "tum"}
    ).render(["", "tu", "tum", "mu", "tumu"]) == "\n".join(expected)


def test_for_all_ratio() -> None:
    def gen(
        variant: str, r: misc.LitSizeTValue
    ) -> Optional[cpp_repr.HasCppRepr]:
        if r.value.bit_count() % 2 == 0:
            return None
        return f"{variant}, {r.value}"

    expected: list[str] = []
    for v in ["tu", "tum"]:
        for r in misc.ALL_RATIO:
            generated = gen(v, r)
            if generated is not None:
                expected.append(cpp_repr.to_cpp_repr(generated))

    assert header.ForAllRatio(gen, allowed_variants={"m", "tu", "tum"}).render(
        ["", "tu", "tum", "mu", "tumu"]
    ) == "\n".join(expected)


def test_for_all_elem_ratio() -> None:
    def gen(
        variant: str, e: elem.RawElemType, r: misc.LitSizeTValue
    ) -> Optional[cpp_repr.HasCppRepr]:
        if (e.element_width.bit_count() + r.value.bit_count()) % 2 == 0:
            return None
        return f"{variant}, {r.value}"

    expected: list[str] = []
    for v in ["tu", "tum"]:
        for e in elem.ALL_ELEM_TYPES:
            for r in misc.ALL_RATIO:
                generated = gen(v, e, r)
                if generated is not None:
                    expected.append(cpp_repr.to_cpp_repr(generated))

    assert header.ForAllElemRatio(
        gen, allowed_variants={"m", "tu", "tum"}
    ).render(["", "tu", "tum", "mu", "tumu"]) == "\n".join(expected)


header_body = header.Namespace(
    "rvv::internal",
    [
        header.WithVariants(
            lambda variant: variant,
            allowed_variants={"tu", "tum"},
        )
    ],
    allowed_variants={"m", "tu"},
)


def test_header_with_guard() -> None:
    assert (
        header.Header(
            [header.Include("a.h"), header_body],
        ).render(["", "m", "tu", "tum"], "test/test.h")
        == """// Copyright (c) 2024 by Sirui Lu (siruilu@cs.washington.edu)
// This file is auto-generated.
#ifndef TEST_TEST_H_
#define TEST_TEST_H_

#include <a.h>
namespace rvv::internal {
tu
}  // namespace rvv::internal

#endif  // TEST_TEST_H_
"""
    )


def test_header_without_guard() -> None:
    assert (
        header.Header(
            [header.Include("a.h"), header_body],
            need_include_guard=False,
        ).render(["", "m", "tu", "tum"], "test/test.h")
        == """// Copyright (c) 2024 by Sirui Lu (siruilu@cs.washington.edu)
// This file is auto-generated.

#include <a.h>
namespace rvv::internal {
tu
}  // namespace rvv::internal
"""
    )


def test_header_write() -> None:
    base_dir: str = tempfile.mkdtemp(
        prefix="rvv-test", dir=tempfile.gettempdir()
    )

    header.Header(
        [header.Include("a.h"), header_body],
        need_include_guard=False,
    ).write(["", "m", "tu", "tum"], base_dir, "test/test.h")
    with open(os.path.join(base_dir, "test/test.h")) as f:
        content = f.read()
        assert (
            content
            == """// Copyright (c) 2024 by Sirui Lu (siruilu@cs.washington.edu)
// This file is auto-generated.

#include <a.h>
namespace rvv::internal {
tu
}  // namespace rvv::internal
"""
        )
