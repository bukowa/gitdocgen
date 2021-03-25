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
            asd[doc.key] = {}
            for header in doc:
                asd[doc.key][header.name] = header.__dict__
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


@dataclass
class Header:
    name: str
    start_index: int
    end_index: int
    value: str = field(init=False)


@dataclass
class Headers(list):
    key: str
    raw: str


if __name__ == '__main__':
    d = Container()
    for k, v in collect_git_docs().items():
        h = Headers(
            key=k,
            raw=v,
        )
        for match in re.finditer("\\n[A-Za-z0-9]+\\n-+\\n", v):
            h.append(Header(
                name=v[match.regs[0][0]:match.regs[0][1]],
                start_index=match.regs[0][0],
                end_index=match.regs[0][1],
            ))
        d.append(h)

    d.do()
    with open("generated.json", "w") as f:
        json.dump(d.as_dict(), f, indent=4)
