#!/usr/bin/env python
#
# Copyright 2026 Dan Kuehling, based on work by Allister Banks and Hannes Juutilainen
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

__all__ = ["iAURLProvider"]

class iAURLProvider(URLGetter):
    """Provides the download URL for the latest version of iA's apps."""

    input_variables = {
        "type": {
            "description": "Download type. Can be writer, writer-windows, or presenter",
            "required": True
        }
    }
    output_variables = {
        "url": {
            "description": "Download URL for the latest version of the iA product."
        }
    }
    description = __doc__

    def main(self):
        if "writer" in self.env['type']:
            code = "writer-download"
        elif "presenter" in self.env['type']:
            code = "presenter-landing"
        
        api_url = f"https://ia.net/download?type={self.env['type']}&code={code}&start=1"

        try:
            json_string = self.download(api_url, text=True)
        except Exception as e:
            raise ProcessorError(f"Can't download {api_url}: {e}")

        root = json.loads(json_string)
        download_url = root['file']
        self.env["url"] = download_url
        self.output(f"Found download URL: {self.env['url']}")

if __name__ == "__main__":
    processor = iAURLProvider()
    processor.execute_shell()
