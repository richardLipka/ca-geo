"""Encode exported animation frames (growth3d.html → Export video) into an H.264 MP4.

Uses the ffmpeg binary bundled with the `imageio-ffmpeg` package (pip install imageio-ffmpeg);
OpenCV's VideoWriter has no reliable H.264 encoder on Windows.

usage: python encode_video.py frames_dir out.mp4 [fps]
"""
import os, subprocess, sys
import imageio_ffmpeg

src, out = sys.argv[1], sys.argv[2]
fps = sys.argv[3] if len(sys.argv) > 3 else '30'
n = sum(1 for f in os.listdir(src) if f.startswith('f_') and f.endswith('.jpg'))
cmd = [imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-loglevel', 'error', '-framerate', fps, '-i', os.path.join(src, 'f_%06d.jpg'),
       '-vf', 'scale=trunc(iw/2)*2:trunc(ih/2)*2', '-c:v', 'libx264', '-preset', 'slow', '-crf', '20', '-pix_fmt', 'yuv420p',
       '-movflags', '+faststart', out]
subprocess.run(cmd, check=True)
print(out, n, 'frames', round(n / float(fps), 1), 's', round(os.path.getsize(out) / 1e6, 1), 'MB')
