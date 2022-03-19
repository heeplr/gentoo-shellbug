#!/usr/bin/env python3

# run shellcheck over shell scripts in portage tree

import collections
import glob
import json
import os
import re
import subprocess

import shellbug


OUTFILE = "output.json"
PORTDIR = "/usr/portage/**"
SHEBANGS = [
    r"^#![\s]*/bin/bash$",
    r"^#![\s]*/bin/sh$",
    r"^#![\s]*/usr/bin/env bash$",
    r"^#![\s]*/usr/bin/env sh$"
]


def strip_false_positives(results):
    """remove known false positives from list of results"""
    cleaned = []

    #import pdb;pdb.set_trace()
    for r in results:
        # strip unusued warnings for known variables
        # ~ if r['code'] == 2034:
            # ~ # get first word of message, is varname
            # ~ varname = r['message'].split()[0]
            # ~ if varname in UNUSED_OK:
                # ~ # skip this warning
                # ~ continue
        # pass this warning
        cleaned += [ r ]

    return cleaned

def shellcheck(filename, include=[], exclude=[ "SC2068" ], severity="error"):
    """
    execute shellcheck on a script
    :param filename: name of script
    :param exclude: list of shellcheck checks to exclude
    """
    include_arg = [ "--include" if include else "" ] + [ ",".join(include) ]
    exclude_arg = [ "--exclude" if exclude else "" ] + [ ",".join(exclude) ]
    process = subprocess.Popen(
        [
            "/usr/bin/shellcheck",
            "--format", "json",
            "--severity", severity
        ] + exclude_arg + [ filename ],
        stdout=subprocess.PIPE)
    (out, err) = process.communicate()
    exitcode = process.wait()
    # parse output
    results = json.loads(out)
    # strip false positives
    results = strip_false_positives(results)
    if results:
        # could be multiple results?
        for res in results:
            # parse package atom
            path = res['file'].split("/")
            res['atom'] = path[3] + "/" + path[4]

    return exitcode, results, err


if __name__ == "__main__":
    # dict of shellcheck results per package
    packages = collections.defaultdict(list)

    # walk portage tree and build list of candidate files
    filelist = []
    print(f"scanning \"{PORTDIR}\"...")
    for filename in glob.glob(PORTDIR, recursive=True):
        # skip out non-files
        if not os.path.isfile(filename):
            continue

        # skip by path content?
        if any(portion in filename for portion in [
            ".git", "/distfiles/"
        ]):
            continue
        # skip by suffix?
        if any(filename.endswith(suffix) for suffix in [
            ".gz", ".patch", ".diff"
        ]):
            continue


        # got an ebuild?
        if filename.endswith(".ebuild"):
            # remember
            filelist += [ filename ]
            continue

        # read first line of file
        with open(filename) as f:
            try:
                firstline = f.readline()
            except UnicodeDecodeError as e:
                # ~ print(f"decode error \"{filename}\": {e}")
                continue

        # got a shebang?
        if any(re.match(shebang, firstline) for shebang in SHEBANGS):
            filelist += [ filename ]

    # check files
    for filename in filelist:
        print(f"shellchecking \"{filename}\"...")
        exitcode, results, err = shellcheck(filename, exclude=[
            "SC2068", "SC2148", "SC2034", "SC2145", "SC1081"
        ])
        for res in results:
            # output
            print(shellbug.result_to_str(res))

            # aggregate packages
            packages[res['atom']] += [ res ]

    # save bugreports
    with open(OUTFILE, "w+") as fd:
        json.dump(packages, fd, indent=4)
