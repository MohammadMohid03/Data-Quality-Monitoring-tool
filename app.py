import os
import pandas as pd
from datetime import datetime
from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
from dq_core.checks import run_all_checks
from dq_core.reporters import deduce_status

app = Flask(__name__)
app.secret_key = 'super-secret-key-for-flash-messages'

# Reusing the existing template directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.template_folder = os.path.join(BASE_DIR, 'templates')

UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def index():
    """Renders the dashboard landing page offering CSV upload."""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handles the file upload and synchronous processing of the dataset."""
    if 'file' not in request.files:
        flash('No file part provided in the request.', 'error')
        return redirect(request.url)
        
    file = request.files['file']
    
    if file.filename == '':
        flash('No file was selected for uploading.', 'error')
        return redirect(request.url)
        
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Load Data
            df = pd.read_csv(filepath)
            
            # Run Checks
            results = run_all_checks(df)
            
            # Decorate the results with UI statuses (reproducing the CLI reporter logic)
            # Process Nulls
            for col, data in results['nulls'].items():
                data['status'] = deduce_status(data['percentage'])
                
            # Process Duplicates
            results['duplicates']['status'] = deduce_status(results['duplicates']['percentage'], critical_threshold=2.0)
            
            # Process Outliers
            for col, data in results['outliers'].items():
                data['status'] = deduce_status(data['outlier_percentage'], critical_threshold=5.0)
                
            # Process Patterns
            for col, data in results['patterns'].items():
                data['status'] = deduce_status(data['invalid_percentage'], critical_threshold=2.0)
                
            # Render the report directly using the existing template 
            # (Flask uses Jinja2 intrinsically, so we can recycle the existing template)
            return render_template(
                'report_template.html', 
                report_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                results=results,
                filename=filename
            )
            
        except Exception as e:
            flash(f"Error processing the file: {str(e)}", 'error')
            return redirect(url_for('index'))
            
    else:
        flash('Allowed file types are solely .csv', 'error')
        return redirect(request.url)

if __name__ == '__main__':
    # Running in debug mode for local development
    app.run(debug=True, port=5000)
