#!/usr/bin/env python3

# generate bugreports from output.json

import json

import shellbug


ISSUEFILE="output.json"
OUTDIR="out"

if __name__ == "__main__":

    # load issues
    with open(ISSUEFILE) as fd:
        issues = json.load(fd)

    # walk all packages
    for package, issuelist in issues.items():
        print(f"generating bug report for {package}...")

        msg = f"Shellckeck found errors in one or more shellscripts provided by {package}.\n" \
              f"To minimize false-positive findings, conservative settings were used. " \
              f"You might want to re-run shellcheck and check the complete output for more issues.\n" \
              f"Please check the findings below. A link to the shellcheck wiki " \
              f"will provide further details on every issue found.\n"

        for issue in issuelist:
            msg += "\n------------------------------------------------\n"
            msg += shellbug.result_to_str(issue)

        msg += "\nThis is an automated bug report.\n"
        msg += "References:\n"
        msg += "[1] this script: https://github.com/heeplr/gentoo-shellbug\n"
        msg += "[2] shellcheck: https://www.shellcheck.net/"

        print(msg)
        break
