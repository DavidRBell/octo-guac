from bs4 import BeautifulSoup
import os
import requests
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import string

def main():
    Base = declarative_base()
    engine = create_engine('mysql://readwrite:'+os.environ["READ_WRITE_PASS"]+'@localhost/futurama')
    Session = sessionmaker(bind=engine)
    session = Session()

    page = requests.get("https://theinfosphere.org/Transcript:Space_Pilot_3000")

    if page.status_code ==requests.codes.ok:
        parse_page_content(session, page.content)

def parse_page_content(session, content):
    """Parses the content of a requests request using the presets I've coded in for the Futuruma pages and inserts it into the db.

    Input:
        session (sqlalchemy.Session): activated SQLAlachemy session we can use to insert the row.
        content (content of a requests request): The content of the page we scraped.
    Returns:
        Nothing.
    """
    
    soup = BeautifulSoup(content, 'html.parser')
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
            dialogue_line = Dialogue(season=1, episode=1, character_name=cleaned_line[0].strip(), episode_time=seconds, line=cleaned_line[2].strip())
            session.add(dialogue_line)
        except Exception as e:
            print(line)
            print(e)

    session.commit()
   

class Dialogue(declarative_base()):
    """Represents a line of dialogue from a tv show or movie.

    Attributes:
        season (int): Which season it's from.
        episode (int): episode number.
        character_name (str): Name of the character who says the line.
        episode_time (int): Time of the line in seconds from the start of the show.
        line (str): The actual line.
        """

    __tablename__ = "dialogue"
    season = Column(Integer, primary_key = True)
    episode = Column(Integer, primary_key = True)
    character_name = Column(String, primary_key = True)
    episode_time = Column(Integer, primary_key = True)
    line = Column(String)


if __name__ == "__main__":
    main()

