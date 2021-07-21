import csv
import datetime
import sys

CLEAN_PATH = '../KISTLER/clean_data/'
CLEAN_CSV = 'press_20210118T193142_20210118T194154.csv'
WRITE_PATH = '../KISTLER/data_set/'
DATE_FORMAT = '%Y%m%dT%H%M%S'

def round_seconds(obj: datetime.datetime) -> datetime.datetime:
    if obj.microsecond >= 500_000:
        obj += datetime.timedelta(seconds=1)
    return obj.replace(microsecond=0)

EPOCH = datetime.datetime.utcfromtimestamp(0)

def unix_time_millis(dt):
    return (dt - EPOCH).total_seconds() * 1000.0

with open(CLEAN_PATH + CLEAN_CSV) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')

    temp_ts = []
    
    header = next(csv_reader, None)

    for row in csv_reader:
        header_index = 13
        date = datetime.datetime.strptime(row[1], DATE_FORMAT)
        date = unix_time_millis(date)
        for value in row[13:1393]:
            temp_ts.append([str(date + float(header[header_index]) * 1000), value])
            header_index = header_index + 1
            print(len(temp_ts))
        
    print('\n')
    print('scrivo file ...')
    CSV = open(WRITE_PATH + 'ready_' + CLEAN_CSV, "a")
    CSV.write('timestamp;pressure')
    CSV.write('\n')
    for row in temp_ts:
        CSV.write(';'.join(row))
        CSV.write('\n')
    CSV.close()
