import abc
from typing import Sequence, Union, overload

from codegen.param_list import param_list
from codegen.typing import base


class TemplateParamList(param_list.ParamList, metaclass=abc.ABCMeta):
    @property
    def _left_bracket(self) -> str:
        return "<"

    @property
    def _right_bracket(self) -> str:
        return ">"


class TemplateTypeArgumentList(TemplateParamList):
    def __init__(self, *type_arg_list: base.Type) -> None:
        self.type_arg_list: Sequence[base.Type] = type_arg_list

    @property
    def _cpp_repr_without_brackets(self) -> str:
        return ", ".join(
            [type_param.cpp_repr for type_param in self.type_arg_list]
        )

    def __add__(
        self, other: "TemplateTypeArgumentList"
    ) -> "TemplateTypeArgumentList":
        return TemplateTypeArgumentList(
            *list(self.type_arg_list) + list(other.type_arg_list)
        )

    def __len__(self) -> int:
        return len(self.type_arg_list)

    @overload
    def __getitem__(self, index: int) -> base.Type:
        pass

    @overload
    def __getitem__(self, index: slice) -> "TemplateTypeArgumentList":
        pass

    def __getitem__(
        self, index: int | slice
    ) -> Union[base.Type, "TemplateTypeArgumentList"]:
        if isinstance(index, slice):
            return TemplateTypeArgumentList(*self.type_arg_list[index])
        return self.type_arg_list[index]

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TemplateTypeArgumentList):
            return False
        return self.type_arg_list == other.type_arg_list


class TemplateTypeParamList(TemplateParamList):
    def __init__(self, *type_param_list: base.TypeParam) -> None:
        self.type_param_list: Sequence[base.TypeParam] = type_param_list

    @property
    def _cpp_repr_without_brackets(self) -> str:
        return ", ".join(
            [
                f"{type_param.kind.cpp_repr} {type_param.typename}"
                for type_param in self.type_param_list
            ]
        )

    @property
    def forward(self) -> TemplateTypeArgumentList:
        return TemplateTypeArgumentList(*self.type_param_list)

    def __add__(
        self, other: "TemplateTypeParamList"
    ) -> "TemplateTypeParamList":
        return TemplateTypeParamList(
            *list(self.type_param_list) + list(other.type_param_list)
        )

    def __len__(self) -> int:
        return len(self.type_param_list)

    def __getitem__(
        self, index: int | slice
    ) -> Union[base.TypeParam, "TemplateTypeParamList"]:
        if isinstance(index, slice):
            return TemplateTypeParamList(*self.type_param_list[index])
        return self.type_param_list[index]

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TemplateTypeParamList):
            return False
        return self.type_param_list == other.type_param_list
