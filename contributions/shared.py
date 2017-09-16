'shared module'
import os
import urllib.request
from urllib.parse import urlparse
import inspect

def hello():
    'hello function'
    print("Hello from shared")


def download_data(url):
    calling_frame = inspect.stack()[1]
    calling_module = inspect.getmodule(calling_frame[0])
    calling_module_folder = os.path.dirname(calling_module.__file__)
    urlpath = urlparse(url)
    downloadedfilepath = calling_module_folder + "\\" + os.path.basename(urlpath.path)

    urllib.request.urlretrieve(url, downloadedfilepath)
