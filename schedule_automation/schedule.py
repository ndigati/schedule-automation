import requests
import configparser
import re
import sqlite3
from bs4 import BeautifulSoup


# global list of days of the week so it is available to all functions
WORK_DAYS = [
    "Sunday", "Monday", "Tuesday", "Wednesday",
    "Thursday", "Friday", "Saturday",
]


def get_login_info(filename):
    """
    This method is used to extract login info from the config (.ini) file in
    the same directory as the script file. Stores this login info in a
    dictionary and returns it to be used to login to the website.

    No error handling yet, needs to be done soon.

    If config file is not located in the same directory as the script, please
    supply the full path to the file.

    Parameters:
        filename = filename of config file (full path filename)

    Return:
        logins = dictionary containing login info
        (key: username, value: password)
    """
    logins = {}
    config = configparser.ConfigParser()
    config.read(filename)
    logins[config['USHER_LOGIN']['username']] = config['USHER_LOGIN']['password']
    logins[config['CREW_LOGIN']['username']] = config['CREW_LOGIN']['password']
    return logins


def http_fetch():
    """
    This method is used to login to the whentowork website and get the HTML
    containing the current week schedule.
    """
    logins = get_login_info('login.ini')
    # Get the correct login from the returned dictionary
    # Need to add handling for when only one login is present in config.
    crew_login = ()
    usher_login = ()
    for key in logins:
        if 'crew' in key:
            crew_login = (key, logins[key])
        else:
            usher_login = (key, logins[key])

    # Set up the payload to pass to requests session
    payload = {
        "NAS_id": 76003,
        "name": "signin",
        "UserId1": usher_login[0],
        "Password1": usher_login[1],
        "Submit1": "Please Wait..."
    }

    # Using a session so it can keep cookies to not have to log in again when
    # navigating to a new page.
    s = requests.Session()
    r = s.post('http://whentowork.com/cgi-bin/w2w.dll/login', data=payload)
    index = r.url.index('=')

    # The SID that is appended to the url of every page on whentowork is the
    # last 13 characters in the url.
    # Since it is dynamically generated every login, use this to get those last
    # 13 characters. Can then append this SID to the end of any W2W pages.
    sid = r.url[index+1:]
    r = s.get('https://www3.whentowork.com/cgi-bin/w2wC.dll/empschedule?SID'
              '={0}'.format(sid))
    return r.text
    #parse_html(r.text)


def parse_html(html):
    """
    Method to get the HTML containing the currently scheduled work days.

    Parameters:
        html = string of HTML containing work schedule.
    """
    soup = BeautifulSoup(html, 'html.parser')
    # Schedule is in an html table tag with the class bd.
    # Actual shift information is within a script tag under that table tag
    table = soup.find("table", class_="bd").find_all("script")

    shifts = []
    # Loop through each tag and then through each day to find appropriate html
    # Can probably be made more pythonic, but this works for now.
    for tag in table:
        for day in WORK_DAYS:
            if day in tag.text:
                shifts.append(tag.text)
    return shifts
    #working_shifts = extract_shifts(shifts)


def extract_shifts(shifts):
    """
    Method to extract and return the exact day, time, and shift info from the
    HTML containg the information.

    Parameters:
        shifts = list of HTML strings containing shift information
        days = list of days of the week to create final dict
    """
    pattern = re.compile(r"\"[0-9]:?([0-9]+)?[a|p]m.+?\"")
    working_shifts = {}
    for day in WORK_DAYS:
        working_shifts[day] = []
        for shift in shifts:
            if day in shift:
                shift_info = re.finditer(pattern, shift)
                for desc in shift_info:
                    working_shifts[day].append(desc.group(0))
    return working_shifts


class DBConnector(object):
    connection = None
    cursor = None

    def __init__(self):
        self.connection = sqlite3.connect('shiftDB.db')
        self.cursor = self.connection.cursor()

if __name__ == '__main__':
    schedule_html = http_fetch()
    shifts = parse_html(schedule_html)
    working_shifts = extract_shifts(shifts)
    #print(working_shifts)
    for day in working_shifts:
        if working_shifts[day]:
            print("{0} : {1}".format(day, working_shifts[day]))
