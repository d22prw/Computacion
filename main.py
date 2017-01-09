#!/usr/bin/env python
#!/usr/bin/python
#-*- coding: utf-8-*-
from pymongo import MongoClient
import urllib2, json
client = MongoClient()
db = client.BBDD

from flask import Flask,session,render_template,url_for,request,redirect,Response,json

app = Flask(__name__,template_folder='Template')

@app.route('/index')
@app.route('/')
def main():
	return render_template('login.html')
@app.route('/valores_cotizacion')
def valores_cotizacion():
	valores_basedatos = db.BBDD.find({}).sort([('Fecha',1),('Hora',-1)]).limit(20)
	print(valores_basedatos)
	lista = {}
	i=0
	for valor_db in valores_basedatos:
		lista[i]=valor_db
		i=i+1
	print(lista)
	return render_template('valores_cotizacion.html',lista=lista)

@app.route('/obtiene_sup_umbral', methods=['POST'])
def obtiene_sup_umbral():
	if request.method == 'POST':
		umbral_usuario = request.form['Umbral']
		if(umbral_usuario == ''):
			return render_template('main.html')
		else:
			basedatos_umbral = db.BBDD.find({});
			umbral_pag = (float(umbral_usuario)+1)*float(basedatos_umbral[1]['Cotizacion'].replace(',','.'))
			print(umbral_pag)
			dic_sup = {}
			for datos_umbral in basedatos_umbral:
				#if(umbral_pag<float(basedatos_umbral['Cotizacion'].replace(',','.'))):
				if(umbral_pag<float(datos_umbral['Cotizacion'].replace(',','.'))):
					print(datos_umbral)
					dic_sup[datos_umbral['Cotizacion']]=datos_umbral
			return render_template('umbrales_superiores.html',dic_sup=dic_sup)

@app.route('/media_cotizaciones', methods =['POST','GET'])
def media_cotizaciones():
	db_usar = request.form['BBDD']
	if(db_usar == 'MongoDB'):
		datos_db = db.BBDD.find({})
		cotizacion_suma = 0
		n_datos = 0
		for datos in datos_db:
			cotizacion_suma = cotizacion_suma + float(datos['Cotizacion'].replace('%','').replace(',','.'))
			n_datos = n_datos+1
		media = float(cotizacion_suma/n_datos)
	if(db_usar == 'Thingspeak'):
		valores = urllib2.urlopen('https://thingspeak.com/channels/179436/field/1.json')
		print(valores)
		#datos_db = ast.literal_eval(str(valores.read()))
		datos_leidos = valores.read()
		print(datos_leidos)
		datos_db = json.loads(datos_leidos)
		cotizacion_suma = 0
		n_datos = 0
		print(datos_db)
		for datos in datos_db['feeds']:
			print(datos)
			#if datos['field1'] != 'Cotizacion':
			cotizacion_suma = cotizacion_suma + float(datos['field1'].replace(',','.'))
			n_datos = n_datos +1;
		media = float(cotizacion_suma/n_datos)
	return render_template('cotizacion_media.html', media = media)
@app.route('/obtiene_graficas', methods=['POST'])
def obtiene_graficas():
	return render_template('graficas.html')

@app.route('/login',methods=['POST','GET'])
def login():
	usuario = request.form['usuario']
	contrasena = request.form['contrasena']
	usuariosycontrasenas=[]
	usuariosycontrasenas = db.users.find({})
	print(usuariosycontrasenas)
	userpass= 0
	for userpass in usuariosycontrasenas:
	#if((str(usuario)=='admin')and(str(contrasena)=='1234')):
	#if(existe != None):
		if((userpass['Usuario']==str(usuario))and(userpass['Contrasena']==str(contrasena))):
			return render_template('main.html')
		else:
			return render_template('login.html')

@app.route('/main')
def principal():
	return render_template('main.html')

if __name__=='__main__':
	import uuid
	app.secret_key=str(uuid.uuid4())
	app.debug=True
	app.run(host='0.0.0.0',port=80)
