from dotenv import find_dotenv
from dotenv import load_dotenv
load_dotenv(find_dotenv())
from os import environ, path
import json, random, datetime, pytz, praw, redis

if __name__ == '__main__':
	r = redis.StrictRedis(
		host=environ.get('REDIS_HOST'),
		port=environ.get('REDIS_PORT'),
		password=environ.get('REDIS_PASSWORD')
	)
	with open(path.join('data', 'prompts.txt')) as topics_file:
		possible_topics = [t.strip() for t in topics_file.readlines() if t.strip() != '']
	random.shuffle(possible_topics)
	topics = []
	for possible_topic in possible_topics:
		if r.exists(possible_topic):
			continue
		topics.append(possible_topic)
		if len(topics) == int(environ.get('N_TOPICS_TO_POST')):
			break
	for topic in topics:
		r.set(topic, '')
		r.expire(topic, 31540000)
	post_title = 'Daily Discussion %s' % datetime.datetime.now(pytz.timezone('America/Chicago')).strftime('%-m/%-d')
	post_text = '\n\n&nbsp;\n\n'.join(['%s%s' % ('' if i==0 else ('ALT%s: ' % (i if i>1 else '')), topics[i]) for i in xrange(len(topics))])
	reddit = praw.Reddit(
		client_id=environ.get('REDDIT_CLIENT_ID'),
		client_secret=environ.get('REDDIT_CLIENT_SECRET'),
		user_agent=environ.get('REDDIT_USERNAME'),
		username=environ.get('REDDIT_USERNAME'),
		password=environ.get('REDDIT_PASSWORD')
	)
	subreddit = reddit.subreddit(environ.get('SUBREDDIT'))
	try:
		for submission in subreddit.hot(limit=10):
			if submission.stickied and submission.author == environ.get('REDDIT_USERNAME'):
				submission.mod.sticky(state=False)
	except:
		print 'Not a moderator! Cannot sticky!'
	new_submission = subreddit.submit(post_title, selftext=post_text, send_replies=False)
	try:
		new_submission.mod.sticky(state=True)
	except:
		print 'Not a moderator! Cannot sticky!'


