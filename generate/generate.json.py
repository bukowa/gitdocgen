import json
import os
import re
from dataclasses import dataclass, field

DOCS_DIR = os.path.join(os.path.dirname(__file__), "git", "Documentation")


def collect_git_docs() -> dict[str, str]:
    d = dict()
    for dirpath, dirnames, filenames in os.walk(DOCS_DIR):
        if dirpath == DOCS_DIR:
            for file in filenames:
                if file.startswith("git-") or file == "git.txt":
                    if file.endswith(".txt"):
                        with open(os.path.join(dirpath, file), "r") as f:
                            d[file] = f.read()
    return d


@dataclass
class Container(list):

    def as_dict(self) -> dict:
        asd = {}
        for doc in self:
            asd[doc.file_name] = {}
            for header in doc:
                asd[doc.file_name][header.name] = header.__dict__
        return asd

    def do(self):
        doc: Headers
        header: Header

        for doc in self:
            for i, header in enumerate(doc):
                if i == len(doc) - 1:
                    header.value = doc.raw[header.end_index:]
                    continue
                next_: Header = doc[i + 1]
                header.value = doc.raw[header.end_index:next_.start_index]
                continue

    def do_options(self):
        doc: Headers
        header: Header
        for doc in self:
            for i, header in enumerate(doc):
                if header.name == "OPTIONS":
                    if not header.value.startswith("\n"):
                        header.value = "\n" + header.value



@dataclass
class Option:
    key: str
    value: str
    description: str

    def __repr__(self):
        return self.key


@dataclass
class Header:
    name: str
    start_index: int
    end_index: int
    value: str = field(init=False)
    options: list[Option] = field(init=False)

    def __repr__(self):
        return self.name


@dataclass
class Headers(list):
    file_name: str
    raw: str

    def __repr__(self):
        return self.file_name


if __name__ == '__main__':
    d = Container()
    for k, v in collect_git_docs().items():
        h = Headers(
            file_name=k,
            raw=v,
        )
        for match in re.finditer("\\n[A-Za-z0-9]+\\n-+\\n", v):
            h.append(Header(
                name=v[match.regs[0][0]:match.regs[0][1]].rsplit()[0],
                start_index=match.regs[0][0],
                end_index=match.regs[0][1],
            ))
        d.append(h)

    d.do()
    d.do_options()
    with open("generated.json", "w") as f:
        json.dump(d.as_dict(), f, indent=4)

