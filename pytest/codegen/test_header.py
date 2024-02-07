from codegen import header, cpp_repr
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


def test_variant_namespace() -> None:
    assert (
        header.VariantNamespace(
            [
                header.WithVariants(
                    lambda v: f"_{v}", allowed_variants={"", "m", "tu", "tumu"}
                )
            ]
        ).render(["", "m", "tu", "tum", "mu", "tumu"])
        == f"""_
_m

namespace tu {{
_tu
}}  // namespace tu

namespace tumu {{
_tumu
}}  // namespace tumu"""
    )


def test_with_variants() -> None:
    assert (
        header.WithVariants(
            lambda variant: ":" + variant,
            allowed_variants={"", "m", "tu"},
        ).render(["", "m", "tu", "tum"])
        == f""":
:m
:tu"""
    )


def test_cross_product() -> None:
    def gen(arg1: str, arg2: str) -> header.HeaderPart:
        if arg1 == "a" and arg2 == "d":
            return header.Verbatim("")
        return header.WithVariants(lambda v: f"{v}, {arg1}, {arg2}")

    assert (
        header.CrossProduct(gen, ["a", "b"], ["c", "d"]).render(["", "m"])
        == """, a, c
m, a, c
, b, c
m, b, c
, b, d
m, b, d"""
    )


def test_cross_product_variants() -> None:
    def gen(variant: str, arg1: str, arg2: str) -> cpp_repr.HasCppRepr:
        if arg1 == "a" and arg2 == "d":
            return None
        return f"{variant}, {arg1}, {arg2}"

    assert (
        header.CrossProduct.variant(gen, ["a", "b"], ["c", "d"]).render(
            ["", "m"]
        )
        == """, a, c
m, a, c
, b, c
m, b, c
, b, d
m, b, d"""
    )


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
