# 🦴 Bone Cancer Detection System

An AI-powered web application for bone cancer detection using YOLOv8 classification, GradCAM visualization, and automated PDF report generation.

## 📋 Features

- **User Authentication**: Secure registration and login system
- **X-Ray Image Upload**: Support for PNG, JPG, and JPEG formats
- **AI-Powered Detection**: YOLOv8 classification model with ~97% validation accuracy
- **Confidence Scores**: Detailed probability scores for cancer and normal classifications
- **GradCAM Heatmaps**: Visual explanation of model decisions
- **PDF Reports**: Professional medical reports with analysis results
- **Prediction History**: Track all previous analyses
- **Responsive Design**: Modern, mobile-friendly interface

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Git (optional)

### Setup Instructions

1. **Clone or download this repository**
   ```bash
   cd bone_cancer_detection
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy the example file
   copy .env.example .env  # Windows
   # or
   cp .env.example .env    # macOS/Linux
   
   # Edit .env and set a secure SECRET_KEY
   ```

5. **Ensure the trained model is in place**
   - The fine-tuned YOLOv8 model (`best.pt`) should be in the root directory
   - Model was trained on bone cancer dataset with ~97% validation accuracy

## 🎯 Usage

1. **Start the Flask application**
   ```bash
   python app.py
   ```

2. **Access the application**
   - Open your web browser
   - Navigate to: `http://localhost:5000`

3. **Create an account**
   - Click "Register" and create your account
   - Login with your credentials

4. **Upload and analyze X-rays**
   - Click "Dashboard" to access the upload interface
   - Upload a bone X-ray image (PNG, JPG, or JPEG)
   - Wait for the AI analysis to complete
   - View results, confidence scores, and GradCAM heatmap
   - Generate and download PDF report

## 📊 System Architecture

```
bone_cancer_detection/
├── app.py                    # Main Flask application
├── config.py                 # Configuration settings
├── models.py                 # Database models
├── best.pt                   # Fine-tuned YOLOv8 model
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables
├── routes/
│   ├── auth.py              # Authentication routes
│   ├── predict.py           # Prediction routes
│   └── reports.py           # Report generation routes
├── utils/
│   ├── yolo_detector.py    # YOLO prediction logic
│   ├── gradcam.py          # GradCAM visualization
│   └── pdf_generator.py    # PDF report generation
├── templates/               # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── results.html
│   └── history.html
├── static/
│   ├── css/
│   │   └── style.css       # Styling
│   └── uploads/            # Uploaded files
│       ├── original/       # Original X-rays
│       ├── heatmaps/       # GradCAM visualizations
│       └── reports/        # Generated PDFs
└── instance/
    └── database.db         # SQLite database
```

## 🧠 Model Information

- **Architecture**: YOLOv8 Nano Classification (yolov8n-cls)
- **Training Dataset**: Bone cancer detection dataset from Roboflow
  - Training images: 7,057 (3,081 cancer + 3,976 normal)
  - Validation images: 882 (398 cancer + 484 normal)
  - Test images: 872 (384 cancer + 488 normal)
- **Validation Accuracy**: ~97%
- **Classes**: 2 (Cancer, Normal)
- **Input Size**: 224x224 pixels

## 🔬 Technology Stack

**Backend:**
- Flask (Python web framework)
- SQLAlchemy (ORM)
- Flask-SQLAlchemy (Database integration)
- Werkzeug (Password hashing)

**AI/ML:**
- Ultralytics YOLOv8 (Object detection/classification)
- PyTorch (Deep learning framework)
- OpenCV (Image processing)
- NumPy (Numerical computations)

**Visualization:**
- Matplotlib (Plotting)
- Seaborn (Statistical visualization)
- GradCAM (Model explainability)

**Report Generation:**
- ReportLab (PDF creation)

**Frontend:**
- HTML5
- CSS3 (Modern gradients, animations)
- Vanilla JavaScript

## ⚠️ Important Disclaimers

**Medical Disclaimer:**
- This system is for **research and screening purposes only**
- It should **NOT** be used as the sole basis for medical diagnosis
- Always consult qualified medical professionals for diagnosis and treatment
- False positives and false negatives are possible with any AI system
- The developers assume no liability for medical decisions based on this system

**Data Privacy:**
- Uploaded images are stored on the server
- Implement proper data encryption and access controls for production use
- Comply with HIPAA, GDPR, and other relevant regulations

## 🛠️ Development

### Running in Development Mode

```bash
# With debug mode enabled (default)
python app.py
```

### Database Management

```bash
# Database is automatically created on first run
# To reset the database, delete instance/database.db
```

## 📝 License

This project is for educational and research purposes.

## 👥 Support

For issues, questions, or contributions, please refer to the project documentation.

## 🔄 Future Enhancements

- [ ] Multi-model ensemble for improved accuracy
- [ ] DICOM format support
- [ ] Advanced analytics dashboard
- [ ] Email notifications for results
- [ ] API endpoints for integration
- [ ] Docker containerization
- [ ] Cloud deployment guide

---

**Built with ❤️ for advancing medical AI research**
