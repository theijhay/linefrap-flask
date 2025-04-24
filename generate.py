from PIL import Image, ImageEnhance, ImageDraw, ImageSequence
import zipfile
import os
from pathlib import Path
import cv2
import numpy as np

def create_dummy_image(size=(200, 200), text="Demo"):
    img = Image.new("L", size, color=180)
    draw = ImageDraw.Draw(img)
    draw.text((10, 90), text, fill=0)
    return img

def generate_frap_demo():
    """
    Generates a ZIP, TIFF, MP4, and GIF file of 4 grayscale images simulating FRAP bleaching & recovery.
    Saves all outputs to the Desktop.
    """
    desktop = Path.home()
    output_dir = desktop / "frap_demo_frames"
    output_dir.mkdir(exist_ok=True)

    img = create_dummy_image()
    brightness_levels = [1.0, 0.6, 0.75, 0.9]
    frame_paths = []
    tiff_frames = []
    video_frames = []
    gif_frames = []

    for i, b in enumerate(brightness_levels):
        enhancer = ImageEnhance.Brightness(img)
        modified = enhancer.enhance(b)

        frame_path = output_dir / f"frame_{i+1}.png"
        modified.save(frame_path)
        frame_paths.append(frame_path)

        tiff_frames.append(modified)
        video_frames.append(np.array(modified))
        gif_frames.append(modified.copy())

    # ZIP
    zip_path = desktop / "frap_demo.zip"
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for path in frame_paths:
            zipf.write(path, path.name)

    # TIFF
    tiff_path = desktop / "frap_demo.tiff"
    tiff_frames[0].save(tiff_path, save_all=True, append_images=tiff_frames[1:])

    # MP4
    mp4_path = str(desktop / "frap_demo.mp4")
    height, width = video_frames[0].shape
    out = cv2.VideoWriter(mp4_path, cv2.VideoWriter_fourcc(*'mp4v'), 1, (width, height), isColor=False)
    for frame in video_frames:
        out.write(cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR))
    out.release()

    # GIF
    gif_path = desktop / "frap_demo.gif"
    gif_frames[0].save(gif_path, save_all=True, append_images=gif_frames[1:], loop=0, duration=500)

    print(f"[✓] Created files on Desktop:")
    print(f" - ZIP:  {zip_path}")
    print(f" - TIFF: {tiff_path}")
    print(f" - MP4:  {mp4_path}")
    print(f" - GIF:  {gif_path}")

if __name__ == '__main__':
    generate_frap_demo()
