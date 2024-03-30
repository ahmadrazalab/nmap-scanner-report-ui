# nmap-ui-app-report

# Nmap UI

Nmap UI is a simple web application built with Flask that allows users to interact with the Nmap tool for scanning and generating reports.

## Installation

1. Clone this repository:

    ```bash
    git clone https://github.com/minikube-mini-projects/nmap-ui-app-report.git
    ```

2. Navigate to the project directory:

    ```bash
    cd nmap-ui
    ```

3. Build the Docker image:

    ```bash
    docker build -t nmap-ui .
    ```

## Usage

1. Run a Docker container based on the built image:

    ```bash
    docker run -p 5000:5000 nmap-ui
    ```

2. Open your web browser and go to `http://localhost:5000` to access the Nmap UI application.

3. Enter the target IP address or domain name into the input field and click the "Scan" button to initiate a scan.

4. Once the scan is complete, you will see the generated report file listed on the page. You can download the report by clicking the link.

5. Additionally, recent scan details will be displayed on the page, showing the filenames and timestamps of the most recent scans.

## Notes

- This application is intended for demonstration purposes and should not be used in a production environment without proper security considerations.
- Ensure that Docker is installed and running on your system before following the installation and usage instructions.
- If you encounter any issues or have questions, please feel free to open an issue on GitHub.
