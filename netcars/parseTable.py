import json
import asyncio
import os
import requests
import pandas
import sqlite3
from formatExcel import makeExel

def FizKZ(jsonfile,path):
	cars_all =[]
	con = sqlite3.connect("db.sqlite3")
	with con:
		cur = con.cursor()
		with open(jsonfile,'r') as file:
			cars = json.load(file)
			for car in cars:
				print(car)
				with con:
					cur = con.cursor()
					liters=[]
					rows = cur.execute('SELECT OTC, CC FROM maincar WHERE ManufKor = ? AND ModeKor = ? AND year = ? OR badge = ?', (car['Manuf'],car['Model'],car['Year'],car['Model']))
					for row in rows:
						liters.append(row)
					if type(car['engine']) == int and liters != []:
						#get closest calc value
						try:
							nearest = min(liters[0], key=lambda v: abs(car['engine']-int(v.replace(' ',''))))
						except AttributeError:
							nearest = min(liters[0], key=lambda v: abs(car['engine']-int(v)))
						ocp = next((item for item in liters if item[1] == nearest), None)
					else :
						ocp = None
					manuf_mod_eng = cur.execute('SELECT Manuf, Model FROM maincar WHERE ManufKor = ? AND ModeKor = ?', (car['Manuf'],car['Model']))
					eng = next((item for item in manuf_mod_eng), None)
					calc_car = {
							'A' : 1#NDA
							'B' : 1#NDA,
							'C' : 1#NDA
							'D' : 1#NDA
							}
					all_price = 0
					for calc in calc_car.items():
						if type(calc[1]) == int:
							all_price += calc[1]
					car_xml_data ={
					"Фото" : car['img'],
					"Марка" : '=HYPERLINK("'+car['idcar']+'","'+eng[0]+'")',
					"Модель" : eng[1],
					"Выкуп" : calc_car['A'],
					"Доставка" : calc_car['B'],
					"Налоги" : calc_car["C"],
					"Регистрация" : calc_car["D"],
					'Итог' : all_price,
					"Год" : int(car ['Year']),
					"Объём двигателя" : str(car['engine'])+'cc'
					}
					cars_all.append(car_xml_data)
	makeExel(cars_all,path);