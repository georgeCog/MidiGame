from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="midigame",
    version="0.0.0",
    description="Utilities for using MIDI devices to automate input.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"":"midigame"},
    packages=find_packages(where="midigame"),
    python_requires=">=3.10, <4",
    install_requires=[
        "py-midi >=2.0.1"
    ]
)