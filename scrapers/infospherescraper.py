import requests
import string
from collections import defaultdict
from bs4 import BeautifulSoup

page = requests.get("https://theinfosphere.org/Transcript:Space_Pilot_3000")
character_lines_by_name = defaultdict(list)

if page.status_code !=requests.codes.ok:
    print("Error fetching page")
    exit

soup = BeautifulSoup(page.content, 'html.parser')
prose = soup.find_all('div', class_='poem')
for x in prose:
    try:
        line =(x.get_text())
        line = ''.join(filter(lambda x: x in string.printable, line))
        trimmed_out_time = line.partition(")")[2]
        cleaned_line = trimmed_out_time.partition(":")
        character_lines_by_name[cleaned_line[0].strip()].append(cleaned_line[2])
    except e:
        print(e)

for line in character_lines_by_name["Fry"]:
    print(line)
