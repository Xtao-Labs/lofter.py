import re


# Parse a dwr response and return a list of dict objects
def parse_dwr_string(dwr_string: str) -> list[dict]:
    # Add line break:
    string = re.sub(r"&nbsp;", r"\t", dwr_string)
    string = re.sub(r";", r"\n", string)

    # Remove js var declaration
    string = re.sub(r"\nvar (s\d+=)", r"\n\1", string)

    # Fix dict key appending syntax
    string = re.sub(r"\n(s\d+)\.([^=]*)=([^\n]*)", r"\n\1['\2']=\3", string)
    # Fix list appending syntax
    string = re.sub(r"\n(s\d+)\[\d+]=([^\n]*)", r"\n\1.append(\2)", string)

    # null to None, false to False, true to True
    string = re.sub(r"null", r"None", string)
    string = re.sub(r"=false\n", r"=False\n", string)
    string = re.sub(r"=true\n", r"=True\n", string)

    # Name the returned list
    string = re.sub(r"\ndwr[^\[]*(\[[^]]*]).*", r"\nresp=\1", string)

    # Remove fist two lines
    string = re.sub(r"//#DWR[^\n]*\n", r"\n", string)

    # Quote
    # Fix long content
    string = re.sub(r'\\"', r"'", string)
    # string = re.sub(r"\\'\n", r'"\n', string)
    string = re.sub(r"\\'\n(s\d+)", r'"\n\1', string)
    string = re.sub(r']="([^"]+)"\n', r']="""\1"""\n', string)
    string = re.sub(r"</p> *\\n", r"</p>\n", string)
    # string = re.sub(r'="""+\n', r'=""\n', string)
    # string = re.sub(r'=""("[^\n]*")""\n',r'=\1\n', string)

    # Fix surrogate error
    string = re.sub(
        r'(")(\)?)\n',
        r"\1.encode('utf-16','surrogatepass').decode('utf-16','ignore')\2\n",
        string,
    )

    # Setup an empty namespace and execute
    ns = {}
    exec(string, ns)

    return ns["resp"]
