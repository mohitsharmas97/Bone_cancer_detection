from flask import Blueprint, send_file, flash, redirect, url_for, session, current_app, make_response
from models import db, Prediction, User
from routes.auth import login_required
from utils.pdf_generator import generate_pdf_report
import os
from datetime import datetime

reports_bp = Blueprint('reports', __name__)


def send_pdf_file(file_path, filename):
    """Send PDF file with proper headers for browser download"""
    with open(file_path, 'rb') as f:
        pdf_data = f.read()
    
    response = make_response(pdf_data)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
    response.headers['Content-Length'] = len(pdf_data)
    return response


@reports_bp.route('/generate/<int:prediction_id>')
@login_required
def generate(prediction_id):
    """Generate PDF report for a prediction"""
    prediction = Prediction.query.get_or_404(prediction_id)
    
    # Verify user owns this prediction
    if prediction.user_id != session['user_id']:
        flash('Unauthorized access', 'error')
        return redirect(url_for('predict.dashboard'))
    
    try:
        # Check if report already exists
        if prediction.report_path and os.path.exists(prediction.report_path):
            return send_pdf_file(
                prediction.report_path,
                f"bone_cancer_report_{prediction.id}.pdf"
            )
        
        # Generate new report
        user = User.query.get(session['user_id'])
        
        report_filename = f"report_{session['user_id']}_{prediction.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        report_path = os.path.join(current_app.config['REPORTS_FOLDER'], report_filename)
        
        # Prepare data for report
        user_info = {
            'username': user.username,
            'email': user.email
        }
        
        prediction_data = {
            'prediction_class': prediction.prediction_class,
            'confidence_cancer': prediction.confidence_cancer,
            'confidence_normal': prediction.confidence_normal
        }
        
        image_paths = {
            'original': prediction.original_image_path,
            'heatmap': prediction.heatmap_image_path
        }
        
        # Generate PDF
        generate_pdf_report(report_path, user_info, prediction_data, image_paths)
        
        # Update database
        prediction.report_path = report_path
        db.session.commit()
        
        flash('PDF report generated successfully!', 'success')
        return send_pdf_file(
            report_path,
            f"bone_cancer_report_{prediction.id}.pdf"
        )
        
    except Exception as e:
        flash(f'Error generating report: {str(e)}', 'error')
        return redirect(url_for('predict.results', prediction_id=prediction_id))


@reports_bp.route('/download/<int:prediction_id>')
@login_required
def download(prediction_id):
    """Download existing PDF report"""
    prediction = Prediction.query.get_or_404(prediction_id)
    
    # Verify user owns this prediction
    if prediction.user_id != session['user_id']:
        flash('Unauthorized access', 'error')
        return redirect(url_for('predict.dashboard'))
    
    if not prediction.report_path or not os.path.exists(prediction.report_path):
        flash('Report not found. Please generate it first.', 'error')
        return redirect(url_for('predict.results', prediction_id=prediction_id))
    
    return send_pdf_file(
        prediction.report_path,
        f"bone_cancer_report_{prediction.id}.pdf"
    )
