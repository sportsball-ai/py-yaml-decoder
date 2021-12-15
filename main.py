from pprint import pprint
from dataclasses import dataclass, field

from yamldecoder import YamlDecoder


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


def load_config() -> Config:
    """This opens up the `config.yaml` file and decodes it into `Config`

    Returns:
        Config: the decoded yaml file
    """
    with open("config.yaml", "r", encoding="utf8") as stream:
        return YamlDecoder(stream).decode(Config)


if __name__ == "__main__":
    cfg = load_config()
    pprint(cfg)
