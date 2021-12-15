import copy

from dataclasses import is_dataclass
from typing import Optional, TypeVar, IO, Text, Union
import yaml

from yamldecoder.node import (
    OptionalNoneNode,
    Node,
    MappingNode,
    SequenceNode,
    ScalarNode,
    new_node,
)


class YamlDecoder:
    """YamlDecoder takes in a yaml stream and decodes it into a dataclass.

    Args:
        stream (Union[bytes, IO[bytes], Text, IO[Text]]): A yaml stream

    Example usage:
    >>> from dataclasses import dataclass, field
    >>> from yaml_decoder.decoder import YamlDecoder
    >>>
    >>> @dataclass
    >>> class ConfigB:
    >>>     a: int = field(metadata={"yaml": "A"})
    >>>     b: float = field(metadata={"yaml": "B"})
    >>>     c: str = field(metadata={"yaml": "C"})
    >>>     d: tuple = field(metadata={"yaml": "D"})
    >>>     e: list = field(metadata={"yaml": "E"})
    >>>
    >>> @dataclass
    >>> class Config:
    >>>     config_b: ConfigB = field(metadata={"yaml": "ConfigB"})
    >>>
    >>> with open("my_config.yaml", "r") as stream:
    >>>     cfg = YamlDecoder(stream).decode(Config)
    >>>

    You can also define Optional fields in your dataclass.
    These fields will default to None if no value exist in the yaml stream.

    Example usage:
    >>> from dataclasses import dataclass, field
    >>> from typing import Optional
    >>>
    >>> @dataclass
    >>> class Config:
    >>>     a: Optional[int] = field(metadata={"yaml": "A"})
    >>>     b: float = field(metadata={"yaml": "B"})
    >>>
    >>>`


    """

    def __init__(self, stream: Union[bytes, IO[bytes], Text, IO[Text]]):
        self._stream = stream

    T = TypeVar("T")

    def decode(self, out_type: T) -> T:
        """Decodes a stream into a dataclass.

        Args:
            out_type (T): out_type should be the type of your dataclass you want to decode your yaml stream into

        Raises:
            ValueError: if out_type is not a dataclass

        Returns:
            T: a dataclass of type = out_type
        """
        if not is_dataclass(out_type):
            raise ValueError(f"'{out_type.__class__.__name__}' is not a dataclass!")

        yaml_dict = yaml.safe_load(self._stream)
        node = MappingNode("", yaml_dict, out_type)
        return self._unmarshall(node)

    def _unmarshall(self, node: Node) -> T:
        if isinstance(node, MappingNode):
            result = self._mapping(node, node.out_type)
            res = node.out_type(**result)

        elif isinstance(node, SequenceNode):
            res = node.out_type(node.value)

        elif isinstance(node, ScalarNode):
            res = copy.deepcopy(node.value)

        elif isinstance(node, OptionalNoneNode):
            res = node.value

        else:
            raise TypeError(f"{node.name} is not of known type")

        if not Optional[type(res)] == node.out_type and not isinstance(
            res, node.out_type
        ):
            raise TypeError(f"{node.name}: {type(res)} must be of type {node.out_type}")

        return res

    def _mapping(self, mapping_node: MappingNode, out_type: type) -> dict:
        result = {}
        for yaml_name, child_value in mapping_node.value.items():
            child_name = mapping_node.yaml_names.get(yaml_name)
            if child_name:
                child_out_type = out_type.__annotations__[child_name]
                child = new_node(child_name, child_value, child_out_type)
                result[child_name] = self._unmarshall(child)

        return result

    def _sequence(self, sequence_node: SequenceNode, out_type: type):
        return out_type(sequence_node.value)
