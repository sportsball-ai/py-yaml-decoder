from setuptools import setup, find_packages


def readme():
    with open("README.md", "r", encoding="utf-8") as f:
        return f.read()


setup(
    name="yamldecoder",
    packages=find_packages(),
    include_package_data=True,
    description="A python Yaml to dataclass decoder",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author="Tempus Ex Machina",
    install_requires=["pyyaml"],
    python_requires=">=3.8",
)
