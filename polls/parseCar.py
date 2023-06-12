import json
import asyncio
import aiohttp


def generateUrl(data):
	host_data = 'http://api.encar.com/search/car/list/general?count=true&q=(And.Hidden.N._.'
	#car model options
	#--------
	carType = '(C.CarType.'+data['carType']+'._.'
	car_manuf_model = '(C.Manufacturer.'+data['manuf']+'._.ModelGroup.'+data['model']+'.'
	#extra options
	#--------
	color = ''.join(filter(None,['_.(Or.Color.',data.get('color'),'.)']))
	fuel = ''.join(filter(None,['_.FuelType.',data.get('fuel'),'.']))
	transmission = ''.join(filter(None,['_.Transmission.',data.get('transmission'),'.']))
	option = ''
	if data.get('options') != None:
		for option in data.get('options'):
			option_add += ''.join(filter(None,['_.Options.',option,'.']))
	findata = ')&sr=%7CModifiedDate|'
	#mainurl
	search = host_data+carType+car_manuf_model+color+fuel+transmission+option+findata

	#params_from_lower
	#--------
	params_from_lower = ['year_from','price_from']
	check = {}
	for param in params_from_lower:
		val = data.get(param)
		if data.get(param) == None or data.get(param) == '':
			val = 0
		check[param] = int(val)

	#params_from_higher
	#--------
	params_from_higher = ['year_to','price_to']
	for param in params_from_higher:
		val = data.get(param)
		if data.get(param) == None  or data.get(param) == '':
			val = 999999999
		check[param] = int(val)

	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop)
	coroutine = parseList(search)
	parseinfo = loop.run_until_complete(coroutine)
	loop.close()

	getInfo = []
	for car in parseinfo:
		if car != None and checkValBadge(car['badge'],data['badge']) :
			if int(car['year']) >= check['year_from'] and int(car['year']) <= check['year_to'] and int(car['price'])*10000 >= check['price_from'] and int(car['price'])*10000 <= check['price_to'] :
				c = {	
					'img' : car['img'],
					'Manuf' : data['manuf'],
					'Model' : data['model'],
					'Year' : car['year'],
					'engine' : car['engine'],
					'price' : car['price'],
					'idcar' : car['idcar']
 				}
				getInfo.append(c)
	return getInfo


def checkValBadge(val, check):
	if check == None or check == '-':
		return True
	answer = False
	if check.lower().replace(' ', '') in val.lower().replace(' ', ''):
		answer = True
	return answer


async def parseList(url):
	pages = ['0', '400','800']
	response = []
	aiohttp_client = aiohttp.ClientSession()
	async with aiohttp_client as client:
		full_list = await asyncio.gather(*[getList(url+page+'|400',client) for page in pages])
		for data in full_list:
			response.append(data)
	await aiohttp_client.close()
	return response[0]

async def getList(url,client):
	start = await client.get(url)
	data = await start.text()
	cars_json = json.loads(data)
	response = []
	cars_listed = cars_json['SearchResults']
	response = await asyncio.gather(*[parseResults(car) for car in cars_listed])
	return response


async def parseResults(car):
	idcar = car['Id']
	engine = await parseEngine(idcar)
	if engine != None and car.get('Photo') != None:
		img = 'https://ci.encar.com/carpicture'+car['Photo']+'001.jpg'
		year = car['FormYear']
		price = car['Price']
		badge = car['Badge']
		response ={
			'img' : img,
			'engine': engine,
			'year': year,
			'price' : price,
			'idcar' : 'http://www.encar.com/dc/dc_cardetailview.do?pageid=dc_carsearch&listAdvType=pic&carid='+idcar,
			'badge' : badge
			 }
		return response


async def parseEngine (idcar):
	carData = None
	carUrl = 'http://www.encar.com/dc/dc_cardetailview.do?method=ajaxInspectView&rgsid='+idcar+'&sdFlag=N'
	aiohttp_client = aiohttp.ClientSession()
	async with aiohttp_client as client:
			start = await client.get(carUrl)
			data = await start.text()
			if json.loads(data)[0].get('inspect') != None:
				carData =json.loads(data)[0]['inspect']['carSaleDto']['displacement']
	return(carData)



if __name__ == '__main__':
	url = 'http://api.encar.com/search/car/list/general?count=true&q=(And.Hidden.N._.(C.CarType.N._.(C.Manufacturer.아우디._.ModelGroup.a3.))_.(Or.Color..)_.FuelType.._.Transmission..)&sr=%7CModifiedDate%7C0%7C80'
	start = requests.get(url)
	print(start.json()['SearchResults'][0])