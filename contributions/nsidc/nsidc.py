'The nsidc contribution'

from contributions import shared

def download():
    'this is the doc string'
    print("this is get() in nsidc")
    #ftp://sidads.colorado.edu/DATASETS/NOAA/G02135/north/daily/data/N_seaice_extent_daily_v2.1.csv
    shared.download_data("ftp://sidads.colorado.edu/DATASETS/NOAA/G02135/north/daily/data/N_seaice_extent_daily_v3.0.csv")
    print("nsidc finished")


    #ftp.sendcmd("MDTM N_seaice_extent_daily_v2.1.csv")

def get_data():
    'Returns nsidc data'
