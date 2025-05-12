from pywind import Pywind, z, Router

wind = Pywind()

registry = Router("registry")  # [], None
wind.useRouter(registry)

double = Router("double")
registry.useRouter(double)


@registry.use("get", {"path": z.string()}, z.number())
def getRegister(path: str):
    return 10


# print("wind.hierarchy: ", wind.hierarchy)
# print("wind.current: ", wind.current)

# print(registry.hierarchy)
# print(registry.current)

# print(double.hierarchy)
# print(double.current)


@double.use("fuck", {}, z.number())
def fuck():
    pass
