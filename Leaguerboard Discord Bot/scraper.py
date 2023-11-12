import time
import os
import requests
import os.path
import os
import json
import numpy
# data
headers = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
	"Accept-Language": "en-US,en;q=0.6",
	"Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
	"Origin": "https://developer.riotgames.com"
}

key = 

#funcs

#get id, returns puuid of user
def getid(name):
	request = requests.get(f'https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{name}?api_key={key}', headers = headers)
	data = json.loads(request.content)
	return str(data['puuid'])

#get matches, returns string list of match IDs
#puuid- str puuid of summoner
#count- number of matches
#idx- start idx of matches
def getmatches(puuid, count, idx):
	request = requests.get(f'https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start={idx}&count={count}&api_key={key}', headers = headers)
	data = json.loads(request.content)
	return data

#get match data, returns match data of one player given puuid
def matchData(puuid, matchid):
	#debug
	#print(matchid)
	
	request = requests.get(f'https://americas.api.riotgames.com/lol/match/v5/matches/{matchid}?api_key={key}', headers = headers)
	if request.status_code == 429:
		time.sleep(120)
		print('timeout')
		request = requests.get(f'https://americas.api.riotgames.com/lol/match/v5/matches/{matchid}?api_key={key}', headers = headers)

	data = json.loads(request.content)
	if 'info' not in data:
		print
		return 'err'
	if data['info']['gameDuration'] == 0:
		return 'err'
	for x in range(0, 9):
		if data['info']['participants'][x]['puuid'] == puuid:
			return data['info']['participants'][x]

def matchData2(puuid, matchid):
	#debug
	#print(matchid)
	
	request = requests.get(f'https://americas.api.riotgames.com/lol/match/v5/matches/{matchid}?api_key={key}', headers = headers)
	if request.status_code == 429:
		time.sleep(120)
		print('timeout')
		request = requests.get(f'https://americas.api.riotgames.com/lol/match/v5/matches/{matchid}?api_key={key}', headers = headers)

	data = json.loads(request.content)
	if 'info' not in data:
		print
		return 'err'
	if data['info']['gameDuration'] == 0:
		return 'err'
	for x in range(0, 9):
		if data['info']['participants'][x]['puuid'] == puuid:
			print(matchid)
			d = {0:data['info']['participants'][x], 1:matchid}
			return d

def writeData(puuid, data):


	with open(f'{puuid}.json', 'a') as f:
		if data is not None:
			kl = data[0]['kills'],
			ds = data[0]['deaths'],
			ss = data[0]['assists']
			r= {
			'matchid': data[1],
			'kills': kl,
			'deaths': ds,
			'assists': ss,
			}
			helper(puuid, r, f)

def helper(puuid,r,f):
	with open(f'{puuid}.json') as file:
		if r['matchid'] in file.read():
			return
	json.dump(r, f)
	f.write('\n')
	

def logData(name, count, idx):
	id=getid(name)
	matches = getmatches(id, count, idx) 
	for match in matches:
		r = matchData2(id, match)
		writeData(id,r)


#gets winloss, key value from matchdata
def getWLKV(key, matchdata):
	if matchdata is not None:
		wl = matchdata['win']
		kv = matchdata[key]
		return [wl, kv]
	return 'err'

#compile a dictionary with key values of key, containing data of arrays with win/loss
#https://developer.riotgames.com/apis#match-v5/GET_getMatch possible keys in 'ParticipantDto'
def compileWLKV(key, mlist, puuid):
	data = dict()
	for matchid in mlist:
		curr = matchData(puuid, matchid)
		if curr == 'err':
			continue

		temp = getWLKV(key, curr)
		
		if temp == 'err':
			continue

		game = [0,1]
		if temp[0]:
			game = [1,0]
		
		if temp[1] in data:
			data[temp[1]][0] += game[0]
			data[temp[1]][1] += game[1]
		else:
			data.update({temp[1]: game})

	return data

#function to combine two dictionaries 
def combineDict(d1, d2):
#    print(d1)
#    print(d2)
	combined = dict()

	for key in set(d1.keys()).union(d2.keys()):
		if key in d1 and key in d2:
			v1 = d1[key][0]
			v2 = d2[key][0]
			combined[key] = [v1 + v2, d1[key][1] + d2[key][1]]
		elif key in d1:
			combined[key] = d1[key]
		else:
			combined[key] = d2[key]
		
	return combined
