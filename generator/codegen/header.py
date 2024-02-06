import abc
import os
from typing import Callable, Iterable, Optional, Sequence, Union
from . import cpp_repr, macro
from .type import elem, lmul, misc

ALL_VARIANTS: set[str] = {"", "m", "tu", "tum", "mu", "tumu"}


class HeaderPart(metaclass=abc.ABCMeta):
    def __init__(self, allowed_variants: set[str]) -> None:
        assert allowed_variants.issubset(ALL_VARIANTS)
        self.allowed_variants: set[str] = allowed_variants
        pass

    @abc.abstractmethod
    def _render(self, variants: Sequence[str]) -> str:
        pass

    def render(self, variants: Sequence[str]) -> str:
        assert set(variants).issubset(ALL_VARIANTS)
        filtered_variants: Sequence[str] = [
            variant for variant in variants if variant in self.allowed_variants
        ]
        if len(filtered_variants) == 0:
            return ""
        return self._render(filtered_variants)


HeaderPartLike = Union[cpp_repr.HasCppRepr, HeaderPart]


def render(part_like: HeaderPartLike, variants: Sequence[str]) -> str:
    if isinstance(part_like, HeaderPart):
        return part_like.render(variants)
    return cpp_repr.to_cpp_repr(part_like)


class Include(HeaderPart):
    def __init__(
        self, filename: str, allowed_variants: set[str] = ALL_VARIANTS
    ) -> None:
        super().__init__(allowed_variants=allowed_variants)
        self.filename: str = filename

    def _render(self, variants: Sequence[str]) -> str:
        return f"#include <{self.filename}>"


class Verbatim(HeaderPart):
    def __init__(
        self,
        content: cpp_repr.HasCppRepr,
        allowed_variants: set[str] = ALL_VARIANTS,
    ) -> None:
        super().__init__(allowed_variants=allowed_variants)
        self.content: cpp_repr.HasCppRepr = content

    def _render(self, variants: Sequence[str]) -> str:
        return cpp_repr.to_cpp_repr(self.content)


class Namespace(HeaderPart):
    def __init__(
        self,
        name: str,
        content: Sequence[HeaderPartLike],
        allowed_variants: set[str] = ALL_VARIANTS,
    ) -> None:
        super().__init__(allowed_variants=allowed_variants)
        self.name: str = name
        self.content: Sequence[HeaderPartLike] = content

    def _render(self, variants: Sequence[str]) -> str:
        rendered = "\n".join([render(part, variants) for part in self.content])
        return f"""namespace {self.name} {{
{rendered}
}}  // namespace {self.name}"""


class VariantNamespace(HeaderPart):
    def __init__(
        self,
        content: Sequence[HeaderPartLike],
        allowed_variants: set[str] = ALL_VARIANTS,
    ) -> None:
        super().__init__(allowed_variants=allowed_variants)
        self.content: Sequence[HeaderPartLike] = content

    def _render(self, variants: Sequence[str]) -> str:
        namespaces: dict[str, list[str]] = dict()

        def add(namespace_name: str, variant: str) -> None:
            if namespace_name not in namespaces:
                namespaces[namespace_name] = []
            namespaces[namespace_name].append(variant)

        for variant in variants:
            if variant == "" or variant == "m":
                add("", variant)
            elif variant == "tu" or variant == "tum":
                add("tu", variant)
            elif variant == "mu" or variant == "tumu":
                add(variant, variant)
            else:
                raise ValueError(f"Unexpected variant: {variant}")
        ret: list[str] = []
        for namespace_name, namespace_variants in namespaces.items():
            rendered = [
                render(part, namespace_variants) for part in self.content
            ]
            if len(rendered) == 0 or all([r == "" for r in rendered]):
                continue
            joined = "\n".join(rendered)
            if namespace_name == "":
                ret.append(joined)
            else:
                ret.append(
                    f"""namespace {namespace_name} {{
{joined}
}}  // namespace {namespace_name}"""
                )
        return "\n\n".join(ret)


def join_all_generated(all_generated: Iterable[Optional[str]]) -> str:
    all: list[str] = []
    for generated in all_generated:
        if generated is not None:
            all.append(generated)
    if len(all) != 0:
        return "\n".join(all)
    return ""


class WithVariants(HeaderPart):
    def __init__(
        self,
        gen: Callable[[str], cpp_repr.HasCppRepr],
        allowed_variants: set[str] = ALL_VARIANTS,
    ) -> None:
        super().__init__(allowed_variants=allowed_variants)
        self.gen: Callable[[str], cpp_repr.HasCppRepr] = gen

    def _render(self, variants: Sequence[str]) -> str:
        return join_all_generated(
            [cpp_repr.to_cpp_repr(self.gen(variant)) for variant in variants]
        )


class ForAllElemLmul(HeaderPart):
    def __init__(
        self,
        gen: Callable[
            [str, elem.RawElemType, lmul.LitLMulValue],
            Optional[cpp_repr.HasCppRepr],
        ],
        allowed_variants: set[str] = ALL_VARIANTS,
    ) -> None:
        super().__init__(allowed_variants=allowed_variants)
        self.gen: Callable[
            [str, elem.RawElemType, lmul.LitLMulValue],
            Optional[cpp_repr.HasCppRepr],
        ] = gen

    def _render(self, variants: Sequence[str]) -> str:
        return join_all_generated(
            [
                macro.for_all_elem_lmul(lambda e, l: self.gen(variant, e, l))
                for variant in variants
            ]
        )


class ForAllRatio(HeaderPart):
    def __init__(
        self,
        gen: Callable[[str, misc.LitSizeTValue], Optional[cpp_repr.HasCppRepr]],
        allowed_variants: set[str] = ALL_VARIANTS,
    ) -> None:
        super().__init__(allowed_variants=allowed_variants)
        self.gen: Callable[
            [str, misc.LitSizeTValue], Optional[cpp_repr.HasCppRepr]
        ] = gen

    def _render(self, variants: Sequence[str]) -> str:
        return join_all_generated(
            [
                macro.for_all_ratio(lambda r: self.gen(variant, r))
                for variant in variants
            ]
        )


class ForAllElemRatio(HeaderPart):
    def __init__(
        self,
        gen: Callable[
            [str, elem.RawElemType, misc.LitSizeTValue],
            Optional[cpp_repr.HasCppRepr],
        ],
        allowed_variants: set[str] = ALL_VARIANTS,
    ) -> None:
        super().__init__(allowed_variants=allowed_variants)

        self.gen: Callable[
            [str, elem.RawElemType, misc.LitSizeTValue],
            Optional[cpp_repr.HasCppRepr],
        ] = gen

    def _render(self, variants: Sequence[str]) -> str:
        return join_all_generated(
            [
                macro.for_all_elem_ratio(lambda e, r: self.gen(variant, e, r))
                for variant in variants
            ]
        )


class ForAllElemSize(HeaderPart):
    def __init__(
        self,
        gen: Callable[[str, int], Optional[cpp_repr.HasCppRepr]],
        allowed_variants: set[str] = ALL_VARIANTS,
    ) -> None:
        super().__init__(allowed_variants=allowed_variants)
        self.gen: Callable[[str, int], Optional[cpp_repr.HasCppRepr]] = gen

    def _render(self, variants: Sequence[str]) -> str:
        return join_all_generated(
            [
                macro.for_all_elem_size(lambda size: self.gen(variant, size))
                for variant in variants
            ]
        )


class Header:
    def __init__(
        self, parts: Sequence[HeaderPartLike], need_include_guard: bool = True
    ) -> None:
        self.parts: Sequence[HeaderPartLike] = parts
        self.need_include_guard: bool = need_include_guard

    def render(self, variants: Sequence[str], filename: str) -> str:
        rendered: str = "\n".join(
            [render(part, variants) for part in self.parts]
        )
        if self.need_include_guard:
            guard: str = (
                filename.upper().replace(".", "_").replace("/", "_") + "_"
            )
            return f"""// Copyright (c) 2024 by Sirui Lu (siruilu@cs.washington.edu)
// This file is auto-generated.
#ifndef {guard}
#define {guard}

{rendered}

#endif  // {guard}
"""
        else:
            return f"""// Copyright (c) 2024 by Sirui Lu (siruilu@cs.washington.edu)
// This file is auto-generated.

{rendered}
"""

    def write(
        self, variants: Sequence[str], base_dir: str, filename: str
    ) -> None:
        header_filename = os.path.join(base_dir, filename)
        os.makedirs(os.path.dirname(header_filename), exist_ok=True)
        with open(os.path.join(base_dir, filename), "w") as f:
            f.write(self.render(variants, filename))
