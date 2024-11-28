import re
from bs4 import BeautifulSoup


def get_blogs_from_htmls(htmls):
    blog_part = re.compile(r"https?://[^.]*\.lofter\.com")
    req_blogs = set()
    for html in htmls:
        soup = BeautifulSoup(html, "lxml")
        for atag in soup.findAll("a", {"href": True}):
            href = atag["href"]
            req_blog = blog_part.findall(href)
            if req_blog:
                req_blogs.add(req_blog[0].replace("http:", "https:"))
    return list(req_blogs)


def get_domain(url):
    return re.sub(r"https?://([^/]*).*", r"\1", url)


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


def fix_tags(tag_list):
    tags = [tag.replace("\xa0", r" ").lower() for tag in tag_list]
    return tags
