from setuptools import setup, find_packages

setup(
    name="general-inquirer-remix",
    version="0.1",
    packages=["general_inquirer"],
    description="This is a version of the General Inquirer (GI) that operates as a spaCy extension.",
    author="pmbaumgartner",
    url="https://github.com/pmbaumgartner/general-inquirer-remix",
    install_requires=["spacy"],
    python_requires=">=3.6",
)
