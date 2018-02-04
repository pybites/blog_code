#!python3
# js_course_time_scraper.py is a tool to scrape the html of the Watch and Code
# JS course to see how long the actual course is in total. It's not listed
# on the course page/site anywhere thus the necessity of this tool.
#
# update 4th of Feb 2018: solved bug and added more elegant way = datetime

from datetime import datetime, timedelta
import re

HTML_FILE = "content.html"


def get_all_timestamps():
    with open(HTML_FILE) as f:
        content = f.read()
        return re.findall(r'\d+:\d+', content)


def calc_duration(timings):
    total_seconds = 0
    for mm_ss in timings:
        minutes, seconds = mm_ss.split(':')
        total_seconds += int(minutes) * 60 + int(seconds)

    minutes, seconds = divmod(total_seconds, 60)
    hours, minutes = divmod(minutes, 60)

    return f'{hours}:{minutes}:{seconds}'


def calc_duration_improved(timings):
    start = datetime.now()
    end = datetime.now()

    for mm_ss in timings:
        minutes, seconds = mm_ss.split(':')
        end += timedelta(minutes=int(minutes), seconds=int(seconds))

    return str(end - start)


if __name__ == "__main__":
    timings = get_all_timestamps()

    # 1. using counting + divmod
    course_total = calc_duration(timings)
    assert str(course_total) == '6:50:31'

    # 2. using datetime (nicer)
    course_total = calc_duration_improved(timings)
    assert '6:50:31' in course_total

    print(f'The course takes {course_total} to complete')
