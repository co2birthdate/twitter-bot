from dateparser.search import search_dates
import requests
import json
from datetime import datetime

# return current value if no date is found
# return previous value if a date is provided, as well as most recent

# http://theautomatic.net/2018/12/18/2-packages-for-extracting-dates-from-a-string-of-text-in-python/

#latest = ['now', 'today', 'current', 'actual', 'latest']

def main(text='Today is 1980-01-01 thank you'):

	data, latest = load_data()

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
	current = round(list(latest.values())[0],1)


	reply = []
	if dates_list is None:
		reply.append('Here is the most recent atmospheric CO₂ measurement:')
		reply.append(list(latest.keys())[0]+': '+str(current)+' ppm')

	else:
		reply.append('Here are your atmospheric CO₂ measurements:')

		for d in dates_list:
			#print(d)
			previous = round(data.get(d,None),1)
			percent_change = round(100.0 * (current - previous) / previous,1)
			if percent_change > 0:
				reply.append(d+': '+str(previous)+' ppm (+' + str(percent_change) + '%)' + '📈'*int(percent_change/5) )
			else:
				reply.append(d+': '+str(previous)+' ppm (' + str(percent_change) + '%)')

		reply.append(list(latest.keys())[0]+': '+str(current)+' ppm (latest)' + '🌡️🔥')

	reply.append('more info: https://co2birth.date #co2birthdate')

	reply = '\n'.join(reply)

	print(reply)
	return reply

def find_dates(t):

	return search_dates(t)

def load_data():

	if True:
		# get online versions
		data = requests.get('https://github.com/co2birthdate/dataops/raw/master/output_data/co2.json').json()
		latest = requests.get('https://github.com/co2birthdate/dataops/raw/master/output_data/latest.json').json()
	else:
		# use local versions for debugging
		with open('data/co2.json','r') as d:
			data = json.load(d)

		with open('data/latest.json','r') as d:
			latest = json.load(d)
	
	return data, latest


if __name__ == "__main__":
	
	main()
