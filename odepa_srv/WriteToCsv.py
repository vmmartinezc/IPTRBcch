#import csv
#from odepa_srv import settings

#def write_to_csv(item):
#    writer = csv.writer(open(settings.csv_file_path, 'a'), lineterminator='\n')
#    writer.writerow([item[key] for key in item.keys()])

#class WriteToCsv(object):
#    def process_item(self, item, spider):
#        write_to_csv(item)
#        return item


#import csv

#class CsvWriterPipeline(object):
#    @classmethod
#    def from_crawler(cls, crawler):
#        settings = crawler.settings
#        file_name = settings.get("FILE_NAME")
#        return cls(file_name)
#
#    def __init__(self, file_name):
#        header = ["URL"]
#        self.csvwriter = csv.writer(open(file_name, 'wb'))
#        self.csvwriter.writerow(header)
#
#    def process_item(self, item, internallinkspider):
#        # build your row to export, then export the row
#        row = [item['url']]
#        row.extend
#        self.csvwriter.writerow(row)
#        return item
#

import csv
import codecs
import items
from odepa_srv import settings

# producto,volumen,url,precioProm,calidad,variedad,precioMin,mercado,precioMax,unidad

class WriteToCsv(object):
    def __init__(self):
        self.file_name = csv.writer(open('output.csv', 'wb'))
        self.file_name.writerow(['url', 'producto','variedad','mercado', 'volumen','calidad','precioMin', 'precioProm','precioMax','unidad'])

    def process_item(self, item, spider):
        self.file_name.writerow([item['url'],
                                    item['producto'].encode('utf8'),
                                    item['variedad'].encode('utf8'),
                                    item['mercado'].encode('utf8'),
                                    item['volumen'].encode('utf8'),
                                    item['calidad'].encode('utf8'),
                                    item['precioMin'].encode('utf8'),
                                    item['precioProm'].encode('utf8'),
                                    item['precioMax'].encode('utf8'),
                                    item['unidad'].encode('utf8'),
                                    ])
        return item 
