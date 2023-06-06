#!./env/bin/python
import dbm
import csv
import sys

def clean_csv(argv):
    taxroll_file = argv[1]
    centroid_file = argv[2]
    db = dbm.open(centroid_file, 'r')

    daytonprops = open('daytonprops.csv', 'w')
    to_remove = ['TXYR','HLF1CHG','HLF2CHG','HLF1RED','HLF2RED','HLF1ADJ',
         'HLF2ADJ','HLF1RLBK','HLF2RLBK','HLF1HMSD','HLF2HMSD','HLF1HMRB',
         'HLF2HMRB','HLF1PEN','HLF2PEN','HLF1SPASMTS','HLF2SPASMTS','HLF1AMTDUE',
         'HLF2AMTDUE','HLF1DAYCRDT','HLF2DAYCRDT']

    error_count = 0
    with open(taxroll_file) as csvfile:
        reader = csv.DictReader(csvfile)
        extended_names = reader.fieldnames + ['lat', 'lon']
        for item in to_remove:
            extended_names.remove(item)
        extended_writer = csv.DictWriter(daytonprops, fieldnames=extended_names)
        extended_writer.writeheader()
        for row in reader:
            try:
                nospace_parcel = row['PARCELID'].replace(" ", "")
                latlon = db[nospace_parcel].split()
                # print(row['PARCELID'], latlon[0], latlon[1])
                extended_row = row
                extended_row['lat'] = latlon[0].decode("utf-8") 
                extended_row['lon'] = latlon[1].decode("utf-8")
                for item in to_remove:
                    del extended_row[item]
                for item in extended_names:
                    extended_row[item] = extended_row[item].strip()
                extended_writer.writerow(extended_row) 

            except Exception as e:
                print("ERROR", row['PARCELID'], e)
                error_count += 1

    print('error count',error_count)
    daytonprops.close()

if __name__ == "__main__":
    if len(sys.argv) == 3:
        clean_csv(sys.argv)
    else:
        print("Usage: clean_csv.py <taxroll filename> <centroid filename>")