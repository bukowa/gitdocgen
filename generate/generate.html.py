import dataclasses
import json
import os
from dataclasses import dataclass, field

from bs4 import BeautifulSoup
from bs4 import Tag

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


@dataclass(init=False)
class Section:
    name: str = field(init=False)
    text: str = field(init=False)

    def __init__(self, tag: Tag):
        self._tag = tag
        self.name = self.tag.find("h2").text
        start_index = self.tag.text.index(self.name) + len(self.name)
        self.text = self.tag.text.lstrip()[start_index:].lstrip()

    @property
    def tag(self):
        return self._tag


class Synopsis(Section):
    ...


class Description(Section):
    ...


@dataclass
class Option:
    keys: list[str]
    info: str


class Options(Section):
    ...
    options: list[Option]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Examples(Section):
    ...


@dataclass
class Command:
    name: str
    synopsis: Synopsis = field(default=None)
    description: Description = field(default=None)
    options: Options = field(default=None)
    examples: Examples = field(default=None)

    @classmethod
    def new(cls, name: str, sections: list[Section]):
        kwargs = {"name": name}
        for sect in sections:
            for kk, vv in cls.__dataclass_fields__.items():
                klass = vv.type
                if sect.name == klass.__name__.upper():
                    kwargs[kk.lower()] = klass(tag=sect.tag)
        return cls(**kwargs)


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
        commands.append(Command.new(k, v))

    del data, html, k, v, docs, s

    class Encoder(json.JSONEncoder):
        def default(self, o):
            if dataclasses.is_dataclass(o):
                return dataclasses.asdict(o)
            return super().default(o)

    with open("gen", "w") as f:
        json.dump(commands, f, cls=Encoder)

# double values, remove last index
# ^[<-].*\n{3}^[-<].*\n{4}(.*\n)+?(^[-<])
# single values, remove last index
# ^[-<].*\n{4}(.*\n)+?(^[-<])

