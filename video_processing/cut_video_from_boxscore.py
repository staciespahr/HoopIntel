from read_pdf import *
from video_clipping import process_video
import requests

#pdf
willamette_pdf = "/Users/stacie/Desktop/Capstone/PycharmProjects/HoopIntel/box_scores/willamette_box_score.pdf"
george_fox_pdf = "/Users/stacie/Desktop/Capstone/PycharmProjects/HoopIntel/box_scores/george_fox_box_score.pdf"
puget_sound_pdf = "/Users/stacie/Desktop/Capstone/PycharmProjects/HoopIntel/box_scores/puget_sound_box_score.pdf"
lewis_pdf = "/Users/stacie/Desktop/Capstone/PycharmProjects/HoopIntel/box_scores/lewis_box_score.pdf"
pacific_pdf = "/Users/stacie/Desktop/Capstone/PycharmProjects/HoopIntel/box_scores/pacific_box_score.pdf"

#video
george_fox_vid_cloud = "https://storage.googleapis.com/hoopintel_dataset/george_fox_video.mp4"
george_fox_vid_path = "george_fox_video.mp4"
lewis_vid_cloud = "https://storage.googleapis.com/hoopintel_dataset/lewis_video.mp4"
lewis_vid_path = "lewis_video.mp4"
pacific_vid_cloud = "https://storage.googleapis.com/hoopintel_dataset/pacific_video.mp4"
pacific_vid_path = "pacific_video.mp4"
puget_sound_vid_cloud = "https://storage.googleapis.com/hoopintel_dataset/puget_sound_video_.mov"
puget_sound_vid_path = "puget_sound_video.mov"
willamette_vid_cloud = "https://storage.googleapis.com/hoopintel_dataset/willamette_video.mp4"
willamette_vid_path = "willamette_video.mp4"

response = requests.get(george_fox_vid_cloud, stream=True, timeout=300)
if response.status_code == 200:
    print(f"Starting download from {george_fox_vid_cloud}...")
    with open(george_fox_vid_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    print("Video downloaded successfully.")
else:
    print(f"Failed to download video from {george_fox_vid_cloud}. Status code: {response.status_code}")

load_pdf(george_fox_pdf)
process_video(george_fox_vid_path, clean_clips[:4])
#george fox start time is 14:53
#lewis and clack sound start time is 22:10
#pacific sound start time is 04:09
#puget sound start time is 00:02
#willamette start time is 19:12


