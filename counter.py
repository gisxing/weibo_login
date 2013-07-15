#!/usr/bin/python
from weibo import APIClient

key = 'you app key'
sec = 'iyour app secret'

call_back = 'http://www.callbackurl.com/'


client = APIClient(app_key=key, app_secret=sec, redirect_uri=call_back)
url = client.get_authorize_url()
print url

# fetch this url , grant privilege , and get the 'code' from the call back url
r = client.request_access_token(code)


access_token = r.access_token 
expires_in = r.expires_in 
client.set_access_token(access_token, expires_in)

res = client.statuses.user_timeline.get()
print res['statuses'][0]['created_at']
print res['statuses'][0]['text']

from datetime import datetime, timedelta
time_gap = datetime.now() - timedelta(days = 30)

t_obj = datetime.strptime(t_str, '%a %b %d %H:%M:%S +0800 %Y')


# make a list for statuses' ids

ids = []
for current_page in xrange(1, 20):
	outdate = False
	res = client.statuses.user_timeline.get(page=current_page, count=100)
	for st in res['statuses']:
		create_time = st['created_at']
		create_time_obj = datetime.strptime(create_time, '%a %b %d %H:%M:%S +0800 %Y')
		if time_gap < create_time_obj:
			ids.append(st['id'])
		else:
			outdate = True
	if outdate:
		break

# get response info base on ids
group_by_src = {}
for status in ids:
	print "counting in status ID: %d" % status
	for current_page in xrange(1,11):
		res = client.comments.show.get(id = status, page=current_page, count=200)
		if not res['comments']:
			break
		print len(res['comments'])
		for comment in res['comments']:
			if group_by_src.get(comment['source'],False):
				group_by_src[comment['source']] +=1;
			else:
				group_by_src[comment['source']] = 1;

		
# get followers uids, and count their platform by the last post
from weibo import APIError
group_by_src = {}
uids = []
next_cursor = 0
for x in xrange(1,210):
        res = client.friendships.followers.ids.get(cursor=next_cursor, count=5000)
        uids += res['ids']
        next_cursor = res['next_cursor']
        if next_cursor == 0:
            print "end"
            break



uids = client.friendships.followers.ids.get(page=1, count=5000)['ids']
c = 1
for userid in uids:
	try:
		res = client.users.show.get(uid=userid)
	except APIError:
		print userid
		print str(APIError)
		continue
	if res.get('status', False):
		print c
		c += 1
		if res['status'].get('source', False):
			if group_by_src.get(res['status']['source'],False):
				group_by_src[res['status']['source']] +=1;
			else:
				group_by_src[res['status']['source']] = 1;
		
	

"""
pid = []	# pid list (400)
for p in xrange(1,5):
	res = client.statuses.user_timeline.get(page = p, count =100))
	for s in res['statuses']:
		pid.append(s['id'])
	
	
#get all coments!!

com_res = client.comments.show.get()
"""
