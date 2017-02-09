# -*- coding: utf-8 -*-

# Importamos desde el sistema scrapy todos los módulos
# necesarios para la operación del scraper
import scrapy
from scrapy.http import FormRequest, Request
from odepa_srv.items import OdepaSrvItem, ReviewLoader

# Estos módulos debieran apoyar las fórmulas para la definición
# de las fechas a importar
from datetime import datetime, date, timedelta

# Generamos la dirección web sobre la que haremos el scraper
init = "http://apps.odepa.cl/BoletinDiarioResult?merc=2%2C1%2C11%2C4%2C22%2C23%2C21%2C9%2C20%2C13%2C24%2C25%2C&produc=1%2C31%2C32%2C46%2C58%2C162%2C85%2C90%2C95%2C99%2C117%2C127%2C137%2C140%2C142%2C399%2C943%2C153%2C164%2C173%2C178%2C183%2C185%2C187%2C189%2C193%2C197%2C203%2C204%2C209%2C219%2C221%2C232%2C231%2C240%2C50%2C245%2C945%2C303%2C304%2C2%2C3%2C10%2C9%2C11%2C12%2C29%2C35%2C51%2C55%2C262%2C59%2C942%2C68%2C79%2C501%2C91%2C81%2C93%2C102%2C132%2C131%2C150%2C166%2C944%2C192%2C214%2C220%2C229%2C230%2C233%2C239%2C246%2C247%2C251%2C255%2C263%2C201%2C271%2C287%2C311%2C312%2C314%2C&variedad=true&calidad=true&mercado=true&origen=true"
ddh = "&dia_desde="
mdh = "&mes_desde="
adh = "&ano_desde="
dhh = "&dia_hasta="
mhh = "&mes_hasta="
ahh = "&ano_hasta="
ssh = "&sub_sector="
fh = "&fecha=="

# Primera versión es generar la url para descargar los datos de los últimos 7 dias
ndays = 1
dt = datetime.now().date()

# Definimos la configuración general del scraper en la clase. Ojo con el nombre,
# que debe ser igual al nombre del archivo
class OdepaBdfvSpider(scrapy.Spider):
    name = "od_bdfv_d"
    allowed_domains = ["odepa.cl"]
    start_urls = ["%s%s%02d%s%02d%s%02d%s%02d%s%02d%s%02d%s%02d%s%s" %(init,ddh,(dt + timedelta(-(ndays-1) + n)).day,mdh,(dt + timedelta(-(ndays-1) + n)).month,adh,(dt + timedelta(-(ndays-1) + n)).year,dhh,(dt + timedelta(-(ndays-1) + n)).day,mhh,(dt + timedelta(-(ndays-1) + n)).month,ahh,(dt + timedelta(-(ndays-1) + n)).year,ssh,ssv,fh,(dt + timedelta(-(ndays-1) + n)).strftime("%d/%m/%Y")) for n in range(0, ndays) for ssv in range(4,6)]

# Detallamos lo que extraeremos y guardaremos de la página web
    def parse(self, response):
        for sel in response.xpath('//table/tr'):
            item = OdepaSrvItem()
            rl = ReviewLoader(response=response, selector=sel)
            rl.add_xpath('mercado', 'td[1]/text()')
            rl.add_xpath('producto', 'td[2]/text()')
            rl.add_xpath('variedad', 'td[3]/text()')
            rl.add_xpath('calidad', 'td[4]/text()')
            rl.add_xpath('volumen', 'td[5]/text()')
            rl.add_xpath('precioMin', 'td[6]/text()')
            rl.add_xpath('precioMax', 'td[7]/text()')
            rl.add_xpath('precioProm', 'td[8]/text()')
            rl.add_xpath('unidad', 'td[9]/text()')
            rl.add_value('url', response.url.split('==')[1])
            yield rl.load_item()
