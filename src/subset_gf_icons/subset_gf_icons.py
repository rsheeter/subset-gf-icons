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

"""Subset a Google-style icon font.

Usage:
subset_gf_icons ~/Downloads/MaterialIcons-Regular.ttf menu
<writes font-subset.ttf>
"""
from absl import app
from fontTools import ttLib, subset
import uharfbuzz as hb


def _run(argv):
    assert len(argv) > 2, "Must specify at least a font and a single icon name"
    blob = hb.Blob.from_file_path(argv[1])
    face = hb.Face(blob)
    font = hb.Font(face)

    for icon_name in argv[2:]:
        buf = hb.Buffer()
        buf.add_str(icon_name)
        buf.guess_segment_properties()
        hb.shape(font, buf, {})

        infos = buf.glyph_infos
        assert len(infos) == 1, f"'{icon_name}' doesn't appear to be the name of a single icon"

        info = infos[0]
        print(f"{icon_name} gid {info.codepoint}")


def main(argv=None):
    # We don't seem to be __main__ when run as cli tool installed by setuptools
    app.run(_run, argv=argv)


if __name__ == "__main__":
    main()
