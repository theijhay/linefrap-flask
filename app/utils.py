import os
import math
import numpy as np
import tifffile
import zipfile
import imageio
import cv2
from PIL import Image
from scipy.optimize import curve_fit
import plotly.graph_objects as go


def load_image_stack(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext in ['.tif', '.tiff']:
        data = tifffile.imread(file_path)
    elif ext in ['.png', '.jpg', '.jpeg']:
        img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
        data = img
    elif ext in ['.mp4', '.avi', '.mov']:
        vid = imageio.get_reader(file_path)
        frames = [cv2.cvtColor(f, cv2.COLOR_RGB2GRAY) for f in vid]
        data = np.array(frames)
    elif ext == '.gif':
        gif = Image.open(file_path)
        frames = []
        try:
            while True:
                frames.append(np.array(gif.convert('L')))
                gif.seek(gif.tell() + 1)
        except EOFError:
            pass
        data = np.array(frames)
    elif ext == '.zip':
        with zipfile.ZipFile(file_path, 'r') as z:
            files = sorted([f for f in z.namelist() if f.lower().endswith(('.png','.jpg','.jpeg'))])
            frames = [np.array(Image.open(z.open(f)).convert('L')) for f in files]
            data = np.array(frames)
    else:
        raise ValueError("Unsupported file format")

    if data.ndim == 2:
        return data[None, ...]
    return data


def extract_roi_normalize(stack, half_width=5):
    # Central horizontal ROI and mean intensities
    y = stack.shape[1] // 2
    roi = stack[:, y-half_width:y+half_width, :]
    intensities = np.array([np.mean(frame) for frame in roi])

    if len(intensities) < 4:
        raise ValueError("Upload must contain at least 4 frames.")

    # Normalize I(t)/I0 (LineFRAP convention)
    I_bleach = intensities[3]
    I_pre = intensities[:3].mean()
    norm = (intensities - I_bleach) / (I_pre - I_bleach)
    t = np.arange(norm.size)
    return norm, t


def analytical_model(t, k, K0, D, rho_e):
    # vectorized model
    TI = sum(((-K0)**j) / (math.factorial(j) * np.sqrt(1 + j)) for j in range(4))
    j = np.arange(4)[:, None]
    denom = np.sqrt((1+j)*(1 + (8*D)/(rho_e**2)*t))
    terms = ((-K0)**j) / (np.vectorize(math.factorial)(j) * denom)
    TD = terms.sum(axis=0)
    return k * TD + (1 - k) * TI


def fit_recovery_curve(norm, t):
    def fit_func(t, k, K0, D, rho_e):
        return 1 - analytical_model(t, k, K0, D, rho_e)

    popt, _ = curve_fit(fit_func, t, norm, p0=[0.8, 0.5, 10, 0.5], bounds=(0, np.inf))
    return popt


def plotly_chart_html(norm, t, popt):
    default_curve = 1 - analytical_model(t, 0.8, 0.5, 10, 0.5)
    fit = 1 - analytical_model(t, *popt)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=norm, mode='markers+lines', name='Normalized Data', marker=dict(size=6), line=dict(dash='dot')))
    fig.add_trace(go.Scatter(x=t, y=fit, mode='lines', name='Fitted Curve', line=dict(width=3)))
    fig.add_trace(go.Scatter(x=t, y=default_curve, mode='lines', name='Model Default', line=dict(dash='dash')))  
    fig.update_layout(title="LineFRAP Recovery Curve", xaxis_title="Time (frames)", yaxis_title="I(t)/I₀", template='plotly_white', height=500, width=800)
    return go.Figure(fig).to_html(include_plotlyjs='cdn', full_html=False)