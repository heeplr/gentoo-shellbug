#!/usr/bin/env python3

# generate bugreports from output.json

import json
import os

import shellbug


ISSUEFILE="output.json"
OUTDIR="./out"

if __name__ == "__main__":

    # create outdir if not existing
    os.makedirs(OUTDIR, exist_ok=True)

    # load issues
    with open(ISSUEFILE) as fd:
        issues = json.load(fd)

    # walk all packages
    for package, issuelist in issues.items():
        print(f"generating bug report for {package}...")

        msg = shellbug.bugreport(package, issuelist)

        with open(f"{OUTDIR}/{package.replace('/', '_')}.txt", "w") as fd:
            fd.write(msg)
