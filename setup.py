import os
from setuptools import setup, find_packages

DISTNAME = 'rpy2deseq'
VERSION = '0.1.0'
DESCRIPTION = "Python wrapper for R DESeq2"
MAINTAINER = 'Chris Jackson'
MAINTAINER_EMAIL = 'cj59@nyu.edu'
URL = 'https://github.com/GreshamLab/rpy2deseq'
LICENSE = 'MIT'

# Description from README.md
base_dir = os.path.dirname(os.path.abspath(__file__))
long_description = "\n\n".join([open(os.path.join(base_dir, "README.md"), "r").read()])

setup(name=DISTNAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url=URL,
      author=MAINTAINER,
      author_email=MAINTAINER_EMAIL,
      license=LICENSE,
      packages=find_packages(include=['rpy2deseq', "rpy2deseq.*"]),
      install_requires=['numpy', 'pandas', 'rpy2'],
      tests_require=['pytest', 'coverage'],
      zip_safe=True,
      classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Development Status :: 4 - Beta"
      ]
)