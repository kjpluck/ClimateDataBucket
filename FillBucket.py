'Here is the docstring'
import pkgutil
import contributions
PACKAGE = contributions

for importer, modname, ispkg in pkgutil.iter_modules(PACKAGE.__path__):
    print("Found submodule %s (is a package: %s)" % (modname, ispkg))
    theModule = importer.find_module(modname).load_module(modname)
    print(theModule.__doc__)
    func = getattr(theModule, "get")
    print(func.__doc__)
    func()
