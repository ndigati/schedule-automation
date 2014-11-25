import requests
import configparser
from bs4 import BeautifulSoup

def get_login_info(filename):
    '''
    This method is used to extract login info from the config (.ini) file in the same directory
    as the script file. Stores this login info in a dictionary and returns it to be used to login
    to the website.

    No error handling yet, needs to be done soon.

    If config file is not located in the same directory as the script, please supply the full path
    to the file.

    Parameters:
        filename = filename of config file (full path filename if not in same directory)

    Return:
        logins = dictionary containing login info (key: username, value: password)
    '''
    logins = {}
    config = configparser.ConfigParser()
    config.read(filename)
    logins[config['USHER_LOGIN']['username']] = config['USHER_LOGIN']['password']
    logins[config['CREW_LOGIN']['username']] = config['CREW_LOGIN']['password']
    return logins

def http_fetch():
    '''
    This method is used to login to the whentowork website and get the HTML containing the current week
    schedule.
    '''
    logins = get_login_info('login.ini')
    # Get the correct login from the dictionary returned from get_login_info method.
    # Need to add handling for when only one login is present in config.
    crewLogin = ()
    usherLogin = ()
    for key in logins:
        if 'crew' in key:
            crewLogin = (key, logins[key])
        else:
            usherLogin = (key, logins[key])

    # Set up the payload to pass to requests session
    payload = {"NAS_id": 76003,
            "name": "signin",
            "UserId1": usherLogin[0] ,
            "Password1": usherLogin[1],
            "Submit1": "Please Wait..."
            }
    s = requests.Session()
    r = s.post('http://whentowork.com/cgi-bin/w2w.dll/login', data=payload)
    index = r.url.index('=')

    # The SID that is appended to the url of every page on whentowork is the last 13 characters in the url
    # Since it is dynamically generated every login use this to get those last 13 characters.
    # Can then apped this SID to the end of any W2W pages to get the HTML
    sid = r.url[index+1:]
    r = s.get('https://www3.whentowork.com/cgi-bin/w2wC.dll/empschedule?SID={0}'.format(sid))
    parse_html(r.text)

def parse_html(html):
    '''
    Method to extract the scheduled work days from the HTML.

    Paramaters:
        html = string of HTML containing work schedule.
    '''
    soup = BeautifulSoup(html)
    print(soup.prettify())


if __name__ == '__main__':
    http_fetch()
