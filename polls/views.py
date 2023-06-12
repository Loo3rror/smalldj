from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, FileResponse
from django.template import loader
from django.apps import apps
from polls.models import Maincar, ParamsTrans, CarFuel, CarTransmission, Colors
from polls.parseCar import generateUrl, parseList
from netcars.parseTable import FizKZ, OPTRFKZ, OPTRFKIRG
import os
import json
import uuid


def index(request):
	manuf_un = []
	manuf = list(Maincar.objects.values_list('manuf', flat=True))
	for m in manuf:
		if m not in manuf_un:
			manuf_un.append(m)
	cars = Maincar.objects.all()
	context = {
    'cars': manuf_un,
    'models':cars
  }
	html = loader.get_template('car_index.html')
	return HttpResponse( html.render(context,request))

def get_manuf_json (request):
	manuf_un = []
	manuf = list(Maincar.objects.values_list('manuf', flat=True))
	for m in manuf:
		if m not in manuf_un:
			manuf_un.append(m)

	return JsonResponse({'car_data':manuf_un })

def get_model_json (request, *args, **kwargs):
	model_un = []
	activeManuf = kwargs.get('manuf')
	manuf = list(Maincar.objects.values())
	for m in manuf:
		if m['model'] not in model_un and m['manuf'] == activeManuf:
			model_un.append(m['model'])
	return JsonResponse({'model_data':model_un })


def checkVal(val, check):
	answer = False
	if val.lower() in check.lower().replace(' ', ''):
		answer = True
	return answer


def get_car_param (request, *args, **kwargs):
	params = request.POST
	kor = []
	korNames = (Maincar.objects.values())
	catch1 = next((item for item in korNames if item["manuf"] == params["manuf"]), None)
	catch2 = next((item for item in korNames if item["model"] == params["model"]), None)
	badge = next((item for item in korNames if checkVal(item["badge"],params["model"])), None)
	#print(params)
	data = {
	'year_from' : params['year_from'] if params['year_from'] != None else None,
	'year_to' : params['year_to'] if params['year_to'] != None else None,
	'mileage_from' : params['mileage_from'] if params['mileage_from'] != None else None,
	'mileage_to' : params['mileage_to'] if params['mileage_to'] != None else None,
	'price_from' : params['price_from'] if params['price_from'] != None else None,
	'price_to' : params['price_to'] if params['price_to'] != None else None,
	'carType' : catch1['cartype'] if catch1 != None else None,
	'manuf' : catch1['manufkor'] if catch1 != None else None,
	'model' : catch2['modekor'] if catch2 != None else None,
	'color' : params['color'] if params['color'] != 'null' else '',
	'fuel' : params['fuel'] if params['fuel'] != 'null' else '',
	'transmission' : params['transmission'] if params['transmission'] != 'null' else '',
	'badge' : badge['badge'] if badge != None else None
	}
	stuff = generateUrl(data)
	json_object = json.dumps(stuff, indent=4)
	json_local = str(uuid.uuid4())
	path = os.getcwd()+"/tmp/"+json_local+".json"
	path_clean = os.getcwd()+"/tmp/"+params["manuf"]+params["model"]
	with open(path, "w") as outfile:
		outfile.write(json_object)
	if params['client'] == "FzKz":
		FizKZ(path,path_clean)
	if params['client'] == "OPTRFKZ":
		OPTRFKZ(path,path_clean) 
	if params['client'] == "OPTRFKIRG":
		OPTRFKIRG(path,path_clean) 
	with open(path_clean+'.xlsx', 'rb') as f:
			file_data = f.read()
		# sending response 
	response = HttpResponse(file_data, content_type='plain/text')
	response['Content-Disposition'] = 'attachment; filename="foo.txt"'
	return response
	return JsonResponse({'file_data':path_clean+'.xlsx'})

def get_OCT(request, *args, **kwargs):
	params = request.POST
	car = params
	data_price = 'getted'
	return JsonResponse({'data' : car})


def getOptions(request):
	options = []
	param = list(ParamsTrans.objects.values())
	i = 1
	for p in param:
		if p['rugroup'] == 'экстерьер/интерьер' or p['rugroup'] == 'безопасность':
			options.append({'id':i, 'label':p['runame'], 'value':p['korname'], 'group':p['rugroup']})
			i+=1

	return JsonResponse({'param_data':options })

def getParams(request):
	col_opt = []
	fuel_opt = []
	transm_opt = []
	fuel = list(CarFuel.objects.values())
	for f in fuel:
		fuel_opt.append({'label':f['rufuel'],'value':f['korfuel']})
	transm = list(CarTransmission.objects.values())
	for t in transm:
		transm_opt.append({'label':t['rutrans'],'value':t['kortrans']})
	colors = list(Colors.objects.values())
	for c in colors:
		col_opt.append({'label':c['rucolor'],'value':c['korcolor']})

	return JsonResponse({'color_data':col_opt,'fuel_data':fuel_opt, 'transm_data':transm_opt })