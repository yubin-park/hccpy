from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(packages=find_packages(),
    name="hccpy",
    version="0.1.3",
    description="hccpy is a Python implementation of HCC",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Yubin Park",
    author_email="yubin.park@gmail.com",
    url="https://github.com/yubin-park/hccpy",
    license="Apache 2.0", 
    install_requires = ["numpy"],
    include_package_data=True,
    package_dirc={"": "hccpy"},
    package_data={"data": ["*.TXT", "*.csv", "*.json"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent"
    ])


