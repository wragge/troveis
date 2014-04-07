import argparse
import random
import requests
import pickle
import credentials

SORT_OPTIONS = ['relevance', 'dateasc', 'datedesc']

ZONES = {
	'book': {'reclevel': 'brief', 'total': 1000000, 'aus': True},
	'article': {'reclevel': 'brief', 'total': 1000000, 'aus': True},
	'music': {'reclevel': 'brief', 'total': 200000, 'aus': True},
	'map': {'reclevel': 'brief', 'total': 40000, 'aus': True},
	'picture': {'reclevel': 'brief', 'total': 1000000, 'aus': True},
	'list': {'reclevel': 'full', 'total': 32000, 'aus': False},
	'collection': {'reclevel': 'brief', 'total': 40000, 'aus': True},
	'people': {'reclevel': 'brief', 'total': 1000000, 'aus': True},
	'newspaper': {'reclevel': 'full', 'total': 10000000, 'aus': False}
}

path = '/home/dhistory/webapps/troveis/troveis/'
#path = ''

def update_zone(zone):
	results = get_items(zone, ZONES[zone]['total'], ZONES[zone]['reclevel'], ZONES[zone]['aus'])
	if results:
		print 'OK'
		with open(path + '{}.pickle'.format(zone), 'wb') as zone_file:
			pickle.dump(results, zone_file)


def update_totals():
	params = {
		'q': ' ',
		'zone': 'all',
		'encoding': 'json',
		'n': 0,
		'key': credentials.TROVE_API_KEY
	}
	results = get_results(params)
	if results:
		with open(path + 'totals.pickle'.format(zone), 'wb') as zone_file:
			pickle.dump(results, zone_file)


def get_items(zone, total, reclevel='brief', aus=True):
	start = random.randint(0, total)
	params = {
		'q': ' ',
		'zone': zone,
		'encoding': 'json',
		'l-availability': 'y',
		'reclevel': reclevel,
		'n': 100,
		's': start,
		'sortby': random.choice(SORT_OPTIONS),
		'key': credentials.TROVE_API_KEY
	}
	if aus:
		params['l-australian'] = 'y'
	results = get_results(params)
	return results


def get_results(params):
	try:
		r = requests.get('http://api.trove.nla.gov.au/result', params=params)
	except requests.exceptions.RequestException:
		results = None
	else:
		try:
			results = r.json()
		except ValueError:
			results = None
	return results


parser = argparse.ArgumentParser()
parser.add_argument('zone')
args = parser.parse_args()
zone = args.zone
if zone == 'total':
	update_totals()
elif zone:
	update_zone(zone)