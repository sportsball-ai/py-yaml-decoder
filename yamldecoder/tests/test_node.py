from dataclasses import dataclass, field
from typing import Optional

import pytest

from yamldecoder.node import SequenceNode, new_node, MappingNode, ScalarNode


@dataclass
class ConfigTest:
    a: int = field(metadata={"yaml": "A"})
    b: float = field(metadata={"yaml": "B"})


@pytest.mark.parametrize(
    "test_input",
    [
        ({"a": 1, "b": 2}, ConfigTest),
    ],
)
def test_new_mapping_node(test_input):
    name = "test_node"
    value = test_input[0]
    out_type = test_input[1]
    node = new_node(name, value, out_type)

    assert isinstance(node, MappingNode)


@dataclass
class OptionalConfigTest:
    a: Optional[int] = field(metadata={"yaml": "A"})
    b: int = field(metadata={"yaml": "B"})


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (({"B": 2}, OptionalConfigTest), {"A": None, "B": 2}),
    ],
)
def test_mapping_optional_none_node(test_input, expected):
    name = "test_node"
    value = test_input[0]
    out_type = test_input[1]

    node = MappingNode(name, value, out_type)

    assert expected == node.value


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (({"A": 1, "B": 2}, OptionalConfigTest), {"A": "a", "B": "b"}),
    ],
)
def test_mapping_node_yaml_names(test_input, expected):
    name = "test_node"
    value = test_input[0]
    out_type = test_input[1]

    node = MappingNode(name, value, out_type)

    assert expected == node.yaml_names


@pytest.mark.parametrize(
    "test_input",
    [
        123,
        1.23,
        "foo",
    ],
)
def test_new_saclar_node(test_input):
    name = "test_node"
    value = test_input
    out_type = type(value)
    node = new_node(name, value, out_type)

    assert isinstance(node, ScalarNode)


@pytest.mark.parametrize(
    "test_input",
    [
        [1, 2, 3, 4, 5],
        (1, 2, 3, 4, 5),
    ],
)
def test_new_sequence_node(test_input):
    name = "test_node"
    value = test_input
    out_type = type(value)
    node = new_node(name, value, out_type)

    assert isinstance(node, SequenceNode)
