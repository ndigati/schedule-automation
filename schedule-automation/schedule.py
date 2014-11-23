import requests
import configparser
from bs4 import BeautifulSoup

def get_login_info(filename):
    logins = {}
    config = configparser.ConfigParser()
    config.read(filename)
    logins[config['USHER_LOGIN']['username']] = config['USHER_LOGIN']['password']
    logins[config['CREW_LOGIN']['username']] = config['CREW_LOGIN']['password']
    return logins

def http_fetch():
    logins = get_login_info('login.ini')
    crewLogin = ()
    usherLogin = ()
    for key in logins:
        if 'crew' in key:
            crewLogin = (key, logins[key])
        else:
            usherLogin = (key, logins[key])

    payload = {"NAS_id": 76003,
            "name": "signin",
            "UserId1": usherLogin[0] ,
            "Password1": usherLogin[1],
            "Submit1": "Please Wait..."
            }
    s = requests.Session()
    r = s.post('http://whentowork.com/cgi-bin/w2w.dll/login', data=payload)
    index = r.url.index('=')
    sid = r.url[index+1:]
    r = s.get('https://www3.whentowork.com/cgi-bin/w2wC.dll/empschedule?SID={0}'.format(sid))
    parse_html(r.text)

def parse_html(html):
    soup = BeautifulSoup(html)
    print(soup.prettify())


if __name__ == '__main__':
    http_fetch()
