from read_pdf import load_pdf, create_time_array, create_clip_tuples, create_player_arrays, clip_tuples
from video_clipping import process_video

play_file_path = "/Users/stacie/Desktop/Capstone/Willamette_play_by_play.pdf"
data = load_pdf(play_file_path)
create_time_array(data)
create_clip_tuples()
create_player_arrays(data)
#print(clip_tuples)

video_file_path = "/Users/stacie/Desktop/Capstone/VideoExpress/Download/2024.01.06 - Willamette at PacificLutheran (3187199)/6599e60a644b910154973037.mp4"
partial_video_path = "/Users/stacie/Desktop/Capstone/VideoExpress/Download/2024.01.06 - Willamette at PacificLutheran (3187199)/partial_game.mp4"

timestamps = [(1, 15), (15,30), (30,40)]
process_video(partial_video_path, timestamps)  #change for real game



