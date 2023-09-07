# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup, find_packages


setup_args = dict(
    name="subset_gf_icons",
    use_scm_version={"write_to": "src/subset_gf_icons/_version.py"},
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    entry_points={
        "console_scripts": [
            "subset_gf_icons=subset_gf_icons.subset_gf_icons:main",
        ],
    },
    setup_requires=["setuptools_scm"],
    install_requires=[
        "absl-py>=1.4.0",
        "fonttools>=4.42.1",
        "uharfbuzz>=0.37.2",
    ],
    extras_require={
        "dev": [
            "pytest",
            "black==23.3.0",
        ],
    },
    # this is so we can use the built-in dataclasses module
    python_requires=">=3.9",
    # this is for type checker to use our inline type hints:
    # https://www.python.org/dev/peps/pep-0561/#id18
    package_data={"subset_gf_icons": ["py.typed"]},
    # metadata to display on PyPI
    author="Rod S",
    author_email="rsheeter@google.com",
    description=(
        "Exploratory utility to subset a Google-style icon font"
    ),
)


if __name__ == "__main__":
    setup(**setup_args)
