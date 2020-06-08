import pandas as pd
import requests
import csv


def has_any_lte(_chunk):
    if _chunk['radio'].values.any() == 'LTE':
        return True
    return False


def is_lte_row(_row):
    if _row[0] == 'LTE':
        return True
    return False


def get_lte_rows(_chunk):
    rows = []
    for _row in _chunk.values:
        if is_lte_row(_row):
            rows.append(_row)
    return rows


'''
url = "https://us1.unwiredlabs.com/v2/process.php"

payload = "{\"token\": \"0ec09ab2fa4d20\"," \
          "\"radio\": \"lte\"," \
          "\"mcc\": 310," \
          "\"mnc\": 410," \
          "\"cells\": [{" \
          "  \"lac\": 7033," \
          "  \"cid\": 17811" \
          "}]," \
          "\"address\": 1}"
'''

csv_file = "~/Downloads/cell_towers.csv"
# csv_file = "../csv_data/lte.csv"

with open('../csv_data/lte_cells.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['radio', 'mcc', 'net', 'area', 'cell', 'unit', 'lon', 'lat', 'range', 'samples', 'changeable',
                     'created', 'updated', 'averageSignal'])
    for chunk in pd.read_csv(csv_file, chunksize=1000, usecols=['radio', 'mcc', 'net', 'area', 'cell', 'unit',
                                                                'lon', 'lat', 'range', 'samples', 'changeable',
                                                                'created', 'updated', 'averageSignal']):
        if has_any_lte(chunk):
            _rows = get_lte_rows(chunk)
            writer.writerows(_rows)
'''
        if chunk['radio'].values.any() == 'LTE':
            for row in chunk.values:
                print(row[0])

            print(count)
            count += 1
            print(chunk['radio'])
        print(chunk.columns)
'''

# response = requests.request("POST", url, data=payload)

# print(response.text)
