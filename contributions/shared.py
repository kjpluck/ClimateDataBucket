'shared module'
import os
import urllib.request
from urllib.parse import urlparse
import inspect
import hashlib

def hello():
    'hello function'
    print("Hello from shared")


def download_data(url):
    "Downloads file if modified since last download"
    if modified_since_last_download(url):
        download_data_file(url)
    else:
        print("Latest file already downloaded.")

def download_data_file(url):
    calling_module_folder = get_calling_module_folder()
    downloadedfilepath = make_download_path(url, calling_module_folder)
    headers = urllib.request.urlretrieve(url, downloadedfilepath)[1]
    update_previous_last_modified(url, headers)

def make_download_path(url, calling_module_folder):
    return os.path.join(calling_module_folder, os.path.basename(urlparse(url).path))

def get_calling_module_folder():
    calling_frame = inspect.stack()[3]
    calling_module = inspect.getmodule(calling_frame[0])
    calling_module_folder = os.path.dirname(calling_module.__file__)
    return calling_module_folder

def modified_since_last_download(url):
    last_modified = get_last_modified(url)
    previous_last_modified = get_previous_last_modified(url)

    return last_modified != previous_last_modified

def get_previous_last_modified(url):
    hash_filepath = get_hash_filepath(url)

    if os.path.exists(hash_filepath):
        last_modified_date_file = open(hash_filepath, "r")
        return last_modified_date_file.read()

    return ""

def get_hash_filepath(url):
    hash_filename = hashlib.sha224(url.encode('utf-8')).hexdigest() + ".txt"
    hash_filepath = os.path.join("LastModifiedCache", hash_filename)
    return hash_filepath


def get_last_modified(url):
    req = urllib.request.Request(url, method="HEAD")
    resp = urllib.request.urlopen(req)
    last_modified = resp.getheader("last-modified")
    return last_modified

def update_previous_last_modified(url, headers):
    hash_filepath = get_hash_filepath(url)
    last_modified = headers["Last-Modified"]
    last_modified_date_file = open(hash_filepath, "w")
    last_modified_date_file.write(last_modified)

