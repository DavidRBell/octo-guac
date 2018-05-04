import _mysql
import os
import requests
import string
from collections import defaultdict
from bs4 import BeautifulSoup

page = requests.get("https://theinfosphere.org/Transcript:Space_Pilot_3000")
character_lines_by_name = defaultdict(list)

if page.status_code !=requests.codes.ok:
    print("Error fetching page")
    exit

db= _mysql.connect("localhost","readwrite",os.environ["READ_WRITE_PASS"],"futurama")

soup = BeautifulSoup(page.content, 'html.parser')
prose = soup.find_all('div', class_='poem')
for x in prose:
    try:
        line =(x.get_text())
        line = ''.join(filter(lambda x: x in string.printable, line))
        split_on_bracket = line.partition(")")
        time = (split_on_bracket[0]).strip()[1:]
        minutes_and_seconds = time.partition(":")
        seconds = (int(minutes_and_seconds[0]))*60 + (int(minutes_and_seconds[2]))
        trimmed_out_time = split_on_bracket[2]
        cleaned_line = trimmed_out_time.partition(":")
        dialogue_line = Dialogue(1,1,cleaned_line[0].strip(),seconds, cleaned_line[2].strip())
        
    except Exception as e:
        print(line)
        print(e)

def insert_into_db(dialogue):
    """Function which takes in a line of Dialogue and writes it to the db.

    Input:
        dialogue (Dialogue): the line of dialogue. See below for class explanation.

    """
    

class Dialogue(object):
    """Represents a line of dialogue from a tv show or movie.

    Attributes:
        season (int): Which season it's from.
        episode (int): episode number.
        character_name (str): Name of the character who says the line.
        time (int): Time of the line in seconds from the start of the show.
        line (str): The actual line.
        """

    def __init__(self, season, episode, character, time, line):
        self.season = season
        self.episode = episode
        self.character_name = character
        self.time = time
        self.line = line


