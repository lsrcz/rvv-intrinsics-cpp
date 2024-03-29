import abc
from dataclasses import dataclass
from typing import Sequence, Union, overload

from codegen.param_list import param_list as plist
from codegen.typing import base


@dataclass(frozen=True, kw_only=True)
class TypedParam:
    type: base.Type
    name: str

    @property
    def cpp_repr(self) -> str:
        return f"{self.type.cpp_repr} {self.name}"


class FunctionParamList(plist.ParamList, metaclass=abc.ABCMeta):
    @property
    def _left_bracket(self) -> str:
        return "("

    @property
    def _right_bracket(self) -> str:
        return ")"


class FunctionTypedParamList(FunctionParamList):
    def __init__(self, *typed_param_list: TypedParam) -> None:
        self.typed_param_list: Sequence[TypedParam] = typed_param_list

    @property
    def _cpp_repr_without_brackets(self) -> str:
        return ", ".join(
            [typed_param.cpp_repr for typed_param in self.typed_param_list]
        )

    @property
    def forward(self) -> "FunctionArgumentList":
        return FunctionArgumentList(
            *[typed_param.name for typed_param in self.typed_param_list]
        )

    def __add__(
        self,
        other: Union[
            "FunctionTypedParamList", tuple[base.Type, str], TypedParam
        ],
    ) -> "FunctionTypedParamList":
        if isinstance(other, FunctionTypedParamList):
            return FunctionTypedParamList(
                *list(self.typed_param_list) + list(other.typed_param_list)
            )
        if isinstance(other, TypedParam):
            return self + FunctionTypedParamList(other)
        return self + TypedParam(type=other[0], name=other[1])

    def __len__(self) -> int:
        return len(self.typed_param_list)

    @overload
    def __getitem__(self, index: int) -> TypedParam:
        pass

    @overload
    def __getitem__(self, index: slice) -> "FunctionTypedParamList":
        pass

    def __getitem__(
        self, index: int | slice
    ) -> Union[TypedParam, "FunctionTypedParamList"]:
        if isinstance(index, slice):
            return FunctionTypedParamList(
                *[typed_param for typed_param in self.typed_param_list[index]]
            )
        return self.typed_param_list[index]

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FunctionTypedParamList):
            return False
        return self.typed_param_list == other.typed_param_list


def param_list(
    type_list: Sequence[base.Type] = tuple(), name_list: Sequence[str] = tuple()
) -> FunctionTypedParamList:
    assert len(type_list) == len(name_list)
    return FunctionTypedParamList(
        *[
            TypedParam(type=type, name=name)
            for type, name in zip(type_list, name_list)
        ]
    )


class FunctionArgumentList(FunctionParamList):
    def __init__(self, *arg_list: str) -> None:
        self.arg_list: Sequence[str] = arg_list

    @property
    def _cpp_repr_without_brackets(self) -> str:
        return ", ".join(self.arg_list)

    def __add__(self, other: "FunctionArgumentList") -> "FunctionArgumentList":
        return FunctionArgumentList(*list(self.arg_list) + list(other.arg_list))

    def __len__(self) -> int:
        return len(self.arg_list)

    @overload
    def __getitem__(self, index: int) -> str:
        pass

    @overload
    def __getitem__(self, index: slice) -> "FunctionArgumentList":
        pass

    def __getitem__(
        self, index: int | slice
    ) -> Union[str, "FunctionArgumentList"]:
        if isinstance(index, slice):
            return FunctionArgumentList(*self.arg_list[index])
        return self.arg_list[index]

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FunctionArgumentList):
            return False
        return self.arg_list == other.arg_list
