
 #!/usr/local/bin/python

import urllib, urllib2,re,time

from pymongo import MongoClient
client = MongoClient()
db = client.BBDD

buscar_umbral = '<div class="difP top center">(.*)</div>'
buscar_cotizacion = '<div class="price top center">(.*)</div>'
buscar_fecha = '<td class="date center">(.*)</td>'
buscar_hora = '<div class="time left">(.*)</div>'

prueba = 0

while True:
	respuesta = urllib2.urlopen('http://www.infobolsa.es/cotizacion/BBVA')
	html_code = respuesta.read().decode('utf-8')

	cot = re.search(buscar_cotizacion,html_code)

	fecha = re.search(buscar_fecha,html_code)
	hora = re.search(buscar_hora,html_code)
	umbral = re.search(buscar_umbral,html_code)

	cotizacion = cot.group(1)
	fecha = fecha.group(1)
	hora = hora.group(1)
	umbral = umbral.group(1)
	cotizacion.replace(',','.')
	umbral.replace(',','.')

	lista_valores = {}
	lista_valores['Cotizacion']=cotizacion
	lista_valores['Fecha']=fecha
	lista_valores['Hora']= hora
	lista_valores['Umbral']= umbral

	print(lista_valores)
	db.BBDD.insert_one(lista_valores)

	datos_acceso = urllib.urlencode({'key':'V4HTZEVYDN4AQK1A','field1':cotizacion.replace(',','.'),'field2':umbral.replace(',','.')})
	a3=urllib2.urlopen('https://api.thingspeak.com/update.json',data=datos_acceso)

	time.sleep(120)
