from typing import Union, get_origin, get_args


def is_optional(field):
    return get_origin(field) is Union and type(None) in get_args(field)


class Node:
    def __init__(self, name: str, value, out_type: type):
        if not isinstance(out_type, type) and not is_optional(out_type):
            raise TypeError("out_type must be a type")

        self._name = name
        self._value = value
        self._out_type = out_type

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        return self._value

    @property
    def out_type(self):
        return self._out_type


class MappingNode(Node):
    def __init__(self, name: str, value: dict, out_type: type):
        super().__init__(name, value, out_type)

        self._yaml_names = {}
        for field_name, field in out_type.__dataclass_fields__.items():
            yaml_str = field.metadata.get("yaml", field_name)
            self._yaml_names[yaml_str] = field_name

            # This is an optional value that was not set.
            # We need to set it to None.
            if yaml_str not in value.keys():
                value[yaml_str] = None

    @property
    def yaml_names(self):
        return self._yaml_names


class SequenceNode(Node):
    def __init__(self, name: str, value: Union[list, tuple], out_type: type):
        super().__init__(name, value, out_type)


class ScalarNode(Node):
    def __init__(self, name: str, value: Union[int, float, str], out_type: type):
        super().__init__(name, value, out_type)


class OptionalNoneNode(Node):
    def __init__(self, name: str):
        super().__init__(name, None, type(None))


def new_node(
    value_name, value, out_type
) -> Union[MappingNode, SequenceNode, ScalarNode]:
    if isinstance(value, dict):
        node = MappingNode(value_name, value, out_type)
    elif isinstance(value, (int, float, str)):
        node = ScalarNode(value_name, value, out_type)
    elif isinstance(value, (list, tuple)):
        node = SequenceNode(value_name, value, out_type)
    elif value is None:
        node = OptionalNoneNode(value_name)
    else:
        raise TypeError(f"{value_name} is not of known type")

    return node
