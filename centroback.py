from flask import Flask, render_template, request
from decimal import Decimal
import pymysql
import requests
import json
#to run on your machine, in command line enter
#set FLASK_APP=centroback.py
#python -m flask run
#assuming the dependecies are correct it will render the page
#on your localhost http://127.0.0.1:5000

#this is just a work around a certificate warning
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

#this will be what renders the actual app when it's ready
app = Flask(__name__)

connection = pymysql.connect(host="pi.cs.oswego.edu",
user="USERREMOVEDFORSECURITY", password="PASSWORDREMOVEDFORSECURITY", db="Centro",
cursorclass=pymysql.cursors.DictCursor)

cur = connection.cursor()


#collects input from the html's drop down list
def getInput():
	select = request.form.get("stopInput")
	return select

def getBusDes():
	getBusDes.dir = request.form.get("dir")
	if(getBusDes.dir == "to campus"):
		return "11 Green Route to Campus Cente"
	elif(getBusDes.dir == "from campus"): 
		return "11 Green Route to Rice Creek"
	return None;
	
def calcData(s):
	#our counters for every time the bus comes into stop radius
	calcData.L5 = 0
	calcData.L4 = 0
	calcData.L3 = 0
	calcData.L2 = 0
	calcData.L1 = 0
	calcData.zero = 0
	calcData.E1 = 0
	calcData.E2 = 0
	calcData.E3 = 0
	calcData.E4 = 0
	calcData.E5 = 0

	def getStopLat(s):
		cur.execute("SELECT lat FROM stops WHERE stopid = '" + s + "'")
		getStopLat.stopLat = cur.fetchall()
		
	def getStopLon(s):
		cur.execute("SELECT lon FROM stops WHERE stopid = '" + s + "'")
		getStopLon.stopLon = cur.fetchall()
	
	getStopLat(s)
	getStopLon(s)
	#gathering lat/lon values for the stop, and creating a radius
	#.0001 is approx. 10 meters(32 feet)
	#if my math is right .008 is about 1/4 a mile 
	latxpos = float(getStopLat.stopLat[0]["lat"]) + .0002
	latxneg = float(getStopLat.stopLat[0]["lat"]) - .0002
	lonypos = float(getStopLon.stopLon[0]["lon"]) + .0002
	lonyneg = float(getStopLon.stopLon[0]["lon"]) - .0002
		
	#collects all time stamps of when the bus is in the stop radius
	
	def getBusCount():
		if(getBusDes() == None):
			cur.execute("SELECT tmstmp FROM vehicles WHERE lat > " + str(latxneg) + " AND lat < " + str(latxpos) + " AND lon > " + str(lonyneg) + " AND lon < " + str(lonypos) + ";")
			getBusCount.busCount = cur.fetchall()
		else:
			cur.execute("SELECT tmstmp FROM vehicles WHERE lat > " + str(latxneg) + " AND lat < " + str(latxpos) + " AND lon > " + str(lonyneg) + " AND lon < " + str(lonypos) + " AND des = " + '"' +  getBusDes() + '";')
			getBusCount.busCount = cur.fetchall()
			print("Bus Direction: " + getBusDes.dir)
	
	#gets our buschedule by stopid 
	def getBusSchedule(s):
		cur.execute("SELECT * FROM busSchedule WHERE stopid = '" + s + "'");
		getBusSchedule.busSchedule = cur.fetchall()
	
	#call both
	getBusSchedule(s)
	getBusCount()
	#des = "11 Green Route"
	#des = "11 Green Route to Campus Cente"
	#des = "10 Blue Route to Campus Cente"
	#des = "10 Blue Route"
	
	#for loop that increments our counters
	for i in getBusSchedule.busSchedule:
		for j in getBusCount.busCount:
			#if timestamps hours match, we then match minutes
			if(j["tmstmp"].split(" ")[1][:-6] == i["scheduledTime"][:-3]):
				diff = int(j["tmstmp"].split(" ")[1][3:5]) - int(i["scheduledTime"][3:5])
				if(diff == 0):
					calcData.zero += 1
				elif(diff == -1 | -2):
					calcData.E1 += 1
				elif(diff == -3 | -4):
					calcData.E2 += 1
				elif(diff == -5 | -6):
					calcData.E3 += 1
				elif(diff == -7 | -8):
					calcData.E4 += 1
				elif(diff == -9 | -10):
					calcData.E5 += 1
				elif(diff == 1 | 2):
					calcData.L1 += 1
				elif(diff == 3 | 4):
					calcData.L2 += 1
				elif(diff == 5 | 6):
					calcData.L3 += 1
				elif(diff == 7 | 8):
					calcData.L4 += 1
				elif(diff == 9 | 10):
					calcData.L5 += 1
				
				
@app.route('/', methods=['GET', 'POST'])

def renderData():
	if(getInput() == None or getBusDes() == None):
		return render_template('index.html', data = "0", content_type='application/json')
	else: 
		calcData(str(getInput()))
		res = calcData
		return render_template('index.html', data = res, content_type='application/json')
	


	
