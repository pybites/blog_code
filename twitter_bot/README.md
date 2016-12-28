## README

A bot to help us automate part of our [@pybites](https://twitter.com/pybites) posting.

We use this in a daily cronjob and watch the following feeds: 

	$ more feeds 
	http://pybit.es/feeds/all.rss.xml
	https://talkpython.fm/episodes/rss
	https://pythonbytes.fm/episodes/rss
	https://dbader.org/rss
	https://www.codementor.io/python/tutorial/feed
	http://feeds.feedburner.com/PythonInsider
	http://www.weeklypython.chat/feed/ 


## Use it for your own Twitter / feeds

	$ pyvenv venv
	$ source venv/bin/activate
	$ pip install -r requirements.txt
	$ mv config.py-example config.py (and edit it with your secret key/token etc)
	$ vi feeds (put your own feeds in)
