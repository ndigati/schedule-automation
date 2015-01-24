# Schedule Automation

This is a project used to scrape online work schedule, and use scraped data to alert the user when work days are approaching.

Runs on Python 3.4 and uses the requests and BeautifulSoup libraries.

###### To use:

1. Clone repository using `git clone https://github.com/ndigati/schedule-automation.git `
2. Install required libraries `pip install -r requirements.txt `
3. Create logins.ini file to have login info with headings `[USHER_LOGIN]` or `[CREW_LOGIN]` as needed
3. Run script using `python3 schedule-automation/schedule.py`


###### TODO:

1. Create Web Interface to handle users.
2. Create Database to store users schedules.
3. Set up a reminder system for scheduled shifts.
4. Implement Text messaging system for scheduled shifts.
