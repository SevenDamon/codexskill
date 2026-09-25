"""Convert a browser recording from a holographic card project to shareable MP4."""

import argparse
from pathlib import Path
import shutil
import subprocess


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', required=True, type=Path)
    parser.add_argument('--webm', type=Path, help='Recording path; defaults to renders/holo-motion.webm')
    parser.add_argument('--output', type=Path, help='MP4 path; defaults to share-video.mp4')
    parser.add_argument('--ffmpeg', help='Path to ffmpeg executable if it is not on PATH')
    args = parser.parse_args()

    project = args.project.resolve()
    if not (project / 'web' / 'card-config.json').is_file():
        parser.error(f'No built card web viewer found in {project}')
    source = args.webm or project / 'renders' / 'holo-motion.webm'
    output = args.output or project / 'share-video.mp4'
    if not source.is_absolute():
        source = project / source
    if not output.is_absolute():
        output = project / output
    if not source.is_file() or source.stat().st_size == 0:
        parser.error(f'No recording found at {source}; open web/capture.html and record first')
    ffmpeg = args.ffmpeg or shutil.which('ffmpeg')
    if not ffmpeg or not Path(ffmpeg).is_file():
        parser.error('ffmpeg was not found; install it or pass --ffmpeg <executable>')

    output.parent.mkdir(parents=True, exist_ok=True)
    command = [
        str(ffmpeg), '-y', '-v', 'error', '-i', str(source),
        '-vf', 'scale=720:1080:force_original_aspect_ratio=decrease:in_range=full:out_range=limited,'
               'pad=720:1080:(ow-iw)/2:(oh-ih)/2:color=white,format=yuv420p',
        '-c:v', 'libx264', '-preset', 'medium', '-crf', '19',
        '-movflags', '+faststart', '-an', str(output),
    ]
    subprocess.run(command, check=True)
    if not output.is_file() or output.stat().st_size == 0:
        raise RuntimeError(f'ffmpeg returned without creating {output}')
    print(f'MP4: {output} ({output.stat().st_size / 1024 / 1024:.1f} MB)')


if __name__ == '__main__':
    main()
