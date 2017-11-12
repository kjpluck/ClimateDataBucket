'The co2 contribution'
from contributions import shared

def download():
    'this is the doc string'
    print("this is download() in co2")

    shared.download_data("http://scrippsco2.ucsd.edu/assets/data/atmospheric/stations/in_situ_co2/weekly/weekly_in_situ_co2_mlo.csv")

    print("co2 finished")
