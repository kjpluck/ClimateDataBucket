'The global mean sea level contribution'

from contributions import shared

def download():
    'this is the doc string'
    print("this is get() in global mean sea level")

    shared.download_data("http://sealevel.colorado.edu/files/2016_rel4/sl_global.txt")
    print("global mean sea level finished")

def get_data():
    'returns sea level data'
