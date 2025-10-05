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

__all__ = ["FlutterURLProvider"]

FEED_URL = "https://storage.googleapis.com/flutter_infra_release/releases/releases_macos.json"

class FlutterURLProvider(URLGetter):
    """Provides the download URL and version number for the latest version of Flutter."""

    input_variables = {
        "arch": {
            "description": "Architecture, can be arm64 or x64",
            "required": True
        },
        "channel": {
            "description": "Release channel to use, can be stable, beta, or dev.",
            "required": True
        }
        
    }
    output_variables = {
        "url": {
            "description": "Download URL for the latest version of Unity 3D."
        },
        "version": {
            "description": "Latest full version number of Unity 3D."
        }
    }
    description = __doc__

    def main(self):
        try:
            json_string = self.download(FEED_URL, text=True)
        except Exception as e:
            raise ProcessorError("Can't download %s: %s" % (FEED_URL, e))

        root = json.loads(json_string)
        base_url = root['base_url']
        current_release = root['current_release'][self.env['channel']]
        releases = root['releases']
        release = [x 
                   for x in releases 
                   if x['hash'] == current_release
                   and x['channel'] == self.env['channel']
                   and x['dart_sdk_arch'] == self.env['arch']][0]
        version = release['version']

        self.env["version"] = version
        self.env["url"] = base_url+"/"+release['archive']
        self.output("Found download URL: %s" % self.env['url'])

if __name__ == "__main__":
    processor = FlutterURLProvider()
    processor.execute_shell()
