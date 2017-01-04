#!python3
# js_course_time_scraper.py is a tool to scrape the html of the Watch and Code
# JS course to see how long the actual course is in total. It's not listed
# on the course page/site anywhere thus the necessity of this tool.

import re

#Specify file to read in
HTML_FILE = "content.html"
SECONDS_IN_MIN = 60
SECONDS_IN_HOUR = 60 * SECONDS_IN_MIN
TIME_REGEX = re.compile(r'\(\d+:\d+\)') #Creating the regex


#Read in the HTML file and search it for time regex
def get_all_timestamps():
    with open(HTML_FILE) as f:
        return TIME_REGEX.findall(f.read()) #Searching for regex and returning it
    
#Strip out the brackets and the colon
def calc_duration(durations):
    sum_seconds = 0
    #For loop to strip brackets/colon and assign the mins/seconds
    for mm_ss in durations:
        minutes, seconds = mm_ss.strip('()').split(':')
        sum_seconds += int(minutes) * SECONDS_IN_MIN
        sum_seconds += int(seconds)
    return sum_seconds #Returns the sum of all mins/seconds


if __name__ == "__main__":
    #Call on search function and assign regex output to variable
    time_list = get_all_timestamps()

    #Call time calc function and assign min & sec output to variables
    total_seconds = calc_duration(time_list)

    #Calculates total hours of course by adding mins + secs together
    total_hours = float(total_seconds / SECONDS_IN_HOUR)

    assert str(total_hours) == '6.841944444444445'

    print('The course takes ' + str(total_hours) + ' hours to complete.')
