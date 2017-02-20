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
from odepa_srv import items
from odepa_srv import settings

# producto,volumen,url,precioProm,calidad,variedad,precioMin,mercado,precioMax,unidad

class WriteToCsv(object):
    def __init__(self):
        #se modifico el valor 'wb' a 'w' por error de escritura en python 3.x
        self.file_name = csv.writer(open('output.csv', 'w'))
        self.file_name.writerow(['url', 'producto','variedad','mercado', 'volumen','calidad','precioMin', 'precioProm','precioMax','unidad'])
        # se crea archivo de url con errores
        self.rr = csv.writer(open('errors.csv', 'w'))
        self.rr.writerow(['Fuente'])


    def process_item(self, item, spider):
        #Los errores solo tendran una linea con informacion
        self.file_name.writerow([item['url'],
                                        item['producto'],
                                        item['variedad'],
                                        item['mercado'],
                                        item['volumen'],
                                        item['calidad'],
                                        item['precioMin'],
                                        item['precioProm'],
                                        item['precioMax'],
                                        item['precio'],
                                        item['cantidad'],
                                        item['unidad'],
                                        item['fuente'],
                                        ])
        return item
        '''else:
            self.rr.writerow(item['fuente'])
            return 'error'''
            


