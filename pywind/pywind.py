compiled = {}

from typing import Optional
from dataclasses import dataclass


@dataclass
class Hierarchy:
    current: str
    isRoot: bool = False


Root = Hierarchy(isRoot=True, current="root")

import json


def pprint(obj):
    print(json.dumps(obj, indent=4))


def set(hs: list[Hierarchy], p: str, input, output):

    target = compiled
    for h in hs:
        if h.current not in target:
            target[h.current] = {}
        target = target[h.current]

    target[p] = {
        "input": input,
        "output": output,
    }

    pprint(compiled)


class Pywind:

    hierarchy = list[Hierarchy]
    current: Hierarchy

    def __init__(self) -> None:
        self.hierarchy = [Root]
        self.current = Root

    def use(self, path: str, input: dict, output: dict):
        print("path: ", path)
        print("input: ", input)
        print("output: ", output)

        set(self.hierarchy, path, input, output)

        def internal_use(func):
            print(func)

        return internal_use

    def useRouter(self, router: "Router"):
        router.hierarchy = self.hierarchy.copy()
        router.hierarchy.append(router.current)


class Router(Pywind):

    def __init__(self, path: str) -> None:
        self.hierarchy = []
        self.current = Hierarchy(current=path)


from dataclasses import dataclass


@dataclass
class PodString:
    pass


@dataclass
class PodNumber:
    pass


class Pod:

    def string(self):
        return PodString()

    def number(self):
        return PodNumber()


z = Pod()
