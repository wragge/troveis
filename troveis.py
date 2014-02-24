from flask import Flask
from flask import render_template
import random
import requests
from flask.ext.cache import Cache
import calendar

import credentials

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'filesystem', 'CACHE_DIR': 'cache'})

ERROR_MESSAGE = 'Something wen\'t wrong. Try again later.'
MAX_TOTAL = 30000
SORT_OPTIONS = ['relevance', 'dateasc', 'datedesc']

ZONES = {
	'book': 'books, theses, proceedings',
	'article': 'articles, papers, chapters, reports',
	'music': 'recordings, videos, sounds, scores',
	'map': 'maps',
	'picture': 'photos, artworks, objects',
	'list': 'public lists',
	'collection': 'diaries, manuscripts, archives',
	'people': 'people, organisations',
	'newspaper': 'newspaper articles'
}

@app.route('/')
def trove_is():
	totals = get_totals()
	examples = get_examples()
	if totals is None or examples is None:
		message = ERROR_MESSAGE
		zones = None
	else:
		zones = process_results(totals, examples)
		message = None
	return render_template('troveis.html', zones=zones, message=message)


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

@cache.cached(timeout=60*60*24, key_prefix='get_totals')
def get_totals():
	params = {
		'q': ' ',
		'zone': 'all',
		'encoding': 'json',
		'n': 0,
		'key': credentials.TROVE_API_KEY
	}
	results = get_results(params)
	return results

@cache.cached(timeout=60*5, key_prefix='get_examples')
def get_examples():
	start = random.randint(0, MAX_TOTAL)
	params = {
		'q': ' ',
		'zone': 'all',
		'encoding': 'json',
		'l-availability': 'y',
		'reclevel': 'full',
		'n': 10,
		's': start,
		'sortby': random.choice(SORT_OPTIONS),
		'key': credentials.TROVE_API_KEY
	}
	results = get_results(params)
	return results

def check_for_image(record):
	image_url = None
	try:
		for link in record['identifier']:
			if link['linktype'] == 'thumbnail':
				image_url = link['value']
				break
	except KeyError:
		pass
	return image_url


def process_results(totals, examples):
	zones = {}
	record_num = random.randint(0,9)
	for zone in totals['response']['zone']:
		zones[zone['name']] = {'total': '{:,}'.format(int(zone['records']['total']))}
	for zone in examples['response']['zone']:
		z_name = zone['name']
		details = zones[z_name]
		try:
			if z_name == 'newspaper':
				record = zone['records']['article'][record_num]
				details['title'] = record['heading']
				details['image_url'] = record['pdf'][:-6]
				details['url'] = record['troveUrl']
				date = format_iso_date(record['date'])
				details['citation'] = '{}, {}'.format(date, record['title']['value'])
			elif z_name == 'list':
				record = zone['records']['list'][record_num]
				details['title'] = record['title']
				details['url'] = record['troveUrl']
				details['citation'] = '{}, {}'.format(record['creator'].replace('public:', ''), record['created'][:4])
			elif z_name == 'people':
				details['url'] = 'http://trove.nla.gov.au/people/result?q='
			else:
				record = zone['records']['work'][record_num]
				details['title'] = record['title']
				details['image_url'] = check_for_image(record)
				details['url'] = record['troveUrl']
				date = record['issued'] if 'issued' in record else None
				contributors = record['contributor'] if 'contributor' in record else None
				try:
					#fix this later
					details['citation'] = u'{}{}{}'.format(', '.join(contributors).encode('utf-8').strip() if contributors else '', '<br>' if contributors else '', date if date else '')
				except:
					pass
			details['name'] = z_name
			details['label'] = ZONES[z_name]
			zones[zone['name']] = details
		except (KeyError, IndexError):
			pass
	zones = zones.values()
	zones.append({'name': 'website', 'label': 'archived web pages', 'total': '80,000,000', 'url': 'http://trove.nla.gov.au/website/result?q='})
	random.shuffle(zones)
	return zones


def format_iso_date(iso_date):
    year, month, day = iso_date.split('-')
    return '{} {} {}'.format(int(day), calendar.month_abbr[int(month)], year)


if __name__ == '__main__':
    app.run(debug=True)