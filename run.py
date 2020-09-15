import tweepy
import time
from dotenv import load_dotenv
import os

import get_dates

# replies with co2 values
# "borrowed" from https://stackoverflow.com/a/59978258/2327328

def create_api():

	load_dotenv()

	consumer_key = os.environ.get("TWITTER_CONSUMER_KEY")
	consumer_secret = os.environ.get("TWITTER_CONSUMER_SECRET")
	access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
	access_token_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth, wait_on_rate_limit=False, wait_on_rate_limit_notify=False)

	api.verify_credentials()

	return api

def check_mentions(api, since_id):

	new_since_id = since_id
	for tweet in tweepy.Cursor(api.mentions_timeline, since_id=since_id).items():
		new_since_id = max(tweet.id, new_since_id)
		if tweet.in_reply_to_status_id is not None:
			continue

		#if not tweet.user.following:
		#	tweet.user.follow()

		reply = get_dates.main(tweet.text)
		with open('log.txt','a') as fp:
			#print(tweet.id, tweet.text)
			fp.write(str(tweet.id)+': '+tweet.text+'\n')
		try:
			api.update_status(status=reply,in_reply_to_status_id=tweet.id,)
		except:
			pass # avoid duplicate replies

	return new_since_id

def main():
	api = create_api()

	with open('since.txt','r') as fp:
		since_id = int(fp.read())

	# debugging
	#since_id = 1
	#print(since_id)

	since_id = check_mentions(api, since_id)
	
	with open('since.txt','w') as fp:
		fp.write(str(since_id))

if __name__ == "__main__":
	main()