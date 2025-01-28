from read_pdf import *
from video_clipping import process_video

#pdf
play_file_path = "/Users/stacie/Desktop/Capstone/WillametteFilm/Willamette_play_by_play.pdf"
load_pdf(play_file_path) #everything is ran from here, but we can fix that

#video
#video_file_path = "/Users/stacie/Desktop/Capstone/willamette/willamette_video.mp4
video_before_jump = "/Users/stacie/Desktop/Capstone/willamette/Willamette_with_jump.mp4"

process_video(video_before_jump, clean_clips[:5])

#willanete start time is 00:12