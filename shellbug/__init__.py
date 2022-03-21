
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
