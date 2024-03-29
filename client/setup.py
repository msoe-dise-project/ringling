"""
Copyright 2023 MSOE DISE Project

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from setuptools import setup

setup(name="ringling-cli",
      version="1.0",
      description="Client and Library for Ringling",
      author="MSOE DISE Project",
      author_email="nowling@msoe.edu",
      license="Apache License, Version 2.0",
      zip_safe=False,
      packages=["ringling", "ringling_lib"],
      python_requires=">=3.8, <3.12",
      install_requires=["requests"],
      scripts=["bin/ringling-cli"])
