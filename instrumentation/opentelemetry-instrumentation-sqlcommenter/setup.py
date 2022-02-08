# Copyright The OpenTelemetry Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# DO NOT EDIT. THIS FILE WAS AUTOGENERATED FROM templates/instrumentation_setup.py.txt.
# RUN `python scripts/generate_setup.py` TO REGENERATE.


import distutils.cmd
import json
import os
from configparser import ConfigParser

import setuptools

config = ConfigParser()
config.read("setup.cfg")

# We provide extras_require parameter to setuptools.setup later which
# overwrites the extra_require section from setup.cfg. To support extra_require
# secion in setup.cfg, we load it here and merge it with the extra_require param.
extras_require = {}
if "options.extras_require" in config:
    for key, value in config["options.extras_require"].items():
        extras_require[key] = [v for v in value.split("\n") if v.strip()]

BASE_DIR = os.path.dirname(__file__)
PACKAGE_INFO = {}

VERSION_FILENAME = os.path.join(
    BASE_DIR,
    "src",
    "opentelemetry",
    "instrumentation",
    "sqlcommenter",
    "version.py",
)
with open(VERSION_FILENAME, encoding="utf-8") as f:
    exec(f.read(), PACKAGE_INFO)

PACKAGE_FILENAME = os.path.join(
    BASE_DIR,
    "src",
    "opentelemetry",
    "instrumentation",
    "sqlcommenter",
    "package.py",
)
with open(PACKAGE_FILENAME, encoding="utf-8") as f:
    exec(f.read(), PACKAGE_INFO)

# Mark any instruments/runtime dependencies as test dependencies as well.
extras_require["instruments"] = PACKAGE_INFO["_instruments"]
test_deps = extras_require.get("test", [])
for dep in extras_require["instruments"]:
    test_deps.append(dep)

extras_require["test"] = test_deps


class JSONMetadataCommand(distutils.cmd.Command):

    description = (
        "print out package metadata as JSON. This is used by OpenTelemetry dev scripts to ",
        "auto-generate code in other places",
    )
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        metadata = {
            "name": config["metadata"]["name"],
            "version": PACKAGE_INFO["__version__"],
            "instruments": PACKAGE_INFO["_instruments"],
        }
        print(json.dumps(metadata))


setuptools.setup(
    cmdclass={"meta": JSONMetadataCommand},
    version=PACKAGE_INFO["__version__"],
    extras_require=extras_require,
)
