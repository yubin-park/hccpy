from setuptools import setup

NAME = "hccpy"
VERSION = "0.0.1"
DESCR = "hccpy is a Python implementation of HCC"
URL = ""
LICENSE = "Apache 2.0"
AUTHOR = "Yubin Park"
EMAIL = "yubin.park@gmail.com"
SRC_DIR = "hccpy"
PACKAGES = [SRC_DIR]

if __name__=="__main__":
    setup(packages=PACKAGES,
            name=NAME,
            version=VERSION,
            description=DESCR,
            author=AUTHOR,
            url=URL,
            license=LICENSE)


