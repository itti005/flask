from flask import Flask, render_template, request, redirect, url_for
from nanonets import NANONETSOCR
import os
import subprocess

app = Flask(__name__)

# Initialize Nanonets OCR model
model = NANONETSOCR()
# Replace 'REPLACE_API_KEY' with your actual API key
model.set_token('1d37e4c0-d32f-11ee-acb4-3a5cdf296df9')

def generate_csv_from_file(input_file_path, output_csv_path='output_data.csv'):
    # Convert to CSV
    model.convert_to_csv(input_file_path, output_file_name=output_csv_path)
    print(f"CSV file generated: {output_csv_path}")
    return output_csv_path

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the uploaded file
        file = request.files['file']

        if file:
            # Save the file to a temporary location
            temp_file_path = 'temp_input_file' + os.path.splitext(file.filename)[1]  # Adjust the file extension

            file.save(temp_file_path)

            # Generate CSV from the uploaded file
            generated_csv_path = generate_csv_from_file(temp_file_path)

            # Clean up: Remove the temporary file
            os.remove(temp_file_path)

            # Open the generated CSV file
            open_csv_command = f'start excel "{generated_csv_path}"'  # Adjust based on your system
            subprocess.Popen(open_csv_command, shell=True)

            return redirect(url_for('index'))

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
