'Here is the docstring'
import pkgutil
import threading
import contributions
PACKAGE = contributions

for importer, modname, ispkg in pkgutil.walk_packages(PACKAGE.__path__):

    print("Found submodule %s (is a package: %s)" % (modname, ispkg))

    theModule = importer.find_module(modname).load_module(modname)

    if not ispkg and modname != "shared":
        print(theModule.__doc__)

        func = getattr(theModule, "get")

        print(func.__doc__)

        threading.Thread(target=func).start()
