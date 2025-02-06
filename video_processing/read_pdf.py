import pdfplumber
from typing import List
import re

# this is not properly working because out of bounds
# are not documented on box score

raw_jump_ball_time = "" #Stores the time of the jump ball in "MM:SS" format.
home_players = [] #List of players on the home team.
away_players = [] #List of players on the away team.
previous_time = None #Stores the last timestamp processed.
clean_clips = [] #List of cleaned and adjusted clip tuples.

def cleanup_clip_tuples(clips):
    """
       Adjusts clip times based on the quarter and ensures proper alignment.
       Parameters:
           clips (List[Tuple[int, int]]): List of start and end times for clips.
       Global Variables:
           clean_clips, raw_jump_ball_time
    """
    quarter = 1
    global clean_clips
    global raw_jump_ball_time
    jump_ball_time = time_to_seconds(raw_jump_ball_time)
    for group in clips:
        start, end = group
        start += jump_ball_time
        end += jump_ball_time
        if group == clips[0] and start != 0:
            clean_clips.append((0 + jump_ball_time, start))
        if start == end:
            continue
        elif start > end:
            quarter += 1
            if start != (600 + jump_ball_time):
                clean_clips.append(((quarter - 1) * 600 - (600 - start), (quarter - 1) * 600))
                clean_clips.append(((quarter - 1) * 600, (quarter - 1) * 600 + end))
            else:
                clean_clips.append(((quarter - 1) * 600 , (quarter - 1) * 600 + end ))
        elif quarter == 1:
            clean_clips.append((start, end))
        elif quarter == 2:
            clean_clips.append((start + 600, end + 600))
        elif quarter == 3:
            clean_clips.append((start + 1200, end + 1200))
        elif quarter == 4:
            clean_clips.append((start + 1800, end + 1800))

def create_clip_tuples(tuples):
    """
       Processes actions like "GOOD," "MISS," and timeouts to create intervals.
       Parameters:
           tuples (List[Tuple[str, int, str]]): List of action, timestamp, and player info.
       Global Variables:
           clean_clips
    """
    clips = []
    last_clip_time = None
    last_player = None
    last_timeout_time = None
    total_timeout_adjustment = 0  # Track the total timeout adjustment
    shot_padding = 4 #shot adjustment
    turnover_padding = 7 #the ball must go out of bounds
    for group in tuples:
        action = group[0]
        time = group[1]
        player = group[2]
        rebound_team = home_or_away(player, last_player)
        # Adjust clip times based on timeouts
        if action == "GOOD":
            if last_clip_time is not None:
                clips.append((600 - last_clip_time + total_timeout_adjustment, 600 - time + total_timeout_adjustment + shot_padding))
            last_clip_time = time
            last_player = player
        elif action == "MISS":
            if last_clip_time is not None:
                if rebound_team == 0:
                    clips.append((600 - last_clip_time + total_timeout_adjustment, 600 - time + total_timeout_adjustment + shot_padding))
                last_clip_time = time
            last_player = player
        elif action == "TURNOVER":
            if last_clip_time is not None:
                clips.append((600 - last_clip_time + total_timeout_adjustment, 600 - time + total_timeout_adjustment + turnover_padding))
            last_clip_time = time - turnover_padding
            last_player = player
        elif action == "TIMEOUT 30SEC" or action == "TIMEOUT MEDIA" or action == "TIMEOUT 60SEC":
            # Only add a timeout if the last action wasn't already a timeout
            if last_timeout_time != time:
                if action == "TIMEOUT 30SEC":
                    clips.append((600 - last_clip_time + total_timeout_adjustment - 5, 600 - time + 35 + total_timeout_adjustment))
                    total_timeout_adjustment += 35
                elif action == "TIMEOUT MEDIA" or action == "TIMEOUT 60SEC":
                    clips.append((600 - last_clip_time + total_timeout_adjustment - 5, 600 - time + 65 + total_timeout_adjustment))
                    total_timeout_adjustment += 65
                last_timeout_time = time
    cleanup_clip_tuples(clips)

def home_or_away(player, previous_player):
    """
        Checks if the action involves the home or away team.
        Parameters:
            player (str): Current player involved in the action.
            previous_player (str): Last player involved in an action.
        Returns:
            int: 1 if from the same team as the previous action, 0 otherwise.
        Global Variables:
            home_players, away_players
    """
    if player in home_players and previous_player in home_players:
        return 1
    elif player in away_players and previous_player in away_players:
        return 1
    elif player == "TEAM":
        return 1
    else:
        return 0

def create_action_tuples(d):
    """
        Extracts actions, timestamps, and players to create action tuples.
        Parameters:
            d (List[List[str]]): Parsed text data from the PDF.
    """
    action_tuples = []
    for line in d:
        action_type = find_key_words(line)
        timestamp = find_timestamp_in_line(line)
        player = find_player_team_in_line(line)
        if player is None:
            action_tuples.append((action_type, timestamp, player))
        action_tuples.append((action_type, timestamp, player))
    create_clip_tuples(action_tuples)

def find_key_words(line):
    """
        Searches for action keywords.
        Parameters:
            line (List[str]): Words from a single line of text.
        Returns:
            Optional[str]: Action keyword or None if not found.
    """
    action_keywords = ["GOOD", "MISS", "FOUL", "REBOUND",
                       "TURNOVER", "SUB", "ASSIST", "STEAL", "BLOCK"]
    timeout_types = ["MEDIA", "30SEC", "60SEC"]
    for i, item in enumerate(line):
        if item in action_keywords:
            return item
        if item == "TIMEOUT":
            if i + 1 < len(line) and line[i + 1] in timeout_types:
                return f"TIMEOUT {line[i + 1]}"
            return "TIMEOUT"
    return None

def find_timestamp_in_line(line):
    """
        Finds the timestamp in a line of code using a regular
        expression pattern.

        Parameters:
            line (List[str]): Words from a single line of text.
        Returns:
            int: Timestamp in seconds.
        Global Variables:
            previous_time
    """
    global previous_time
    line = " ".join(line)
    time_pattern = r'\b([0-9]{2}):([0-9]{2})\b'
    time = re.findall(time_pattern, line)
    if not time:
        return previous_time
    new_time = time_to_seconds(f"{time[0][0]}:{time[0][1]}")
    previous_time = new_time
    return new_time

def time_to_seconds(time: str) -> int:
    """
        Converts a time string (HH:MM:SS or MM:SS) into total seconds.
        Parameters:
            time (str): Time in "MM:SS" format.
        Returns:
            int: Time in seconds.
    """
    parts = list(map(int, time.split(":")))
    if len(parts) == 3:  # HH:MM:SS format
        hours, minutes, seconds = parts
    elif len(parts) == 2:  # MM:SS format
        hours = 0
        minutes, seconds = parts
    else:
        raise ValueError("Invalid time format. Use HH:MM:SS or MM:SS.")
    return hours * 3600 + minutes * 60 + seconds


def find_player_team_in_line(line):
    """
        Extracts the player or TEAM from a line.
        Parameters:
            line (List[str]): Words from a single line of text.
        Returns:
            Optional[str]: Player or team name, or None if not found.
    """
    line = " ".join(line)
    player_pattern = r'\b([A-Za-z]+,[A-Za-z]+)\b'
    team = "TEAM"
    if team in line:
        return team
    player = re.findall(player_pattern, line)
    if not player:
        return None
    return player[0]

def create_player_arrays(d: List[List[str]]) -> None:
   """
       Extracts player names for home and away teams using a regular
       expression pattern.

       Parameters:
           d (List[List[str]]): Parsed text data from the PDF.

       Global Variables:
           home_players, away_players
    """
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
                   away_players.extend([player.lower() for player in players])
       elif header_count == 2:
           for item in row:
               players = re.findall(player_pattern, item)
               if players:
                   home_players.extend([player.lower() for player in players])
       if header_count >= 2 and "1st Play By Play" in whole_row:
           break


def get_jump_ball_time():
    """
        Ensures the user inputs a valid jump ball time in "HH:MM:SS" or "MM:SS" format.
        Global Variables:
            raw_jump_ball_time
    """
    global raw_jump_ball_time
    while True:
        try:
            raw_jump_ball_time = input("What time is the jump ball thrown? (HH:MM:SS or MM:SS): ").strip()
            parts = raw_jump_ball_time.split(":")
            if len(parts) == 3:  # HH:MM:SS format
                hours, minutes, seconds = map(int, parts)
            elif len(parts) == 2:  # MM:SS format
                hours = 0
                minutes, seconds = map(int, parts)
            else:
                raise ValueError("Invalid format. Use HH:MM:SS or MM:SS.")
            if not (0 <= minutes < 60 and 0 <= seconds < 60):
                raise ValueError("Minutes and seconds must be within valid ranges.")
            break
        except ValueError as e:
            print(
                f"Invalid time format: {e}. Please enter the time in HH:MM:SS or MM:SS format (e.g., 01:30:45 or 10:45).")

def load_pdf(file_path: str) -> List[List[str]]:
    """
        Extracts and processes text from a PDF.
        Parameters:
            file_path (str): Path to the PDF file.
        Returns:
            List[List[str]]: Parsed text data as lists of words.
        Purpose:
            Triggers the creation of player arrays and action tuples.
    """
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
    get_jump_ball_time()
    create_player_arrays(data)
    create_action_tuples(data)
    return data

