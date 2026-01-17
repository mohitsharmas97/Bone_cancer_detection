from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import os


class BoneCancerReportGenerator:
    """Generate PDF reports for bone cancer detection results"""
    
    def __init__(self, output_path):
        """Initialize PDF generator"""
        self.output_path = output_path
        self.doc = SimpleDocTemplate(output_path, pagesize=letter)
        self.styles = getSampleStyleSheet()
        self.story = []
        
        # Custom styles
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1e3a8a'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#1e40af'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        )
        
        self.normal_style = ParagraphStyle(
            'CustomNormal',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=8,
            fontName='Helvetica'
        )
    
    def generate_report(self, user_info, prediction_data, image_paths):
        """
        Generate complete PDF report
        
        Args:
            user_info: Dict with user information
            prediction_data: Dict with prediction results
            image_paths: Dict with paths to original and heatmap images
        """
        # Title
        title = Paragraph("Bone Cancer Detection Report", self.title_style)
        self.story.append(title)
        self.story.append(Spacer(1, 0.3 * inch))
        
        # Report Information
        self._add_report_info(user_info)
        self.story.append(Spacer(1, 0.3 * inch))
        
        # Prediction Results
        self._add_prediction_results(prediction_data)
        self.story.append(Spacer(1, 0.3 * inch))
        
        # Images
        self._add_images(image_paths)
        self.story.append(Spacer(1, 0.3 * inch))
        
        # Analysis Summary
        self._add_analysis_summary(prediction_data)
        self.story.append(Spacer(1, 0.3 * inch))
        
        # Disclaimer
        self._add_disclaimer()
        
        # Build PDF
        self.doc.build(self.story)
        return self.output_path
    
    def _add_report_info(self, user_info):
        """Add report metadata"""
        heading = Paragraph("Report Information", self.heading_style)
        self.story.append(heading)
        
        data = [
            ['Report Date:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
            ['Patient ID:', user_info.get('username', 'N/A')],
            ['Report ID:', f"BCR-{datetime.now().strftime('%Y%m%d%H%M%S')}"]
        ]
        
        table = Table(data, colWidths=[2 * inch, 4 * inch])
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#4b5563')),
            ('TEXTCOLOR', (1, 0), (1, -1), colors.black),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        self.story.append(table)
    
    def _add_prediction_results(self, prediction_data):
        """Add prediction results table"""
        heading = Paragraph("Detection Results", self.heading_style)
        self.story.append(heading)
        
        # Determine result color
        pred_class = prediction_data['prediction_class'].upper()
        if pred_class == 'CANCER':
            result_color = colors.HexColor('#dc2626')
            status = '⚠ CANCER DETECTED'
        else:
            result_color = colors.HexColor('#16a34a')
            status = '✓ NORMAL'
        
        data = [
            ['Classification:', Paragraph(f"<b><font color='{result_color.hexval()}'>{status}</font></b>", self.normal_style)],
            ['Cancer Confidence:', f"{prediction_data['confidence_cancer']:.2%}"],
            ['Normal Confidence:', f"{prediction_data['confidence_normal']:.2%}"],
            ['Model Accuracy:', '~97% (based on validation)']
        ]
        
        table = Table(data, colWidths=[2.5 * inch, 3.5 * inch])
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#4b5563')),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f3f4f6')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#d1d5db'))
        ]))
        
        self.story.append(table)
    
    def _add_images(self, image_paths):
        """Add original and heatmap images"""
        heading = Paragraph("Visual Analysis", self.heading_style)
        self.story.append(heading)
        
        images_data = []
        labels = []
        
        # Original image
        if os.path.exists(image_paths['original']):
            img = RLImage(image_paths['original'], width=2.5 * inch, height=2.5 * inch)
            images_data.append(img)
            labels.append(Paragraph("<b>Original X-ray</b>", self.normal_style))
        
        # Heatmap
        if os.path.exists(image_paths['heatmap']):
            heatmap = RLImage(image_paths['heatmap'], width=2.5 * inch, height=2.5 * inch)
            images_data.append(heatmap)
            labels.append(Paragraph("<b>GradCAM Heatmap</b>", self.normal_style))
        
        if images_data:
            # Create table with images
            table_data = [images_data, labels]
            table = Table(table_data, colWidths=[3 * inch] * len(images_data))
            table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ]))
            
            self.story.append(table)
    
    def _add_analysis_summary(self, prediction_data):
        """Add analysis summary"""
        heading = Paragraph("Analysis Summary", self.heading_style)
        self.story.append(heading)
        
        pred_class = prediction_data['prediction_class']
        confidence = prediction_data['confidence_cancer'] if pred_class == 'cancer' else prediction_data['confidence_normal']
        
        if pred_class == 'cancer':
            summary_text = f"""
            The AI model has detected <b>abnormal patterns</b> in the X-ray image that are 
            consistent with bone cancer. The model confidence is <b>{confidence:.2%}</b>.
            <br/><br/>
            The GradCAM heatmap highlights the regions of the image that most influenced this 
            classification. Red/yellow areas indicate regions of high importance for the cancer detection.
            <br/><br/>
            <b><font color='#dc2626'>⚠ Important:</font></b> This is a preliminary screening result. 
            Immediate consultation with a qualified radiologist or oncologist is strongly recommended 
            for confirmation and treatment planning.
            """
        else:
            summary_text = f"""
            The AI model has classified the X-ray as <b>normal</b> with a confidence of <b>{confidence:.2%}</b>.
            No significant abnormalities consistent with bone cancer were detected.
            <br/><br/>
            The GradCAM heatmap shows the regions that influenced this normal classification.
            <br/><br/>
            <b>Note:</b> While this result is encouraging, it should not replace professional medical 
            evaluation. Regular check-ups and consultations with healthcare providers are recommended.
            """
        
        summary = Paragraph(summary_text, self.normal_style)
        self.story.append(summary)
    
    def _add_disclaimer(self):
        """Add medical disclaimer"""
        heading = Paragraph("Medical Disclaimer", self.heading_style)
        self.story.append(heading)
        
        disclaimer_text = """
        <b>IMPORTANT MEDICAL DISCLAIMER:</b><br/><br/>
        This report is generated by an artificial intelligence system for preliminary screening purposes only. 
        The AI model, while trained on medical imaging data, is NOT a substitute for professional medical diagnosis.
        <br/><br/>
        <b>Key Points:</b><br/>
        • This analysis should NOT be used as the sole basis for medical decisions<br/>
        • False positives and false negatives are possible with any AI system<br/>
        • Always consult qualified medical professionals for diagnosis and treatment<br/>
        • This system is intended as a decision support tool for healthcare providers<br/>
        • The developers assume no liability for medical decisions based on this report<br/><br/>
        <b>For medical emergencies, contact your healthcare provider or emergency services immediately.</b>
        """
        
        disclaimer = Paragraph(disclaimer_text, ParagraphStyle(
            'Disclaimer',
            parent=self.normal_style,
            fontSize=9,
            textColor=colors.HexColor('#6b7280'),
            borderColor=colors.HexColor('#d1d5db'),
            borderWidth=1,
            borderPadding=10,
            backColor=colors.HexColor('#f9fafb')
        ))
        
        self.story.append(disclaimer)


def generate_pdf_report(output_path, user_info, prediction_data, image_paths):
    """
    Convenience function to generate PDF report
    
    Args:
        output_path: Path to save PDF
        user_info: User information dict
        prediction_data: Prediction results dict
        image_paths: Dict with 'original' and 'heatmap' keys
    
    Returns:
        str: Path to generated PDF
    """
    generator = BoneCancerReportGenerator(output_path)
    return generator.generate_report(user_info, prediction_data, image_paths)
