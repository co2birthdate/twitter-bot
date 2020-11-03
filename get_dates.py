from dateparser.search import search_dates
import requests
import json
from datetime import datetime

# return current value if no date is found
# return previous value if a date is provided, as well as most recent

# http://theautomatic.net/2018/12/18/2-packages-for-extracting-dates-from-a-string-of-text-in-python/

#latest = ['now', 'today', 'current', 'actual', 'latest']

def main(text, data, latest):

	# debugging
	#text = "Today is 12-01-18 thank you"
	#text = "Today is 2018-01-01 thank you"
	#text = "Now is June 1st, 2020 thank you"
	#text = "now, and 01 June 2020 or perhaps August/15/1980 and 08/15/1980 and again now 09/15/2020"
	#text = "abc"

	# find all dates in text
	dates_list = find_dates(text)

	# remove today since it's already provided in the response
	if dates_list is not None:

		# get dates only (ignore text)
		dates_list = [d[1].date() for d in dates_list]

		# remove today, since it's added anyway
		dates_list = [d for d in dates_list if d not in [datetime.now().date()]]

		# convert to string
		dates_list = [d.strftime('%Y-%m-%d') for d in dates_list]
		
		# get unique dates, sort reverse order
		dates_list = sorted(list(set(dates_list)))[::-1]

	# get current value
	current_date = latest.get('date')
	current_value = latest.get('ppm')

	reply = []
	if dates_list is None:
		reply.append('Here is the most recent atmospheric CO₂ measurement:')
		reply.append(current_date+': '+str(current_value)+' ppm')

	else:
		reply.append('Here are your atmospheric CO₂ measurements:')

		for d in dates_list:
			print(d)
			previous = next((item for item in data if item['date'] == d), None)
			if previous is None:
				continue
			previous_value = previous.get('ppm')

			percent_change = round(100.0 * (current_value - previous_value) / previous_value,1)
			if percent_change > 0:
				reply.append(d+': '+str(previous_value)+' ppm (+' + str(percent_change) + '%)' + '📈'*int(percent_change/5) )
			else:
				reply.append(d+': '+str(previous_value)+' ppm (' + str(percent_change) + '%)')

		reply.append(current_date+': '+str(current_value)+' ppm (latest)' + '🌡️🔥')

	reply.append('more info: https://co2birth.date #co2birthdate')

	reply = '\n'.join(reply)

	print(reply)
	return reply

def find_dates(t):

	return search_dates(t)

def load_data():

	if True:
		# get online versions (use this old commit, since the current input data is borked)
		data = requests.get('https://raw.githubusercontent.com/co2birthdate/dataops/37e471357b893d6a3a55a50a58a297365a437434/output_data/co2.json').json()
		latest = requests.get('https://raw.githubusercontent.com/co2birthdate/dataops/37e471357b893d6a3a55a50a58a297365a437434/output_data/latest.json').json()
		#data = requests.get('https://github.com/co2birthdate/dataops/raw/master/output_data/co2.json').json()
		#latest = requests.get('https://github.com/co2birthdate/dataops/raw/master/output_data/latest.json').json()
	else:
		# use local in git submodule (or for debugging)
		with open('dataops/output_data/co2.json','r') as d:
			data = json.load(d)

		with open('dataops/output_data/co2.json','r') as d:
			latest = json.load(d)
	
	return data, latest


if __name__ == "__main__":

	data, latest = load_data()

	main('Today is 1980-01-01 thank you', data, latest)
