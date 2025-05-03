import imghdr
import os
import numpy as np
from flask import Blueprint, render_template, request, flash, current_app
from .utils import load_image_stack, extract_roi_normalize, fit_recovery_curve, plotly_chart_html

main_bp = Blueprint('main', __name__)

""" This module defines the main routes for the Flask application."""
@main_bp.route('/', methods=['GET', 'POST'])
def index():
    results = {}
    if request.method == 'POST':
        file = request.files.get('file')
        if not file or file.filename == '':
            flash("No file selected")
            return render_template('index.html', **results)

        header = file.read(64)
        file.seek(0)
        kind = imghdr.what(None, header)
        ext = os.path.splitext(file.filename)[1].lower()
        allowed_exts = ('.tif','.tiff','.png','.jpg','.jpeg','.gif','.mp4','.avi','.mov','.zip')
        if not kind and ext not in allowed_exts:
            flash("Unsupported file type")
            return render_template('index.html', **results)

        upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename)
        file.save(upload_path)

        try:
            stack = load_image_stack(upload_path)
            if stack.ndim < 3 or stack.shape[0] <= 1:
                flash("⚠️ Only one frame was detected. A proper FRAP analysis requires multiple time-lapse frames. "
                "Please check that you've uploaded the correct time-series file.")
                
            intensities, t = extract_roi_normalize(stack)
            popt, fitted, r2 = fit_recovery_curve(intensities, t)
            chart_html = plotly_chart_html(intensities, t, popt)

            k, K0, D, rho_e = popt
            results = {
                'k': f"{k:.3f}", 'K0': f"{K0:.3f}", 'D': f"{D:.2f}", 'rho_e': f"{rho_e:.2f}",
                'summary': (
                    f"<b>Mobile fraction (k):</b> {k:.3f}<br>"
                    f"<b>Bleach strength (K₀):</b> {K0:.3f}<br>"
                    f"<b>Diffusion coefficient (D):</b> {D:.2f}<br>"
                    f"<b>Effective radius (ρₑ):</b> {rho_e:.2f}")
                ,
                'chart': chart_html
            }
        except Exception as e:
            flash(f"Error processing file: {e}")
        return render_template('index.html', **results)

    return render_template('index.html', **results)
