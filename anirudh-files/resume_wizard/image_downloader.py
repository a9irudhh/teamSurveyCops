from flask import Flask, render_template, request, send_file
import pdfkit
import os

app = Flask(__name__)

# Configuration for pdfkit (path to wkhtmltopdf)
PDFKIT_CONFIG = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')

@app.route('/')
def index():
    return render_template('resume.html')  # Your HTML resume page

@app.route('/print_resume', methods=['POST'])
def print_resume():
    # Generate HTML from the template
    rendered_html = render_template('resume.html')
    
    # Convert HTML to PDF
    output_file = 'resume.pdf'
    pdfkit.from_string(rendered_html, output_file, configuration=PDFKIT_CONFIG)

    # Serve the generated PDF file for download
    return send_file(output_file, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
