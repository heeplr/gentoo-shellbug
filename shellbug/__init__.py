
def nth_line(filename, n, consecutive=0):
    """read nth line from textfile
    :param n: line number starting from 1
    :param filename: name of script
    :param consecutive: print additional lines after nth line
    """
    if n <= 0:
        return None

    result = []
    with open(filename) as fp:
        for i, line in enumerate(fp):
            if i >= n-1 and i < n+consecutive:
                result += [ line ]
            if i > n+consecutive:
                break

    return "".join(result).rstrip()

def result_to_str(result):
    """generate string for a shellcheck result"""
    text = ""

    # print portion of affected code
    code = nth_line(
            filename = result['file'],
            n = result['line'],
            consecutive = result['endLine']-result['line']
        ) + "\n"
    text += f"script: {result['file']}:{result['line']}:\n\n{code}"
    # print markers
    text += " " * (result['column'] - 1)  +  "^" * (result['endColumn'] - result['column']) + "\n"
    # print message
    text += f"{result['level']}: {result['message']} (https://github.com/koalaman/shellcheck/wiki/SC{result['code']})\n"
    # print fix
    if result['fix']:
        text += result['fix'] + "\n"

    return text

def bugreport(package, issues):
    msg = f"Shellckeck found errors in one or more shellscripts provided by {package}.\n" \
              f"To minimize false-positive findings, conservative settings were used. " \
              f"You might want to re-run shellcheck and check the complete output for more issues.\n" \
              f"Please check the findings below. A link to the shellcheck wiki " \
              f"will provide further details.\n"

    for issue in issues:
        msg += "\n------------------------------------------------\n"
        msg += result_to_str(issue)

    msg += "\nThis is an automated bug report.\n\n"
    msg += "References:\n"
    msg += "[1] this script: https://github.com/heeplr/gentoo-shellbug\n"
    msg += "[2] shellcheck: https://www.shellcheck.net/"

    return msg
