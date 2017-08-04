from dotenv import find_dotenv
from dotenv import load_dotenv
load_dotenv(find_dotenv())
import json, random, datetime, pytz, praw, os, redis

if __name__ == '__main__':
	r = redis.StrictRedis(
		host=os.environ.get('REDIS_HOST'),
		port=os.environ.get('REDIS_PORT'),
		password=os.environ.get('REDIS_PASSWORD')
	)
	with open('topics.txt') as topics_file:
		possible_topics = [t.strip() for t in topics_file.readlines() if t.strip() != '']
	random.shuffle(possible_topics)
	topics = []
	for possible_topic in possible_topics:
		if r.exists(possible_topic):
			continue
		topics.append(possible_topic)
		if len(topics) == int(os.environ.get('N_TOPICS_TO_POST')):
			break
	for topic in topics:
		r.set(topic, '')
		r.expire(topic, 31540000)
	post_title = 'Daily Discussion %s' % datetime.datetime.now(pytz.timezone('America/Chicago')).strftime('%-m/%-d')
	post_text = '\n\n&nbsp;\n\n'.join(['%s%s' % ('' if i==0 else ('ALT%s: ' % (i if i>1 else '')), topics[i]) for i in xrange(len(topics))])
	print '\n' + post_title + '\n----------------------\n'
	print post_text
	reddit = praw.Reddit(
		client_id=os.environ.get('REDDIT_CLIENT_ID'),
		client_secret=os.environ.get('REDDIT_CLIENT_SECRET'),
		user_agent=os.environ.get('REDDIT_USERNAME'),
		username=os.environ.get('REDDIT_USERNAME'),
		password=os.environ.get('REDDIT_PASSWORD')
	)
	subreddit = reddit.subreddit(os.environ.get('SUBREDDIT'))
	new_submission = subreddit.submit(post_title, selftext=post_text, send_replies=False)
	try:
		for submission in subreddit.hot(limit=10):
			if submission.stickied and submission.author == os.environ.get('REDDIT_USERNAME'):
				submission.mod.sticky(state=False)
		new_submission.mod.sticky(state=True, bottom=True)
	except:
		print 'Not a moderator! Cannot sticky!'


