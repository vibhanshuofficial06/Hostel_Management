from flask import Flask, render_template, request, jsonify, Response
import csv
from allocation import allocate_rooms
from io import StringIO

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    group_info = None
    hostel_info = None

    
    group_file = request.files['group_file']
    hostel_file = request.files['hostel_file']

    if group_file and hostel_file:
        
        group_info = process_csv(group_file)

        
        hostel_info = process_csv(hostel_file)

        if group_info and hostel_info:
            
            allocation_results = allocate_rooms(group_info, hostel_info)

            
            csv_output = generate_csv(allocation_results)

            
            return Response(
                csv_output,
                mimetype="text/csv",
                headers={"Content-disposition":
                         "attachment; filename=room_allocation.csv"})

        else:
            return jsonify({'error': 'Failed to parse CSV files'})

    return jsonify({'error': 'Files not uploaded'})

def process_csv(csv_file):
    data = []
    csv_reader = csv.DictReader(csv_file.stream.read().decode('utf-8').splitlines())
    for row in csv_reader:
        data.append(dict(row))
    return data

def generate_csv(allocation_results):
    output = StringIO()
    fieldnames = ['Group ID', 'HostelName', 'Room Number', 'Members Allocated']  # Include 'Members Allocated'
    csv_writer = csv.DictWriter(output, fieldnames=fieldnames)
    csv_writer.writeheader()
    for result in allocation_results:
        csv_writer.writerow({
            'Group ID': result['Group ID'],
            'HostelName': result['HostelName'],
            'Room Number': result['Room Number'],
            'Members Allocated': result['Members Allocated']  # Assuming 'Members Allocated' is a key in allocation_results
        })
    return output.getvalue()

if __name__ == '__main__':
    app.run(debug=True)
