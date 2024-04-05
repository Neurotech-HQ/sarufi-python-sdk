from os import path
from setuptools import setup

# read the contents of your description file

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "description.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="sarufi",
    version="0.1.9",
    description="Opensource python wrapper to Sarufi Conversation API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Neurotech-HQ/sarufi-python-sdk",
    download_url="https://github.com/Neurotech-HQ/sarufi-python-sdk/archive/refs/tags/v0.0.2.tar.gz",
    author="Jordan Kalebu",
    author_email="isaackeinstein@gmail.com",
    license="MIT",
    packages=["sarufi"],
    install_requires=["requests", "pyyaml"],
    keywords=[
        "sarufi",
        "Sarufi Python SDK",
        "Conversation API python",
        "Swahili Conversational API",
        "Conversational platform Python",
    ],
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
