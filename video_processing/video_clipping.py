import cv2

game_times = []          ##placing of this might be wrong??
home_players = []
away_players = []

def cut_clips(v, s_time: float, e_time: float, out_path: str):
    #Find frames per second and convert times to frames
    fps = int(v.get(cv2.CAP_PROP_FPS))
    start_frame = int(s_time * fps)
    end_frame = int(e_time * fps)

    #Video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    frame_width = int(v.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(v.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(out_path, fourcc, fps, (frame_width, frame_height))

    #Fill in frames from start to end
    v.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    for current_frame in range(start_frame, end_frame):
        read, frame = v.read()
        if not read:
            print("Error: Could not read frame.")
            break
        out.write(frame)
    out.release()
    print(f"Clip saved to {out_path}")

# Example usage: Cutting a video using start and end times
def process_video(video_file_path, timestamps):
    video = cv2.VideoCapture(video_file_path)
    if not video.isOpened():
        print("Error: Could not open video.")
        return

    for i, (start_time, end_time) in enumerate(timestamps):
        output_path = f"clip_{i + 1}.mp4"
        cut_clips(video, start_time, end_time, output_path)

    video.release()
#starting from 0, the quarters also need to start at 0, 600, 1200, 1800
#original video does not start at tip off
#I need to make it so that the game_times are passed into the file in a tuple so that it can cut the clips
#The timeouts need to be clipped at a different time
#REDOUND could be O-Board