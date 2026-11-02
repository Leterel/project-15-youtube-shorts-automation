"""Render a local original vertical draft with Windows SAPI and FFmpeg.

No upload, scraping, remote speech service, API keys or package installation.
"""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import math
import unicodedata
import wave
import hashlib
import html


def webvtt(scenes, durations):
    """Scene-level narration cues; explicitly not word-aligned subtitles."""
    if len(scenes) != len(durations) or not scenes:
        raise ValueError("Need matching scenes and durations")
    def timestamp(milliseconds):
        hours, rest = divmod(milliseconds, 3_600_000)
        minutes, rest = divmod(rest, 60_000)
        seconds, millis = divmod(rest, 1000)
        return f"{hours:02}:{minutes:02}:{seconds:02}.{millis:03}"
    lines = ["WEBVTT", "", "NOTE Scene-level narration; timing is not word aligned.", ""]
    elapsed = 0.0
    for index, (scene, duration) in enumerate(zip(scenes, durations), 1):
        if type(duration) not in (int, float) or not math.isfinite(duration) or duration < 0.001 or duration > 35:
            raise ValueError("Invalid cue duration")
        start = round(elapsed * 1000)
        elapsed += duration
        end = round(elapsed * 1000)
        lines.extend([str(index), f"{timestamp(start)} --> {timestamp(end)}",
                      html.escape(" ".join(scene["narration"].split()), quote=False), ""])
    return "\n".join(lines)


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


def text_units(text):
    return sum(0 if unicodedata.combining(c) else
               2 if unicodedata.east_asian_width(c) in ("W", "F") else 1 for c in text)


def fit_text(text, width, height, maximum, minimum):
    """Conservative em-sized glyph budget, with explicit line/height limits."""
    normalized = " ".join(text.split())
    for size in range(maximum, minimum-1, -1):
        limit = width // size
        lines, line = [], ""
        for word in normalized.split(" "):
            if line and text_units(line + " " + word) <= limit:
                line += " " + word
                continue
            if line:
                lines.append(line)
                line = ""
            for char in word:
                if line and text_units(line + char) > limit:
                    lines.append(line)
                    line = ""
                line += char
        if line:
            lines.append(line)
        if (lines and all(text_units(line)*size <= width for line in lines)
                and len(lines) * (math.ceil(size*1.5) + 8) <= height):
            return {"text": "\n".join(lines), "fontSize": size, "lines": len(lines)}
    raise ValueError("Text does not fit; shorten it before rendering")


def build(script, output):
    scenes = validate(json.loads(script.read_text(encoding="utf-8")))
    layouts = [{"heading": fit_text(s["heading"], 630, 330, 48, 28),
                "caption": fit_text(s["caption"], 590, 260, 34, 22)} for s in scenes]
    ffmpeg, ffprobe = shutil.which("ffmpeg"), shutil.which("ffprobe")
    shell = shutil.which("powershell.exe")
    font = Path("C:/Windows/Fonts/arial.ttf")
    if not all([ffmpeg, ffprobe, shell, font.exists()]):
        raise RuntimeError("Need Windows SAPI, powershell.exe, FFmpeg, ffprobe and Arial")
    output.mkdir(parents=True, exist_ok=False)
    font_filter = "fontfile='" + font.as_posix().replace(":", "\\:") + "'"
    speech = Path(__file__).with_name("speak.ps1").resolve()
    durations = []
    for i, scene in enumerate(scenes):
        prefix = f"scene-{i:02d}"
        (output / (prefix+"-speech.txt")).write_text(scene["narration"], encoding="utf-8-sig")
        layout = layouts[i]
        (output / (prefix+"-heading.txt")).write_text(layout["heading"]["text"], encoding="utf-8", newline="\n")
        (output / (prefix+"-caption.txt")).write_text(layout["caption"]["text"], encoding="utf-8", newline="\n")
        command([shell, "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass", "-File", str(speech),
                 "-TextPath", str(output / (prefix+"-speech.txt")),
                 "-OutputPath", str(output / (prefix+".wav"))], output)
        with wave.open(str(output / (prefix+".wav")), "rb") as audio:
            duration = audio.getnframes() / audio.getframerate() + .5
        if duration > 35:
            raise ValueError("Scene too long; shorten narration")
        durations.append(duration)
        filters = ("drawbox=x=45:y=100:w=630:h=12:color=0xB7F571:t=fill,"
                   f"drawtext={font_filter}:text='TECHNIK KURZ ERKLAERT':fontsize=23:fontcolor=0xB7F571:x=45:y=150,"
                   f"drawtext={font_filter}:textfile={prefix}-heading.txt:expansion=none:fontsize={layout['heading']['fontSize']}:fontcolor=white:x=45:y=290:line_spacing=8,"
                   "drawbox=x=45:y=660:w=630:h=330:color=0x24304A:t=fill,"
                   f"drawtext={font_filter}:textfile={prefix}-caption.txt:expansion=none:fontsize={layout['caption']['fontSize']}:fontcolor=0xD4DEEF:x=65:y=700:line_spacing=8,"
                   f"drawbox=x=45:y=1040:w=630:h=6:color=0x33455C:t=fill,drawbox=x=45:y=1040:w={630*(i+1)/len(scenes):.0f}:h=6:color=0xB7F571:t=fill,"
                   f"drawtext={font_filter}:text='LOKALER ENTWURF / SYNTHETISCHE STIMME':fontsize=19:fontcolor=0x99AAC2:x=45:y=1140")
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
    audio_streams = [s for s in metadata["streams"] if s["codec_type"] == "audio"]
    if len(audio_streams) != 1 or audio_streams[0]["codec_name"] != "aac" or int(audio_streams[0]["sample_rate"]) != 48000 or audio_streams[0]["channels"] != 2:
        raise RuntimeError("Unexpected audio format")
    if abs(float(metadata["format"]["duration"])-sum(durations)) > 0.2:
        raise RuntimeError("Output duration differs from the scene timeline")
    (output / "narration.vtt").write_text(webvtt(scenes, durations), encoding="utf-8", newline="\n")
    manifest = {"status": "local-unpublished-draft", "width": 720, "height": 1280,
                "durationSeconds": float(metadata["format"]["duration"]),
                "sceneDurations": durations, "voice": "Windows SAPI, first installed German voice",
                "uploaded": False, "factsAndListeningReviewRequired": True, "textLayouts": layouts,
                "scriptSha256": hashlib.sha256(script.read_bytes()).hexdigest(),
                "videoSha256": hashlib.sha256((output / "draft-short.mp4").read_bytes()).hexdigest(),
                "subtitles": {"file": "narration.vtt", "alignment": "scene-level, not word-aligned"},
                "audio": {"codec": "aac", "sampleRate": 48000, "channels": 2}}
    (output / "verification.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("script", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    build(args.script.resolve(), args.output.resolve())
