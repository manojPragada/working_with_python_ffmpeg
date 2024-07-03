# EXTRACT Audio
# ffmpeg -i videoava.mp4 -map 0:a:0 -c copy -map 0:a:1 -c copy -map 0:a:2 -c copy audio.mp4

# Combine and Generate FLS
# ffmpeg -i videoava.mp4 -i audio.mp4 -threads 0 -muxdelay 0 -y -map 0 -pix_fmt yuv420p -vsync 1 -async 1 -vcodec libx264 -r 29.97 -g 60 -refs 3 -f hls -hls_time 10 -hls_list_size 0 index.m3u8 -map 1 -acodec aac -strict experimental -async 1 -ar 44100 -ab 96k -f segment -segment_time 10 -segment_list_size 0 -segment_list_flags -cache -segment_format aac -segment_list audio.mp4

# -metadata:s:a:0 language=eng -metadata:s:a:0 title="Title 1" -metadata:s:a:1 language=sme -metadata:s:a:1 title="Title 2" -metadata:s:a:2 language=ipk -metadata:s:a:2 title="Title 3" -metadata:s:a:3 language=nob -metadata:s:a:3 title="Title 4" -metadata:s:a:4 language=swa -metadata:s:a:4 title="Title 5"

import subprocess
import os
import random
import ffmpeg

rand_name = random.randint(10,999999999)
file = "./uploads/input.mp4"
output_dir = "./uploads/generated/"
prep_command_indexing = prep_command_inps = ""
# Audio Extraction
command = os.popen("ffprobe -loglevel error -select_streams a -show_entries stream=codec_type -of default=nw=1 " + file)
no_of_streams = len((command.read()).split())
for i in range(no_of_streams):
        # current_file = f'{output_dir}audio/756419610-{str(i)}.m4a'
        # prep_command_indexing += ' -i '+current_file
        # prep_command_inps += ' -map 1 -acodec aac -strict experimental -async 1 -ar 44100 -ab 96k -f segment -segment_time 10 -segment_list_size 0 -segment_list_flags -cache -segment_format aac -segment_list '+current_file
        subprocess.call(f'ffmpeg -i {file} -map 0:a:{str(i)} {output_dir}audio/{rand_name}-{str(i)}.m4a')
        
# Generate HLS 

# hls_command = f'ffmpeg -i {file}{prep_command_indexing} -vf scale=192:144 -threads 0 -muxdelay 0 -y -map 0 -pix_fmt yuv420p -vsync 1 -async 1 -vcodec libx264 -r 29.97 -g 60 -refs 3 -f hls -hls_time 10 -hls_list_size 0 {output_dir}out.m3u8{prep_command_inps}'
# subprocess.call(hls_command)


# stream = ffmpeg.input('./uploads/input.mp4')
# split = stream.filter_multi_output('split')
# split0 = split.stream(0)
# split1 = split[2]
# split2 = split[3]
# split3 = split[4]
# ffmpeg.concat(split1,split2,split3).filter('scale', width='-1', height='478').output('./uploads/generated/out.m3u8', audio_bitrate = 180).run()
# ffmpeg.concat(split2).output('./uploads/generated/out2.m3u8', audio_bitrate = 180).run()
# ffmpeg.concat(split3).output('./uploads/generated/out3.m3u8', audio_bitrate = 180).run()