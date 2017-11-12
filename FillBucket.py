'Here is the docstring'
import sys
import os
import pkgutil
import importlib
import threading
import contributions
from contributions import shared
PACKAGE = contributions

shared.set_refresh_files(False)

CONTRIBUTIONS_TO_EXECUTE = sys.argv[1:]


def _check_all_contributions_listed_exist():

    for a_contribution_to_execute in CONTRIBUTIONS_TO_EXECUTE:
        head, filename = os.path.split(a_contribution_to_execute)
        _, extension = os.path.splitext(filename)
        head, _ = os.path.split(head)
        head, should_be_contributions = os.path.split(head)
        if should_be_contributions != "contributions":
            print(a_contribution_to_execute + " should look like '."
                  + os.path.sep + "contributions"
                  + os.path.sep + "package_name"
                  + os.path.sep + "name.py'")
            exit()

        if extension != ".py":
            print(a_contribution_to_execute + " must be a .py file")
            exit()

    for a_contribution_to_execute in CONTRIBUTIONS_TO_EXECUTE:
        if not os.path.exists(a_contribution_to_execute):
            print(a_contribution_to_execute + " doesn't exists")
            exit()



def _make_module_name_from_path(a_contribution_to_execute):
    tail, contribution_name = os.path.split(a_contribution_to_execute)
    contribution_name, _ = os.path.splitext(contribution_name)
    _, package_name = os.path.split(tail)

    return "." + package_name +"."+contribution_name

if CONTRIBUTIONS_TO_EXECUTE:

    _check_all_contributions_listed_exist()

    for contribution_to_execute in CONTRIBUTIONS_TO_EXECUTE:
        module_name = _make_module_name_from_path(contribution_to_execute)
        the_contribution = importlib.import_module(module_name, "contributions")
        the_contribution.download()
else:

    for importer, modname, ispkg in pkgutil.walk_packages(PACKAGE.__path__):

        print("Found submodule %s (is a package: %s)" % (modname, ispkg))

        theModule = importer.find_module(modname).load_module(modname)

        if not ispkg and modname != "shared":
            print(theModule.__doc__)

            func = getattr(theModule, "download")

            print(func.__doc__)

            threading.Thread(target=func).start()
