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
            
            """ Display an error message if no file is selected."""
            return render_template('index.html', **results)
        
        """Check if the file is a valid image or video format."""
        header = file.read(64)
        file.seek(0)
        kind = imghdr.what(None, header)
        ext = os.path.splitext(file.filename)[1].lower()
        allowed_exts = ('.tif','.tiff','.png','.jpg','.jpeg','.gif','.mp4','.avi','.mov','.zip')
        if not kind and ext not in allowed_exts:
            flash("Unsupported file type")
            
            """ Display an error message if the file type is not supported."""
            return render_template('index.html', **results)
        
        """ Check if the file is a valid image format."""
        upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename)
        file.save(upload_path)
        
        """ Check if the file is a valid image format."""
        try:
            stack = load_image_stack(upload_path)
            intensities, t = extract_roi_normalize(stack)
            if len(t) < 6:
                flash("⚠️ Consider using more than 6 frames for a better fit.", "warning")
            
            """ Fit the recovery curve using the provided data."""    
            popt, fitted, r2 = fit_recovery_curve(intensities, t)
            chart_html = plotly_chart_html(intensities, t, popt, r_squared=r2)
            k, K0, D, rho_e = popt
            results = {
                'k': f"{k:.3f}", 'K0': f"{K0:.3f}", 'D': f"{D:.2f}", 'rho_e': f"{rho_e:.2f}",
                'summary': (
                    f"<b>Mobile fraction (k):</b> {k:.3f}<br>"
                    f"<b>Bleach strength (K₀):</b> {K0:.3f}<br>"
                    f"<b>Diffusion coefficient (D):</b> {D:.2f}<br>"
                    f"<b>Effective radius (ρₑ):</b> {rho_e:.2f}<br>"
                    f"<b>Fit Quality (R²):</b> {r2:.4f}"),
                'chart': chart_html
            }
            
            """ Display the fitted curve and the original data."""
        except Exception as e:
            flash(f"Error processing file: {e}")
            
        """ Handle any exceptions that occur during file processing."""
        return render_template('index.html', **results)
    
    """ If the request method is GET, render the index page."""
    return render_template('index.html', **results)
