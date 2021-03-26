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
    text: str = field(init=False)

    def __post_init__(self):
        self.name = self.tag.find("h2").text
        start_index = self.tag.text.index(self.name) + len(self.name)
        self.text = self.tag.text.lstrip()[start_index:].lstrip()


@dataclass
class Synopsis(Section):
    ...


@dataclass
class Description(Section):
    ...


@dataclass
class Options(Section):
    ...


@dataclass
class Examples(Section):
    ...


@dataclass
class Command:
    name: str
    sections: list[Section]

    synopsis: Synopsis = field(init=False)
    description: Description = field(init=False)
    options: Options = field(init=False)

    def __post_init__(self):
        for sect in self.sections:
            for kk, vv in self.__dataclass_fields__.items():
                klass = vv.type
                if sect.name == klass.__name__.upper():
                    self.__setattr__(kk.lower(), klass(tag=sect.tag))


if __name__ == '__main__':
    docs = collect_git_html_docs()
    data = {}

    for k, v in docs.items():
        data[k] = []
        html = BeautifulSoup(v, "html.parser")
        for s in html.findAll("div", {"class": "sect1"}):
            data[k].append(Section(s))

    commands = []

    for k, v in data.items():
        commands.append(Command(
            name=k,
            sections=v,
        ))
