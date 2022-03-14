# YamlDecoder :goggles:

This is a simple python package to decode yaml files into dataclasses with type check.

This works similarly to the [yaml decoder](https://pkg.go.dev/gopkg.in/yaml.v2) package in Go.

## Using This Module

Run this commmand in any python project you are working on (as long as it uses pipenv):

```bash
# for a specific commit version
pipenv install -e git+https://github.com/sportsball-ai/py-yaml-decoder.git@<commit-id>d#egg=yamldecoder
# for the latest version
pipenv install -e git+https://github.com/sportsball-ai/py-yaml-decoder#egg=yamldecoder
```

## Using The Decoder

A fully working example is available here [example.py](example.py).

### Getting Started

The `yamldecoder` is very easy to use. Here is a example snippet of how it works:

```python
from pprint import pprint
from dataclasses import dataclass, field

from yamldecoder import YamlDecoder


@dataclass
class Config:
    a: int = field(metadata={"yaml": "A"})
    b: float = field(metadata={"yaml": "B"})
    c: str = field(metadata={"yaml": "C"})


yaml_stream = """
A: 1
B: 1.0
C: "test"
"""

cfg = YamlDecoder(yaml_stream).decode(Config)
pprint(cfg)
```

There are two main parts to this code:

The first part consists in creating a dataclass:

```python
@dataclass
class Config:
    a: int = field(metadata={"yaml": "A"})
    b: float = field(metadata={"yaml": "B"})
    c: str = field(metadata={"yaml": "C"})
```

In the code snippet above we are telling the `YamlDecoder` that we want to decode 3 fields `a`, `b` and `c`, each with their own type. We are also telling the decoder what the field name key will be in the yaml stream (this is done by setting a field metadata: `= field(metadata={"yaml": "A"})`). For example, the field`A: 1` will map to `a: int` in the dataclass.

The second part consists in calling the decoder:

```python
cfg = YamlDecoder(yaml_stream).decode(Config)
```

This snippet should be pretty straight forward. We are telling the decoder to read the yaml string in `yaml_stream` and decode it using the "schema" define in the dataclass `Config`. This returns a dataclass of type `Config`.

If any value is missing in the yaml, the corresponding class field will be set to `None`.

### Recursively Using Dataclasses

You can use a dataclass inside a dataclass to recursively decode values in a yaml stream.

For example:

```python
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


yaml_stream = """
ConfigB:
  A: 1
  B: 1.0
  C: "test"
  D: [1,2,3,4,5]
  E: [1,2,3,4,5]
"""

cfg = YamlDecoder(yaml_stream).decode(Config)
pprint(cfg)
```

### Reading From A File

You can decode a yaml file directly like this:

```python
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
```
