from PIL import Image, ImageDraw
import imageio.v2 as iio
import zipfile
import os
from pathlib import Path
import cv2
import numpy as np
import shutil

def generate_synthetic_frame(size=(200, 200), center_brightness=50, noise_level=20):
    """Generate a synthetic frame with noisy background and bright central region."""
    img = np.random.normal(loc=128, scale=noise_level, size=size).astype(np.uint8)
    cx, cy = size[0] // 2, size[1] // 2
    for y in range(cy - 10, cy + 10):
        for x in range(cx - 10, cx + 10):
            img[y, x] = min(255, img[y, x] + center_brightness)
    return Image.fromarray(img)

def generate_frap_demo():
    """
    Generates synthetic FRAP demo files: ZIP, TIFF, MP4, and GIF using pixel-randomized data.
    Saves all outputs to the user's Desktop.
    """
    try:
        desktop = Path.home()
        output_dir = desktop / "frap_demo_frames"

        # Clean previous folder
        if output_dir.exists():
            shutil.rmtree(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        brightness_series = [30, 50, 80, 100]  # Simulated recovery brightnesses
        frame_paths, tiff_frames, video_frames, gif_frames = [], [], [], []

        for i, brightness in enumerate(brightness_series):
            frame = generate_synthetic_frame(center_brightness=brightness)

            frame_path = output_dir / f"frame_{i+1}.png"
            frame.save(frame_path)
            frame_paths.append(frame_path)

            tiff_frames.append(frame)
            video_frames.append(np.array(frame))
            gif_frames.append(frame.copy())

        # ZIP
        zip_path = desktop / "frap_demo.zip"
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for path in frame_paths:
                zipf.write(path, path.name)

        # TIFF
        tiff_path = desktop / "frap_demo.tiff"
        tiff_frames[0].save(tiff_path, save_all=True, append_images=tiff_frames[1:])

        # MP4
        mp4_path = desktop / "frap_demo.mp4"
        with iio.get_writer(mp4_path, fps=1, codec='libx264', format='FFMPEG') as writer:
            for frame in video_frames:
                writer.append_data(frame)

        # GIF
        gif_path = desktop / "frap_demo.gif"
        gif_frames[0].save(gif_path, save_all=True, append_images=gif_frames[1:], loop=0, duration=500)

        print("[✓] Synthetic FRAP demo files created:")
        print(f" - ZIP:  {zip_path}")
        print(f" - TIFF: {tiff_path}")
        print(f" - MP4:  {mp4_path}")
        print(f" - GIF:  {gif_path}")

    except Exception as e:
        print(f"[✗] Failed to generate demo files: {e}")

if __name__ == '__main__':
    generate_frap_demo()
