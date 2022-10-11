import re
from pathlib import Path
from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

path = Path(__file__).parent / "thino" / "__init__.py"
version = re.search(r'\d[.]\d[.]\d',path.read_text()).group(0) #type: ignore

packages = [
    'thino'
]


setup(
    name='osu.py',
    author='SawshaDev',
    version=version,
    packages=packages,
    license='MIT',
    description='An asynchronous python wrapper around the osu API!',
    install_requires=requirements,
    python_requires='>=3.8.0',
)