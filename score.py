import requests
from bs4 import BeautifulSoup
from win10toast import ToastNotifier
import re

from time import sleep


def ascii_art():
    
    print("""
 _____    _____ ____   ____ _________                ______ _______    _____   ______ ___  ____  _________ _________               _______   ______   ____   _______    _________ 
|_   _|  |_   _|_  _| |_  _|_   ___  |             ./ ___  |_   __ \  |_   _|./ ___  |_  ||_  _||_   ___  |  _   _  |             /  ___  |./ ___  |.'    \.|_   __ \  |_   ___  |
  | |      | |   \ \   / /   | |_  \_|            / ./   \_| | |__) |   | | / ./   \_| | |_/ /    | |_  \_|_/ | | \_|            |  (__ \_| ./   \_|  .--.  \ | |__) |   | |_  \_|
  | |   _  | |    \ \ / /    |  _|  _             | |        |  __ /    | | | |        |  __'.    |  _|  _    | |                 '.___\-.| |      | |    | | |  __ /    |  _|  _ 
 _| |__/ |_| |_    \ ' /    _| |___/ |   ______   \ \.___.'\_| |  \ \_ _| |_\ \.___.'\_| |  \ \_ _| |___/ |  _| |_      ______   |\\____) | \.___.'\  \--'  /_| |  \ \_ _| |___/ |
|________|_____|    \_/    |_________|  |______|   \._____.'____| |___|_____|\._____.'____||____|_________| |_____|    |______|  |_______.'\._____.'\.____.'|____| |___|_________|
""")


def get_current_matches():
    
    page = requests.get('http://static.cricinfo.com/rss/livescores.xml')  
    soup = BeautifulSoup(page.text, 'xml')  
    matches = soup.find_all('description')  
    live_matches = [s.get_text() for s in matches if
                    '*' in s.get_text()]  
    return live_matches


def fetch_score(matchNum):
    
    page = requests.get('http://static.cricinfo.com/rss/livescores.xml')
    soup = BeautifulSoup(page.text, 'xml')
    matches = soup.find_all('description')
    live_matches = [s.get_text() for s in matches if '*' in s.get_text()]
    return live_matches[matchNum]


def notify(score,support):
    
    toaster = ToastNotifier()
    toaster.show_toast(score,
                       f"Come on!!! {support},Go!",
                       duration=10)


### The Main Function ###
if __name__ == "__main__":
    ascii_art()
    matches = get_current_matches()
    print('Current matches in play')
    print('=' * 23)

    for i, match in enumerate(matches):
        print('[{}] '.format(i) +
              re.search('\D+', match.split('v')[0]).group() + 'vs.' +
              re.search('\D+', match.split('v')[1]).group()
              )

    print()
try:
    matchNum = int(input('Pick the match number [0, 1, 2, ...] => '))
    if matchNum < 0 or matchNum >= len(matches):
        print("Invalid match number. Please select a valid match number.")
    else:
        support = input("Enter the team you are supporting: ")
       
except ValueError:
    print("Invalid input. Please enter a valid numeric match number.")

    
    while True:
        current_score = fetch_score(matchNum)
        notify(current_score,support)
        sleep(30)
