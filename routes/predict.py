from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from models import db, User, Prediction
from routes.auth import login_required
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from utils.yolo_detector import BoneCancerDetector
from utils.gradcam import generate_gradcam_heatmap

predict_bp = Blueprint('predict', __name__)


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


@predict_bp.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard for file upload"""
    return render_template('dashboard.html')


@predict_bp.route('/upload', methods=['POST'])
@login_required
def upload():
    """Handle file upload and prediction"""
    if 'file' not in request.files:
        flash('No file uploaded', 'error')
        return redirect(url_for('predict.dashboard'))
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('predict.dashboard'))
    
    if not allowed_file(file.filename):
        flash('Invalid file type. Please upload PNG, JPG, or JPEG images.', 'error')
        return redirect(url_for('predict.dashboard'))
    
    try:
        # Save original image
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{session['user_id']}_{timestamp}_{filename}"
        
        original_path = os.path.join(current_app.config['ORIGINAL_FOLDER'], unique_filename)
        file.save(original_path)
        
        # Run prediction
        detector = BoneCancerDetector(current_app.config['MODEL_PATH'])
        results = detector.predict(original_path)
        
        # Generate GradCAM heatmap
        heatmap_filename = f"heatmap_{unique_filename}"
        heatmap_path = os.path.join(current_app.config['HEATMAP_FOLDER'], heatmap_filename)
        
        # Target class: 0 for cancer, None for predicted class
        target_class = 0 if results['prediction_class'] == 'cancer' else 1
        generate_gradcam_heatmap(
            current_app.config['MODEL_PATH'],
            original_path,
            heatmap_path,
            target_class=None  # Use predicted class
        )
        
        # Save to database
        prediction = Prediction(
            user_id=session['user_id'],
            original_image_path=original_path,
            heatmap_image_path=heatmap_path,
            prediction_class=results['prediction_class'],
            confidence_cancer=results['confidence_cancer'],
            confidence_normal=results['confidence_normal']
        )
        
        db.session.add(prediction)
        db.session.commit()
        
        # Store prediction ID in session for results page
        session['last_prediction_id'] = prediction.id
        
        flash('Analysis complete!', 'success')
        return redirect(url_for('predict.results', prediction_id=prediction.id))
        
    except Exception as e:
        flash(f'Error processing image: {str(e)}', 'error')
        return redirect(url_for('predict.dashboard'))


@predict_bp.route('/results/<int:prediction_id>')
@login_required
def results(prediction_id):
    """Display prediction results"""
    prediction = Prediction.query.get_or_404(prediction_id)
    
    # Verify user owns this prediction
    if prediction.user_id != session['user_id']:
        flash('Unauthorized access', 'error')
        return redirect(url_for('predict.dashboard'))
    
    # Get relative paths for templates
    original_rel = os.path.join('uploads', 'original', os.path.basename(prediction.original_image_path))
    heatmap_rel = os.path.join('uploads', 'heatmaps', os.path.basename(prediction.heatmap_image_path))
    
    return render_template('results.html', 
                         prediction=prediction,
                         original_image=original_rel,
                         heatmap_image=heatmap_rel)


@predict_bp.route('/history')
@login_required
def history():
    """View prediction history"""
    predictions = Prediction.query.filter_by(user_id=session['user_id'])\
                                  .order_by(Prediction.created_at.desc())\
                                  .all()
    
    return render_template('history.html', predictions=predictions)
