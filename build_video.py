"""Render a local original vertical draft with Windows SAPI and FFmpeg.

No upload, scraping, remote speech service, API keys or package installation.
"""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import textwrap
import wave


def validate(data):
    if not isinstance(data, dict) or data.get("version") != 1:
        raise ValueError("Need a version 1 script")
    scenes = data.get("scenes")
    if not isinstance(scenes, list) or not 1 <= len(scenes) <= 12:
        raise ValueError("Need 1 to 12 scenes")
    result = []
    for scene in scenes:
        if not isinstance(scene, dict):
            raise ValueError("Invalid scene")
        clean = {}
        for field, limit in [("heading", 70), ("caption", 140), ("narration", 700)]:
            value = scene.get(field)
            if not isinstance(value, str) or not 1 <= len(value.strip()) <= limit:
                raise ValueError("Invalid scene field: " + field)
            if any(ord(c) < 32 and c not in "\n\t" for c in value):
                raise ValueError("Unsupported control character")
            clean[field] = value.strip()
        result.append(clean)
    return result


def command(args, cwd):
    subprocess.run(args, cwd=cwd, check=True, stdout=subprocess.DEVNULL)


def build(script, output):
    scenes = validate(json.loads(script.read_text(encoding="utf-8")))
    ffmpeg, ffprobe = shutil.which("ffmpeg"), shutil.which("ffprobe")
    shell = shutil.which("powershell.exe")
    font = Path("C:/Windows/Fonts/arial.ttf")
    if not all([ffmpeg, ffprobe, shell, font.exists()]):
        raise RuntimeError("Need Windows SAPI, powershell.exe, FFmpeg, ffprobe and Arial")
    output.mkdir(parents=True, exist_ok=False)
    shutil.copyfile(font, output / "font.ttf")
    speech = Path(__file__).with_name("speak.ps1").resolve()
    durations = []
    for i, scene in enumerate(scenes):
        prefix = f"scene-{i:02d}"
        (output / (prefix+"-speech.txt")).write_text(scene["narration"], encoding="utf-8-sig")
        (output / "heading.txt").write_text(textwrap.fill(scene["heading"], 22), encoding="utf-8")
        (output / "caption.txt").write_text(textwrap.fill(scene["caption"], 28), encoding="utf-8")
        command([shell, "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass", "-File", str(speech),
                 "-TextPath", str(output / (prefix+"-speech.txt")),
                 "-OutputPath", str(output / (prefix+".wav"))], output)
        with wave.open(str(output / (prefix+".wav")), "rb") as audio:
            duration = audio.getnframes() / audio.getframerate() + .5
        if duration > 35:
            raise ValueError("Scene too long; shorten narration")
        durations.append(duration)
        filters = ("drawbox=x=45:y=100:w=630:h=12:color=0xB7F571:t=fill,"
                   "drawtext=fontfile=font.ttf:text='TECHNIK IN 30 SEKUNDEN':fontsize=23:fontcolor=0xB7F571:x=45:y=150,"
                   "drawtext=fontfile=font.ttf:textfile=heading.txt:expansion=none:fontsize=48:fontcolor=white:x=45:y=290:line_spacing=15,"
                   "drawbox=x=45:y=660:w=630:h=330:color=0x24304A:t=fill,"
                   "drawtext=fontfile=font.ttf:textfile=caption.txt:expansion=none:fontsize=34:fontcolor=0xD4DEEF:x=65:y=700:line_spacing=14,"
                   f"drawbox=x=45:y=1040:w=630:h=6:color=0x33455C:t=fill,drawbox=x=45:y=1040:w={630*(i+1)/len(scenes):.0f}:h=6:color=0xB7F571:t=fill,"
                   "drawtext=fontfile=font.ttf:text='LOKALER ENTWURF / SYNTHETISCHE STIMME':fontsize=19:fontcolor=0x99AAC2:x=45:y=1140")
        command([ffmpeg, "-hide_banner", "-loglevel", "error", "-n", "-f", "lavfi", "-i",
                 "color=c=0x101928:s=720x1280:r=30", "-i", prefix+".wav", "-vf", filters,
                 "-af", "apad", "-t", str(duration), "-c:v", "libx264", "-preset", "fast",
                 "-crf", "22", "-pix_fmt", "yuv420p", "-c:a", "aac", "-ar", "48000",
                 "-ac", "2", prefix+".mp4"], output)
    (output / "concat.txt").write_text("".join(f"file 'scene-{i:02d}.mp4'\n" for i in range(len(scenes))), encoding="ascii")
    command([ffmpeg, "-hide_banner", "-loglevel", "error", "-n", "-f", "concat", "-safe", "1", "-i", "concat.txt",
             "-c", "copy", "-movflags", "+faststart", "draft-short.mp4"], output)
    probe = subprocess.run([ffprobe, "-v", "error", "-show_streams", "-show_format", "-of", "json",
                            str(output / "draft-short.mp4")], capture_output=True, text=True, check=True)
    metadata = json.loads(probe.stdout)
    video = next(s for s in metadata["streams"] if s["codec_type"] == "video")
    if (video["width"], video["height"]) != (720, 1280):
        raise RuntimeError("Unexpected output resolution")
    manifest = {"status": "local-unpublished-draft", "width": 720, "height": 1280,
                "durationSeconds": float(metadata["format"]["duration"]),
                "sceneDurations": durations, "voice": "Windows SAPI, first installed German voice",
                "uploaded": False, "factsAndListeningReviewRequired": True}
    (output / "verification.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    # Do not include the system font in deliverables.
    (output / "font.ttf").unlink()
    print(json.dumps(manifest))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("script", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    build(args.script.resolve(), args.output.resolve())
