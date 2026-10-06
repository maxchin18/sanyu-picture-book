set -e
rm -rf 1080 720 master.m3u8; mkdir -p 1080 720
ffmpeg -y -loglevel error -i ../../final.mp4 \
 -filter_complex "[0:v]split=2[a][b];[b]scale=1280:720:flags=lanczos[b2]" \
 -map "[a]" -map "[b2]" -map 0:a -map 0:a \
 -c:v libx264 -preset slow -profile:v high -pix_fmt yuv420p -r 24 -g 48 -keyint_min 48 -sc_threshold 0 \
 -b:v:0 4800k -maxrate:v:0 6500k -bufsize:v:0 9000k \
 -b:v:1 2200k -maxrate:v:1 3000k -bufsize:v:1 4400k \
 -c:a aac -b:a 128k -ar 48000 \
 -f hls -hls_time 6 -hls_playlist_type vod -hls_flags independent_segments \
 -hls_segment_filename "%v/seg_%03d.ts" \
 -master_pl_name master.m3u8 -var_stream_map "v:0,a:0,name:1080 v:1,a:1,name:720" "%v/index.m3u8"
echo ENC-DONE
