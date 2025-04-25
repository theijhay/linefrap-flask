from PIL import Image
import zipfile
from pathlib import Path
import numpy as np
import imageio.v2 as iio
import shutil

def generate_synthetic_frame(size=(208, 208), center_brightness=50, noise_level=20):
    """
    Generate a synthetic frame with Gaussian spot in center to simulate FRAP recovery.
    """
    img = np.random.normal(loc=128, scale=noise_level, size=size).astype(np.float32)
    cx, cy = size[0] // 2, size[1] // 2
    xv, yv = np.meshgrid(np.arange(size[1]), np.arange(size[0]))

    # Gaussian spot centered with decaying intensity
    sigma = 12
    gaussian = center_brightness * np.exp(-((xv - cx)**2 + (yv - cy)**2) / (2.0 * sigma**2))
    img += gaussian
    img = np.clip(img, 0, 255).astype(np.uint8)
    return Image.fromarray(img)

def generate_frap_demo():
    """
    Generates advanced synthetic FRAP demo files: ZIP, TIFF, MP4, and GIF using Gaussian ROI + time-series.
    Saves all outputs to the user's Desktop.
    """
    try:
        desktop = Path.home()
        output_dir = desktop / "frap_demo_frames"

        if output_dir.exists():
            shutil.rmtree(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        brightness_series = np.linspace(20, 150, 10)  # simulate real FRAP recovery
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

        # MP4 using imageio (ensures proper metadata)
        mp4_path = desktop / "frap_demo.mp4"
        with iio.get_writer(mp4_path, fps=2, codec='libx264', format='FFMPEG') as writer:
            for frame in video_frames:
                writer.append_data(frame)

        # GIF
        gif_path = desktop / "frap_demo.gif"
        gif_frames[0].save(gif_path, save_all=True, append_images=gif_frames[1:], loop=0, duration=300)

        print("[✓] Advanced synthetic FRAP demo files created:")
        print(f" - ZIP:  {zip_path}")
        print(f" - TIFF: {tiff_path}")
        print(f" - MP4:  {mp4_path}")
        print(f" - GIF:  {gif_path}")

    except Exception as e:
        print(f"[✗] Failed to generate demo files: {e}")

if __name__ == '__main__':
    generate_frap_demo()
