
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
    text += f"script: {result['file']}:{result['line']}\n\n{code}"
    # print markers
    text += " " * (result['column'] - 1)  +  "^" * (result['endColumn'] - result['column']) + "\n"
    # print message
    text += f"{result['level']}: {result['message']} (https://github.com/koalaman/shellcheck/wiki/SC{result['code']})\n"
    # print fix
    if result['fix']:
        text += result['fix'] + "\n"

    return text

def bugreport(package, issues):
    msg = f"Shellckeck found errors in one or more shellscripts provided by {package}.\n\n" \
          f"Kindly refer to the findings below and the shellcheck wiki for further details:\n" \

    for issue in issues:
        msg += "\n------------------------------------------------\n"
        msg += result_to_str(issue)

    msg += f"\nThis is an automated bug report. Conservative settings were used to minimize false-positives but there's still a chance that the above list contains non-issues.\n" \
           f"Running shellcheck again with default settings could detect other possible issues.\n\n"
    msg += "References:\n"
    msg += "[1] this script: https://github.com/heeplr/gentoo-shellbug\n"
    msg += "[2] shellcheck: https://www.shellcheck.net/"

    return msg
