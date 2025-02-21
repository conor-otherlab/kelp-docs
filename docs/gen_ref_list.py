#! /usr/bin/env python

from pathlib import Path

cwd = Path(__file__).parent
ref_dir = cwd / "references"

template = "* [{title}]({link} ':ignore')\n"

ref_files = ref_dir.glob("*")
ref_list = ""
for ref in ref_files:
    ref_list += template.format(
        title=ref.name, link=str(ref.relative_to(Path(__file__).parent))
    )

print(ref_list)
