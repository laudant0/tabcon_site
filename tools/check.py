"""Reports local links/assets that don't exist. Run from repo root: python tools/check.py"""
import os
import pathlib
import re

bad = 0
for p in pathlib.Path(".").glob("*.html"):
    t = p.read_text(encoding="utf-8")
    for m in set(re.findall(r'(?:src|href)="(?!http|#|mailto|tel)([^"]+)"', t)):
        path = m.split("#")[0]
        # exact-case check so it also works on case-sensitive hosts
        parts = path.split("/")
        cur = "."
        ok = True
        for part in parts:
            if part not in os.listdir(cur):
                ok = False
                break
            cur = os.path.join(cur, part)
        if not ok:
            bad += 1
            print(p.name, "MISSING", m)
print("problems:", bad)
