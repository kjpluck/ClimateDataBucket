'The global temperature contribution'
from contributions import shared

_path = "hello"

def download():
    'this is the doc string'
    print("downloading global temperature data")
    global _path
    _path = shared.download_data("https://data.giss.nasa.gov/gistemp/tabledata_v3/GLB.Ts+dSST.csv")


    print("global temperature download finished")

def get_data():
    'Returns global_temperatue data'
    global _path
    data_file = open(_path)
    data = []
    for line in data_file:
        values = line.split(',')
        if not values[0].isdecimal():
            continue

        for month in range(1, 12):
            if values[month] == "***":
                continue
            data.append({'year':values[0], 'month':month, 'value':values[month]})

    data_file.close()
    return data
