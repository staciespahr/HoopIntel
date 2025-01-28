import cv2

def cut_clips(v, s_time: float, e_time: float, out_path: str):
    """
       Extracts a video clip from the given video object based on start and end times
       and saves it to the specified output path.

       Args:
           v (cv2.VideoCapture): OpenCV VideoCapture object for the video.
           s_time (float): Start time in seconds for the clip.
           e_time (float): End time in seconds for the clip.
           out_path (str): File path to save the extracted video clip.

       Returns:
           None
       """
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


def process_video(video_file_path, timestamps):
    """
        Processes a video file by extracting multiple clips based on the provided timestamps.

        Args:
            video_file_path (str): Path to the video file.
            timestamps (list[tuple[float, float]]): List of (start_time, end_time) tuples
                                                    specifying clip ranges in seconds.

        Returns:
            None
        """
    video = cv2.VideoCapture(video_file_path)
    if not video.isOpened():
        print("Error: Could not open video.")
        return
    for i, (start_time, end_time) in enumerate(timestamps):
        output_path = f"clip_{i + 1}.mp4"
        cut_clips(video, start_time, end_time, output_path)
    video.release()
