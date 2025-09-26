#!/usr/bin/env python
#
# Copyright 2023 Dan Kuehling, based on work by Allister Banks and Hannes Juutilainen
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

from __future__ import absolute_import
import json
from autopkglib import Processor, ProcessorError, URLGetter

__all__ = ["Unity3DURLProvider"]

FEED_URL = "https://services.api.unity.com/unity/editor/release/v1/releases?version="

class Unity3DURLProvider(URLGetter):
    """Provides the download URL and full version number for the latest version of Unity 3D."""

    input_variables = {
        "major_version": {
            "description": "Yearly or other major version of Unity 3D (four digits).",
            "required": True
        },
        "arch": {
            "description": "Architecture, can be arm64 or x86_64",
            "required": True
        }
        
    }
    output_variables = {
        "url": {
            "description": "Download URL for the latest version of Unity 3D."
        },
        "version": {
            "description": "Latest full version number of Unity 3D"
        }
    }
    description = __doc__

    def main(self):
        try:
            json_string = self.download(FEED_URL+self.env['major_version'], text=True)
        except Exception as e:
            raise ProcessorError("Can't download %s: %s" % (FEED_URL, e))

        root = json.loads(json_string)
        latest = [x for x in root['results'] if x['stream'] == "SUPPORTED"][0]
        version = latest['version']
        arch = self.env['arch'].upper()
        mac = [x for x in latest['downloads'] if x['platform'] == "MAC_OS" if x['architecture'] == arch][0]

        self.env["version"] = version
        self.env['url'] = mac['url']
        self.output("Found download URL: %s" % self.env['url'])

if __name__ == "__main__":
    processor = Unity3DURLProvider()
    processor.execute_shell()
