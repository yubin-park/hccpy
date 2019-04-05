from setuptools import setup, find_packages

setup(packages=find_packages(),
    name="hccpy",
    version="0.0.1",
    description="hccpy is a Python implementation of HCC",
    author="Yubin Park",
    author_email="yubin.park@gmail.com",
    url="",
    license="Apaceh 2.0", 
    include_package_data=True,
    package_data={"": ["*.TXT", "*.csv"]})


