import os
from dataclasses import dataclass, field
from bs4 import Tag
from bs4 import BeautifulSoup

DOCS_DIR = os.path.join(os.path.dirname(__file__), "githtml")


def collect_git_html_docs() -> dict[str, str]:
    d = dict()
    for dirpath, dirnames, filenames in os.walk(DOCS_DIR):
        if dirpath == DOCS_DIR:
            for file in filenames:
                if file.startswith("git-") or file == "git.html":
                    if file.endswith(".html"):
                        with open(os.path.join(dirpath, file), "r") as f:
                            d[file] = f.read()
    return d


@dataclass
class Section:
    tag: Tag
    name: str = field(init=False)

    def __post_init__(self):
        self.name = self.tag.find("h2").text


if __name__ == '__main__':
    docs = collect_git_html_docs()
    sections = list()

    for k, v in docs.items():
        if k == "git-add.html":
            html = BeautifulSoup(v, "html.parser")
            for s in html.findAll("div", {"class": "sect1"}):
                sections.append(Section(s))
