'The global temperature contribution'
from contributions import shared

def get():
    'this is the doc string'
    print("this is get() in global temperature")

    path = shared.download_data("https://data.giss.nasa.gov/gistemp/tabledata_v3/GLB.Ts+dSST.csv")

    data_file = open(path)

    for line in data_file:
        values = line.split(',')
        print(values[0])
    data_file.close()

    print("global temperature finished")
