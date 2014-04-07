import argparse
import random
import requests
import pickle
import credentials

SORT_OPTIONS = ['relevance', 'dateasc', 'datedesc']

ZONES = {
	'book': {'reclevel': 'brief', 'total': 1000000},
	'article': {'reclevel': 'brief', 'total': 1000000},
	'music': {'reclevel': 'brief', 'total': 1000000},
	'map': {'reclevel': 'brief', 'total': 150000},
	'picture': {'reclevel': 'brief', 'total': 1000000},
	'list': {'reclevel': 'full', 'total': 32000},
	'collection': {'reclevel': 'brief', 'total': 370000},
	'people': {'reclevel': 'brief', 'total': 1000000},
	'newspaper': {'reclevel': 'full', 'total': 10000000}
}


def update_zone(zone):
	results = get_items(zone, ZONES[zone]['total'], ZONES[zone]['reclevel'])
	if results:
		print 'OK'
		with open('cache/{}.pickle'.format(zone), 'wb') as zone_file:
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
		with open('cache/totals.pickle'.format(zone), 'wb') as zone_file:
			pickle.dump(results, zone_file)


def get_items(zone, total, reclevel='brief'):
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