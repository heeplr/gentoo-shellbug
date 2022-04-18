#!/usr/bin/env python3

# post bugreports to bugs.gentoo.org

import bugzilla
import click
import json
import os

import shellbug

URL = "bugs.gentoo.org"
ISSUEFILE="output.json"
OUTDIR = "./posted"


def postbug(bzapi, package, issues):
    buginfo = bzapi.build_createbug(
        product="Gentoo Linux",
        version="unspecified",
        component="Current packages",
        summary=f"{package}: automated shellcheck found errors",
        description = shellbug.bugreport(package, issues),
        platform="All",
        op_sys="Linux"
    )

    bug = bzapi.createbug(buginfo)
    # save bugreport
    with open(f"{OUTDIR}/{package.replace('/', '_')}.txt", "w") as fd:
        fd.write("")
    print(f"Created new bug id={bug.id} url={bug.weburl}")
    return bug


@click.option(
    "-p",
    "--password",
    prompt=True,
    hide_input=True,
    show_envvar=True,
    help="secret password"
)
@click.option(
    "-u",
    "--username",
    prompt=True,
    show_envvar=True,
    help="login id"
)
@click.command()
def postbugs(username, password):
    # create outdir if not existing
    os.makedirs(OUTDIR, exist_ok=True)

    # load issues
    with open(ISSUEFILE) as fd:
        issues = json.load(fd)

    # connect to bugzilla
    bzapi = bugzilla.Bugzilla(URL)
    if not bzapi.logged_in:
        bzapi.interactive_login(user=username, password=password)

    # walk all packages
    for package, issuelist in issues.items():
        print(f"posting bug report for {package}...")
        # post bugreport
        bug = postbug(bzapi, package, issuelist)

if __name__ == "__main__":
    postbugs()
