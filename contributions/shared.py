'shared module'
import os
import urllib.request
from urllib.parse import urlparse
import inspect
import hashlib
import ftplib
import socket

_refresh_files = True

def set_refresh_files(value):
    "Stop files from being downloaded"
    _refresh_files = value

def download_data(url):
    "Downloads file if modified since last download"

    modified, error = _modified_since_last_download(url)

    if modified and _refresh_files:
        return _download_data_file(url)

    short_url = _shorten_url(url)

    if error:
        print("Error - could not download " + short_url)
    else:
        print(short_url + " not modified since last download")

    return _generate_download_path(url)

def _shorten_url(url):
    if len(url) > 70:
        return url[:30] + "..." + url[-30:]

    return url

def _generate_download_path(url):
    calling_module_folder = _get_calling_module_folder()
    downloaded_filepath = _make_download_path(url, calling_module_folder)
    return downloaded_filepath

def _download_data_file(url):
    calling_module_folder = _get_calling_module_folder()
    downloaded_filepath = _make_download_path(url, calling_module_folder)

    parsed_url = urlparse(url)
    scheme = parsed_url.scheme

    if scheme == "http" or scheme == "https":
        last_modified = _retrieve_via_http(url, downloaded_filepath)

    if scheme == "ftp" or scheme == "sftp":
        last_modified = _retrieve_via_ftp(parsed_url, downloaded_filepath)

    _update_previous_last_modified(_get_hash_filepath(url), last_modified)

    return downloaded_filepath

def _retrieve_via_http(url, downloaded_filepath):
    headers = urllib.request.urlretrieve(url, downloaded_filepath)[1]
    last_modified = headers["Last-Modified"]
    return last_modified

def _make_download_path(url, calling_module_folder):
    return os.path.join(calling_module_folder, os.path.basename(urlparse(url).path))

def _get_calling_module_folder():
    calling_frame = inspect.stack()[3]
    calling_module = inspect.getmodule(calling_frame[0])
    calling_module_folder = os.path.dirname(calling_module.__file__)
    return calling_module_folder

def _modified_since_last_download(url):

    try:
        last_modified = _get_last_modified(url)
    except urllib.error.URLError as exception:
        print(exception.reason)
        return (False, True)
    except ftplib.error_perm as exception:
        print(exception)
        print("file likely doesn't exist - check filename")
        return (False, True)
    except socket.gaierror as exception:
        print(exception)
        print("Ftp hostname likely doesn't exist - check hostname")
        return (False, True)


    previous_last_modified = _get_previous_last_modified(url)

    return (last_modified != previous_last_modified, False)

def _get_previous_last_modified(url):
    hash_filepath = _get_hash_filepath(url)

    if os.path.exists(hash_filepath):
        last_modified_date_file = open(hash_filepath, "r")
        return last_modified_date_file.read()

    return ""

def _get_hash_filepath(url):
    hash_filename = hashlib.sha224(url.encode('utf-8')).hexdigest() + ".txt"
    hash_filepath = os.path.join("LastModifiedCache", hash_filename)
    return hash_filepath


def _get_last_modified(url):
    parsed_url = urlparse(url)
    scheme = parsed_url.scheme

    if scheme == "http" or scheme == "https":
        last_modified = _get_last_modified_via_http(url)
        return last_modified

    if scheme == "ftp" or scheme == "sftp":
        last_modified = _get_last_modified_via_ftp(url)
        return last_modified

    return ""

def _get_last_modified_via_http(url):
    req = urllib.request.Request(url, method="HEAD")
    resp = urllib.request.urlopen(req)

    last_modified = resp.getheader("last-modified")
    return last_modified

def _get_last_modified_via_ftp(url):
    parsed_ftp_url = urlparse(url)
    ftp_host = parsed_ftp_url.hostname
    ftp_path = parsed_ftp_url.path
    ftp = ftplib.FTP(ftp_host)
    ftp.login()
    last_modified = str(ftp.sendcmd("MDTM " + ftp_path))
    ftp.quit()
    return last_modified

def _update_previous_last_modified(hash_filepath, last_modified):
    last_modified_date_file = open(hash_filepath, "w")
    last_modified_date_file.write(last_modified)

def _retrieve_via_ftp(parsed_url, downloaded_filepath):
    ftp_host = parsed_url.hostname
    ftp_path = parsed_url.path

    try:
        ftp = ftplib.FTP(ftp_host)
        ftp.login()
        ftp.retrbinary("RETR " + ftp_path, open(downloaded_filepath, "wb").write)
        last_modified = str(ftp.sendcmd("MDTM " + ftp_path))
    finally:
        ftp.quit()

    return last_modified
