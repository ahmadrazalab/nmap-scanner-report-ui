# app.py

from flask import Flask, render_template, request, send_file
import subprocess
import os
from datetime import datetime

app = Flask(__name__)

# Ensure 'reports' directory exists
if not os.path.exists('reports'):
    os.makedirs('reports')

@app.route('/')
def index():
    recent_scans = get_recent_scans()
    return render_template('index.html', recent_scans=recent_scans)

def get_recent_scans():
    recent_scans = []
    for file in os.listdir('reports'):
        if file.endswith('.txt'):
            file_path = os.path.join('reports', file)
            scan_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            recent_scans.append({'file': file, 'time': scan_time})
    recent_scans.sort(key=lambda x: x['time'], reverse=True)
    return recent_scans[:5]  # Show the 5 most recent scans

@app.route('/scan', methods=['POST'])
def scan():
    target = request.form['target']
    output_file = f'reports/scan_{target}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'  # Include target in filename
    
    # Run Nmap command
    nmap_command = f'nmap -oN {output_file} {target}'
    subprocess.run(nmap_command, shell=True)
    
    # Parse scan result for open ports and service versions
    open_ports, service_versions = parse_scan_result(output_file)
    
    return render_template('index.html', scan_result=output_file, open_ports=open_ports, service_versions=service_versions)

def parse_scan_result(output_file):
    open_ports = []
    service_versions = {}
    with open(output_file, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if "/tcp" in line:
                port_info = line.split()
                open_ports.append(port_info[0])
                service_versions[port_info[0]] = port_info[-1].strip()
    return open_ports, service_versions

@app.route('/download/<path:file_name>')
def download(file_name):
    return send_file(f'reports/{file_name}', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
