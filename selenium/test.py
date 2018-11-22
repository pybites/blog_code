from datetime import date
import os

from dateutil.relativedelta import relativedelta
import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

HOMEPAGE = "https://codechalleng.es"
TODAY = date.today()

USER_NAME = os.environ['USER_NAME']
USER_PASSWORD = os.environ['USER_PASSWORD']


def _make_3char_monthname(dt):
    return dt.strftime('%b').upper()


@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


def test_loggedout_homepage(driver):
    driver.get(HOMEPAGE)
    expected = "PyBites Code Challenges | Hone Your Python Skills"
    assert driver.title == expected


def test_loggedin_dashboard(driver):
    driver.get(HOMEPAGE)
    driver.find_element_by_class_name('ghLoginBtn').click()
    driver.find_element_by_name('login').send_keys(USER_NAME)
    driver.find_element_by_name('password').send_keys(USER_PASSWORD +
                                                      Keys.RETURN)

    h2s = [h2.text for h2 in driver.find_elements_by_tag_name('h2')]
    expected = [f'Happy Coding, {USER_NAME}!',
                'PyBites Platform Updates [all]',
                'PyBites Ninjas (score ≥ 50)',
                'Become a better Pythonista!',
                'Keep Calm and Code in Python!    SHARE ON TWITTER']
    for header in expected:
        assert header in h2s, f'{header} not in h2 headers'

    # calendar / coding streak feature
    this_month = _make_3char_monthname(TODAY)
    last_month = _make_3char_monthname(TODAY-relativedelta(months=+1))
    two_months_ago = _make_3char_monthname(TODAY-relativedelta(months=+2))
    for month in (this_month, last_month, two_months_ago):
        month_year = f'{month} {TODAY.year}'
        assert month_year in h2s, f'{month_year} not in h2 headers'

    # only current date is marked active
    assert len(driver.find_elements_by_class_name('today')) == 1


def test_coding_streak_calendar_widget(driver):
    pass
    # I challenge you!
    # write some code to do a bite save, or log progress on a challenge,
    # or update a 100 days grid, then see if the calendar's cell for today
    # turned green
