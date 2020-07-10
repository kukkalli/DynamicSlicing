import pandas as pd
import time
import json

start_time = time.time()


def get_rows(_chunk, _data):

    for _row in _chunk.values:
        row = {
            "id": _row[4],
            "name": _row[4],
            "address": "",
            "heighAGLInMeters": 0,
            "antennaHeightAGLInMeters": 0,
            "type": "",
            "operator": "",
            "radioType": _row[0],
            "radioDetails": {
                "mcc": _row[1],
                "mnc": _row[2],
                "areaCode": _row[3],
                "range": _row[8]
            },
            "geoLocation": {
                "lat": _row[7],
                "lon": _row[6]
            },
            "deviceIds": [],
            "linkIds": []
        }
        _data.append(row)


csv_file = "../csv/essex_cells.csv"
data = []
for chunk in pd.read_csv(csv_file, chunksize=10, usecols=['radio', 'mcc', 'net', 'area', 'cell', 'unit',
                                                          'lon', 'lat', 'range', 'samples', 'changeable',
                                                          'created', 'updated', 'averageSignal']):
    get_rows(chunk, data)

with open('../csv/essex_cells.json', 'w', newline='') as file:
    json.dump(data, file)
print("--- %s seconds ---" % (time.time() - start_time))
