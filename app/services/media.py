from __future__ import annotations

from pathlib import Path
import subprocess
import tempfile
import textwrap

from PIL import Image, ImageDraw, ImageFont


FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
]


def _font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in FONT_CANDIDATES:
        if Path(path).exists():
            return ImageFont.truetype(path, size=size)
    return ImageFont.load_default()


def render_quote_card(text: str, output_path: str, brand: str = "Metaphor") -> str:
    width, height = 1080, 1350
    image = Image.new("RGB", (width, height), (23, 24, 31))
    draw = ImageDraw.Draw(image)
    title_font = _font(46)
    body_font = _font(54)
    small_font = _font(30)

    draw.rounded_rectangle((70, 70, width - 70, height - 70), radius=42, outline=(218, 184, 106), width=4)
    draw.text((110, 115), brand, font=title_font, fill=(218, 184, 106))

    wrapped = textwrap.wrap(text, width=29)
    y = 300
    for line in wrapped[:12]:
        draw.text((110, y), line, font=body_font, fill=(245, 245, 242))
        y += 76
    draw.text((110, height - 150), "Слова, которые можно отправить", font=small_font, fill=(180, 180, 184))

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, "PNG")
    return str(path)


def render_story_card(text: str, output_path: str, brand: str = "Metaphor") -> str:
    width, height = 1080, 1920
    image = Image.new("RGB", (width, height), (18, 19, 25))
    draw = ImageDraw.Draw(image)
    title_font = _font(52)
    body_font = _font(66)
    small_font = _font(34)
    draw.rounded_rectangle((64, 64, width - 64, height - 64), radius=46, outline=(218, 184, 106), width=5)
    draw.text((110, 120), brand, font=title_font, fill=(218, 184, 106))
    wrapped = textwrap.wrap(text, width=24)
    total = min(len(wrapped), 13) * 88
    y = max(340, (height - total) // 2)
    for line in wrapped[:13]:
        draw.text((110, y), line, font=body_font, fill=(245, 245, 242))
        y += 88
    draw.text((110, height - 165), "metaphor.uz", font=small_font, fill=(180, 180, 184))
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, "PNG")
    return str(path)


def _media_duration(path: str) -> float:
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", path],
            check=True,
            capture_output=True,
            text=True,
        )
        return max(0.0, float(result.stdout.strip()))
    except Exception:
        return 0.0


def render_vertical_video(
    text: str,
    output_path: str,
    duration: int = 9,
    audio_path: str | None = None,
) -> str:
    """Render a simple 9:16 branded MP4; optionally attach generated narration."""
    target = Path(output_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        frame = Path(tmp) / "frame.png"
        render_story_card(text, str(frame))
        audio_duration = _media_duration(audio_path) if audio_path else 0.0
        actual_duration = max(float(duration), audio_duration + 0.5)
        frames = int(actual_duration * 25)
        video_filter = (
            f"zoompan=z='min(zoom+0.0007,1.08)':d={frames}:s=1080x1920,"
            f"fade=t=in:st=0:d=0.5,fade=t=out:st={max(actual_duration-0.6,0)}:d=0.6,format=yuv420p"
        )
        command = ["ffmpeg", "-y", "-loop", "1", "-i", str(frame)]
        if audio_path:
            command += ["-i", audio_path, "-vf", video_filter, "-map", "0:v:0", "-map", "1:a:0", "-shortest"]
        else:
            command += ["-vf", video_filter, "-an"]
        command += [
            "-t", str(actual_duration),
            "-r", "25",
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-movflags", "+faststart",
        ]
        if audio_path:
            command += ["-c:a", "aac", "-b:a", "128k"]
        command += [str(target)]
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return str(target)
