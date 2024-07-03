# ffmpeg -i videoava.mp4 -filter_complex "[v:0]split=2[vtemp001][vout002];[vtemp001]scale=w=192:h=144[vout001]" -map "[vout001]" -c:v:0 libx264 -b:v:0 2000k -maxrate:v:0 2200k -bufsize:v:0 3000k -map "[vout002]" -c:v:1 libx264 -b:v:1 6000k -maxrate:v:1 6600k -bufsize:v:1 8000k -map a:0 -map a:1 -map a:2 -c:a aac -b:a 128k -ac 2 -f hls -hls_time 4 -hls_playlist_type event -hls_flags independent_segments -master_pl_name master.m3u8 -hls_segment_filename data%06d.ts 1 stream_%v.m3u8

from operator import indexOf
import os
import subprocess
import ffmpeg

resolutions = ["w=3840:h=2160", "w=1920:h=1080","w=1280:h=720","w=720:h=480","w=426:h=360","w=320:h=240","w=192:h=144"]
res_p = [2160, 1080, 720, 480, 360, 240, 144]
video_bitrates = [44000, 10000, 6500, 2500, 1000, 500, 250]
audio_bit_rate = "128k"
audio_streams = 1
hls_command = "ffmpeg -i "

def closest(K):
    return res_p[min(range(len(res_p)), key = lambda i: abs(res_p[i]-K))]

file_name = "sample_multi_audio.mp4"
file_name_for_directory = os.path.splitext(file_name)[0]
if os.path.exists(file_name_for_directory):
    target_path = os.getcwd() + "/" + file_name_for_directory+ "/"
else:
    os.mkdir(file_name_for_directory)
    target_path = os.getcwd() + "/" + file_name_for_directory+ "/"
os.chmod(target_path, 0o0777)
pwd = os.getcwd() + "/" + file_name

hls_command += pwd

hls_command += ' -filter_complex "[v:0]split='

probe = ffmpeg.probe(pwd)

video_streams = [stream for stream in probe["streams"] if stream["codec_type"] == "video"]
audio_streams = [stream for stream in probe["streams"] if stream["codec_type"] == "audio"]

resolution_height = video_streams[0]["height"]
audio_streams_count = len(audio_streams)

closest_resolution = closest(resolution_height)
index = res_p.index(closest_resolution)
count = 1
hls_video = ""
hls_split = ""
#  MAP**** -map "[vout001]" -c:v:0 libx264 -b:v:0 2000k -maxrate:v:0 2200k -bufsize:v:0 3000k -map "[vout002]" -c:v:1 libx264 -b:v:1 6000k -maxrate:v:1 6600k -bufsize:v:1 8000k 
# hls_map_video = " -map[vout000] -c:v:0 libx264 -b:v:0 "+str(video_bitrates[index])+"k -maxrate:v:0 "+str(video_bitrates[index])+"k"
hls_map_video = ""
hls_map_audio = ""
for i in range(index, len(resolutions)):
    disp_count = str(count)
    disp_map_count = str(count - 1)
    hls_split += "[vtemp00"+disp_count+"]"
    hls_video += ';[vtemp00'+disp_count+']scale='+resolutions[i]+'[vout00'+disp_count+']'
    hls_map_video += ' -map [vout00'+disp_count+'] -c:v:'+disp_count+'  libx264 -b:v:0 '+str(video_bitrates[i])+"k -maxrate:v:0 "+str(video_bitrates[i])+"k -bufsize:v:1 "+str(video_bitrates[i])+"k"
    count += 1

for i in range(audio_streams_count):
    hls_map_audio += " -map a:" + str(i)

hls_command += str(count - 1) + " " + hls_split + hls_video+ '"' + hls_map_video
hls_command += hls_map_audio + " -c:a aac -b:a "+audio_bit_rate + " -ac 2 -f hls -hls_time 4 -hls_playlist_type event -hls_flags independent_segments -master_pl_name "+file_name_for_directory+'.m3u8 -hls_segment_filename data'+"%06"+'d.ts 1 stream_%v.m3u8'

final_hls_command = f'cd {file_name_for_directory} && {hls_command}'
print(final_hls_command)

print("***************************************************************************************************")
print("***************************************************************************************************")
print("***************************************************************************************************")
print("************************************Starting the HLS Convertion************************************")
print("***************************************************************************************************")
print("***************************************************************************************************")
print("***************************************************************************************************")
print("***************************************************************************************************")

subprocess.call(final_hls_command, shell=True)