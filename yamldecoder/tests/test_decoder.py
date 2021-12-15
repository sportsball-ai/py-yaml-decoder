from dataclasses import dataclass, field
from typing import Optional

import pytest

from yamldecoder import YamlDecoder

# pylint: disable=redefined-outer-name


@dataclass
class ConfigB:
    a: int = field(metadata={"yaml": "A"})
    b: float = field(metadata={"yaml": "B"})
    c: str = field(metadata={"yaml": "C"})
    d: tuple = field(metadata={"yaml": "D"})
    e: list = field(metadata={"yaml": "E"})


@dataclass
class Config:
    config_b: ConfigB = field(metadata={"yaml": "ConfigB"})


@pytest.fixture
def expected():
    return Config(
        config_b=ConfigB(
            a=1,
            b=1.0,
            c="test",
            d=(1, 2, 3, 4, 5),
            e=[1, 2, 3, 4, 5],
        )
    )


def test_yaml_decoder(expected):
    yaml_stream = """
    ConfigB:
        A: 1
        B: 1.0
        C: "test"
        D: [1,2,3,4,5]
        E: [1,2,3,4,5]
    """

    cfg = YamlDecoder(yaml_stream).decode(Config)

    assert expected == cfg


def test_yaml_decoder_extra_values(expected):
    yaml_stream = """
    NotAConfig:
        foo: bar
    ConfigB:
        A: 1
        B: 1.0
        C: "test"
        D: [1,2,3,4,5]
        E: [1,2,3,4,5]
    """

    cfg = YamlDecoder(yaml_stream).decode(Config)

    assert expected == cfg


@dataclass
class OptionalTestDataClass:
    a: Optional[int] = field(metadata={"yaml": "A"})
    b: int = field(metadata={"yaml": "B"})


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("B: 2", OptionalTestDataClass(a=None, b=2)),
        (
            """
            A: 1
            B: 2
        """,
            OptionalTestDataClass(a=1, b=2),
        ),
    ],
)
def test_yaml_decoder_optional_values(test_input, expected):
    yaml_stream = test_input

    cfg = YamlDecoder(yaml_stream).decode(OptionalTestDataClass)

    assert expected == cfg
