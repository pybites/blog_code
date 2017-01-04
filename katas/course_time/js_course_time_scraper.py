#!python3
# js_course_time_scraper.py is a tool to scrape the html of the Watch and Code
# JS course to see how long the actual course is in total. It's not listed
# on the course page/site anywhere thus the necessity of this tool.

import re

HTML_FILE = "content.html"
MM_SS_SEP = ':'
SECONDS_IN_MIN = 60
SECONDS_IN_HOUR = 60 * SECONDS_IN_MIN
TIME_REGEX = re.compile(r'\(\d+:\d+\)') 


def get_all_timestamps():
    with open(HTML_FILE) as f:
        return TIME_REGEX.findall(f.read()) 
    
def calc_duration(durations):
    sum_seconds = 0
    for mm_ss in durations:
        minutes, seconds = mm_ss.strip('()').split(MM_SS_SEP)
        sum_seconds += int(minutes) * SECONDS_IN_MIN + int(seconds)
    return sum_seconds 


if __name__ == "__main__":
    video_timings = get_all_timestamps()
    total_seconds = calc_duration(video_timings)
    total_hours = float(total_seconds / SECONDS_IN_HOUR)
    assert str(total_hours) == '6.841944444444445'
    print('The course takes ' + str(total_hours) + ' hours to complete.')
