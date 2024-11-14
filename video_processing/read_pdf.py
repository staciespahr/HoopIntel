import pdfplumber
from typing import List
import re

game_times = []          ##placing of this might be wrong??
clip_tuples = []
home_players = []
away_players = []

#might delete
def write_to_file(d, output_file: str):
    try:
        with open(output_file, 'w') as file:
            for item in d:
                file.write(f"{item}\n")
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")

def create_clip_tuples():
    global game_times
    global clip_tuples
    time_tuples = []
    # helper method
    def convert_to_seconds(time_str):
        minutes, seconds = map(int, time_str.split(":"))
        return minutes * 60 + seconds
    #helper method
    def quarter_convertor():
        quarter = 1
        for t in time_tuples:
            first = t[0]
            second = t[1]
            if quarter == 1:
                clip_tuples.append((600 - first, 600 - second))
            elif quarter == 2:
                clip_tuples.append((1200 - first, 1200 - second)) #these also might be wrong
            elif quarter ==3:
                clip_tuples.append((1800 - first, 1800 - second))
            elif quarter == 4:
                clip_tuples.append((2400 - first, 2400 - second))
            if second == 600:
                quarter += 1 #this is wrong

    for i in range(len(game_times) - 1):
        if game_times[i] != game_times[i+1]:
            start_seconds = convert_to_seconds(game_times[i])
            end_seconds = convert_to_seconds(game_times[i + 1])
            if start_seconds < end_seconds:
                time_tuples.append((start_seconds, 0))
            else:
                time_tuples.append((start_seconds, end_seconds))
    quarter_convertor()

def create_time_array(d):
    global game_times
    time_pattern = r'\b([0-9]{2}):([0-9]{2})\b'
    #insert game start time.
    if not game_times:
        game_times.append("10:00")
    for row in d:
        for item in row:
            times = re.findall(time_pattern, item)
            for time in times:
                game_times.append(f"{time[0]}:{time[1]}")

def create_player_arrays(d):
    global home_players, away_players
    player_pattern = r'\b([A-Za-z]+,[A-Za-z]+)\b'
    header_count = 0
    for row in d:
        whole_row = " ".join(row)
        if whole_row == "# Player GS MIN FG 3PT FT ORB-DRB REB PF A TO BLK STL PTS":
            header_count += 1
            continue
        if header_count == 1:
            for item in row:
                players = re.findall(player_pattern, item)
                if players:
                    away_players.extend(players)
        elif header_count == 2:
            for item in row:
                players = re.findall(player_pattern, item)
                if players:
                    home_players.extend(players)
        if header_count >= 2 and "1st Play By Play" in whole_row:
            break

def load_pdf(file_path: str) -> List[List[str]]:
    data = []
    try:
        with pdfplumber.open(file_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text:
                    lines = text.splitlines()
                    for line in lines:
                        if line.strip():  # Skip any empty lines
                            data.append(line.split())  # Split by spaces and add to data
                else:
                    print(f"Page {page_num + 1} is empty or has no extractable text.")
    except Exception as e:
        print(f"An error occurred while opening the PDF: {e}")
    return data

#clips need to be changes to seconds starting from 0, the quarters also need to start at 0, 600, 1200, 1800
#original video does not start at tip off
#I need to make it so that the game_times are passed into the file in a tuple so that it can cut the clips
#The timeouts need to be clipped at a different time
#REDOUND could be O-Board