import csv
import datetime

RAW_CSV = '../KISTLER/raw_data/24_10_2019__13_11_2019/1.csv'
WRITE_PATH = '../KISTLER/clean_data/'
DELAY = 900 #in secondi
DATE_FORMAT = '%Y%m%dT%H%M%S'

def round_seconds(obj: datetime.datetime) -> datetime.datetime:
    if obj.microsecond >= 500_000:
        obj += datetime.timedelta(seconds=1)
    return obj.replace(microsecond=0)

with open(RAW_CSV) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')

    temperature = []
    pressure = []
    
    header = next(csv_reader, None)
    temperature.append([next(csv_reader, None)])
    pressure.append([next(csv_reader, None)])

    for row in csv_reader:
        dateRow = datetime.datetime.strptime(row[1], DATE_FORMAT)
        if(row[4] == 'Temperature'):
            dateLastTempRow = datetime.datetime.strptime(temperature[-1][-1][1], DATE_FORMAT)
            if((dateRow - dateLastTempRow).total_seconds() >= DELAY):
                temperature.append([row])
            else:
                temperature[-1].append(row)
        if(row[4] == 'Pressure'):
            dateLastTempRow = datetime.datetime.strptime(pressure[-1][-1][1], DATE_FORMAT)
            if((dateRow - dateLastTempRow).total_seconds() >= DELAY):
                pressure.append([row])
            else:
                pressure[-1].append(row)
        
    for file in temperature:
        CSV = open(WRITE_PATH + "/temp_" + file[0][1] + "_" + file[-1][1] + ".csv", "a")
        CSV.write(';'.join(header))
        CSV.write('\n')
        for row in file:
            CSV.write(';'.join(row))
            CSV.write('\n')
        CSV.close()
    for file in pressure:
        CSV = open(WRITE_PATH + "/press_" + file[0][1] + "_" + file[-1][1] + ".csv", "a")
        CSV.write(';'.join(header))
        CSV.write('\n')
        for row in file:
            CSV.write(';'.join(row))
            CSV.write('\n')
        CSV.close()