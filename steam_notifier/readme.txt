XML Steam Scraper

A program to parse the steam XML feed for new titles.

1. Run pull_xml.py to pull down the steam newreleases XML feed.

2. Run xml_steam_scraper.py to parse the feed and save the game names and URLs to an sqlite database. (The db will be created on first run).

3. Populate email_list.py with email addresses.

4. Run emailer.py to send yourself the list of newly released games.

5. Automate this by adding each of the scripts (pull, scraper and emailer) to crontab in order. I'd recommend leaving a minute or two between each script run.

6. Set cron to run the 3 entries every day. The end result will be a daily email of the latest games as they're added to Steam.

7. The program is configured such that once a game has been emailed to you, it won't be emailed again.


CRONTAB ENTRY EXAMPLE TO RUN SCRIPT AT 8:30PM DAILY:

30 20 * * * cd /opt/development/steamscraper && /usr/bin/python3 pull_xml.py
