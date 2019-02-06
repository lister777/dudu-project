from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="dudu",
    version="0.0.1",
    author="Jack X",
    author_email="linghuax@gmail.com",
    description="A small ec2 management package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lister777/dudu",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['boto3'],
    scripts=['bin/dudu'],
)