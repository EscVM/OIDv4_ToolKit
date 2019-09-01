import pathlib
from setuptools import setup

# the directory containing this file
BASE_DIR = pathlib.Path(__file__).parent

# the text of the README file
README = (BASE_DIR / "README.md").read_text()

setup(
    name="OIDv4_ToolKit",
    version="1.0.0",
    url="https://github.com/EscVM/OIDv4_ToolKit",
    license="GPL3",
    author="Vittorio, Angelo",
    author_email="EscVM@github.com",
    description=(
        "Toolkit to facilitate the download and usage of "
        "the Open Images Dataset (v4)."
    ),
    long_description=README,
    long_description_content_type="text/markdown",
    packages=["modules"],
    include_package_data=True,
    install_requires=[
        "awscli",
    ],
    keywords=[
        "openimages",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    entry_points={
        "console_scripts": [
            "oidv4_toolkit = modules.__main__:main",
        ],
    }
)
