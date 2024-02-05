import abc


class ParamList(metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def _cpp_repr_without_brackets(self) -> str:
        pass

    @property
    @abc.abstractmethod
    def _left_bracket(self) -> str:
        pass

    @property
    @abc.abstractmethod
    def _right_bracket(self) -> str:
        pass

    @property
    def cpp_repr(self) -> str:
        return (
            self._left_bracket
            + self._cpp_repr_without_brackets
            + self._right_bracket
        )
