#!/usr/bin/env bash
/usr/bin/python setup.py py2app -O2

echo "Unzipping Template DMG..."
bunzip2 -c template.dmg.bz2 > dist/temp.dmg
echo "Mount template_dmg/temp.dmg file, copy the DEEPN.app file to the mounted DEEPN folder, unmount temp.dmg, compress temp.dmg (using Disk Utility) and delete temp .dmg and DEEPN.app file."