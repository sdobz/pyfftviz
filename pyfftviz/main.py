import sys
from os import path
import json
from data_source import FFTClip
from frame_source import AmplitudeClip, GlobStore
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip


def error(msg, *args, **kwargs):
    print msg.format(*args, **kwargs)
    sys.exit(1)


def main():
    if len(sys.argv) != 2:
        error("Usage {} <filename.json>", sys.argv[0])

    viz_filename = sys.argv[1]
    if not path.exists(viz_filename):
        error("File not found")

    root_path = path.dirname(viz_filename)

    with open(viz_filename) as f:
        song_data = json.loads(f.read())

        if 'song' not in song_data:
            error("\"song\" key not found in json")

        song_filename = path.join(root_path, song_data['song'])
        if not path.exists(song_filename):
            error("\"{}\" not found")

        song_clip = FFTClip(song_filename)

        glob_cache = {}

        if 'fft-clips' not in song_data:
            error("\"fft-clips\" key not found in json")
        amplitude_clips = []
        for clip_data in song_data['fft-clips']:
            assert 'x' in clip_data
            assert 'y' in clip_data
            assert 'frequency' in clip_data
            assert 'image-pattern' in clip_data
            relative_pattern = path.join(root_path, clip_data['image-pattern'])
            if 'resize-x' in clip_data:
                assert 'resize-x' in clip_data
                resize = (clip_data['resize-y'], clip_data['resize-x'])
            else:
                resize = None

            if relative_pattern in glob_cache:
                glob_store = glob_cache[relative_pattern]
            else:
                glob_store = GlobStore(relative_pattern, resize=resize)
                glob_cache[relative_pattern] = glob_store

            amplitude_clip = AmplitudeClip(
                fft_clip=song_clip,
                glob_store=glob_store,
                freq=clip_data['frequency']).set_position((clip_data['x'], clip_data['y']))

            amplitude_clips.append(amplitude_clip)

    composite = CompositeVideoClip(amplitude_clips, size=(1120, 367)).set_audio(song_clip)
    composite.write_videofile(viz_filename + '.avi', codec='h264', fps=12)
