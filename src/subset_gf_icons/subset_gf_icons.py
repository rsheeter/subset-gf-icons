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

Subset by glyph id to avoid an over-large layout closure (e.g. alarm_on would
retain the alarm icon). If we subset by the glyph ids for the icon name(s)
plus the glyph ids of the targets of ligatures we should keep the activation
characters and the ligatures and nothing else.

Usage:
    subset_gf_icons ~/Downloads/MaterialIcons-Regular.ttf menu
    subset_gf_icons ~/Downloads/MaterialIcons-Regular.ttf menu alarm etc
"""
from absl import app
from absl import flags
from fontTools import ttLib, subset
from functools import reduce
import uharfbuzz as hb
from pathlib import Path


FLAGS = flags.FLAGS


# Input to https://github.com/fonttools/fonttools/blob/98242634c45cf4ca9f8aff6fd059de9dcf734471/Lib/fontTools/subset/__init__.py#L1821
class ClosureState:
    def __init__(self, glyphs):
        self.table = ""
        self.glyphs = glyphs


flags.DEFINE_enum(
    "flavor",
    None,
    ["woff", "woff2"],
    "Specify flavor of output font file. May be 'woff' or 'woff2'. If unspecified output is uncompressed.",
)


def _shape(hb_font, text):
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(hb_font, buf, {})
    return buf


def _run(argv):
    assert len(argv) > 2, "Must specify at least a font and a single icon name"
    in_file = Path(argv[1])
    assert in_file.is_file(), in_file

    blob = hb.Blob.from_file_path(in_file)
    face = hb.Face(blob)
    font = hb.Font(face)

    icon_names = set(argv[2:])

    # \n breaks any accidental ligature here. It will bring in 0 but we want notdef anyway so that's fine.
    name_chars = "\n".join(sorted(reduce(lambda a, e: a | set(e), icon_names, set())))

    gids = reduce(
        lambda a, e: a | {e.codepoint},
        _shape(font, name_chars).glyph_infos,
        set(),
    )

    tt_font = ttLib.TTFont(in_file)
    glyph_order = tt_font.getGlyphOrder()

    icon_glyph_names = set()

    for icon_name in icon_names:
        buf = hb.Buffer()
        buf.add_str(icon_name)
        buf.guess_segment_properties()
        hb.shape(font, buf, {})

        infos = buf.glyph_infos
        assert (
            len(infos) == 1
        ), f"'{icon_name}' doesn't appear to be the name of a single icon"

        info = infos[0]
        # the gid is in .codepoint
        gids.add(info.codepoint)
        icon_glyph_names.add(glyph_order[info.codepoint])

    # We do NOT want to close over all the gids of name chars, that results in a subset to "alarm_on"
    # including the glyph for "alarm" However, we DO want to close over the icon gids themselves to
    # ensure we include things like their contextual subs
    # See https://github.com/google/material-design-icons/issues/1201#issuecomment-1752180289 for why
    # this matters
    state = ClosureState(icon_glyph_names)
    tt_font["GSUB"].closure_glyphs(state)
    gids |= {tt_font.getGlyphID(gn) for gn in state.glyphs}

    options = subset.Options()
    options.layout_closure = False
    subsetter = subset.Subsetter(options)
    subsetter.populate(gids=gids)

    subsetter.subset(tt_font)

    out_file = in_file.parent / (in_file.stem + "-subset" + in_file.suffix)

    if FLAGS.flavor is not None:
        out_file = out_file.with_suffix("." + FLAGS.flavor)
        tt_font.flavor = FLAGS.flavor

    tt_font.save(out_file)

    print("Wrote subset to", out_file)


def main(argv=None):
    # We don't seem to be __main__ when run as cli tool installed by setuptools
    app.run(_run, argv=argv)


if __name__ == "__main__":
    main()
