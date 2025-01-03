# Network Settings Configuration

This repository provides a Flask-based web interface for configuring network settings and managing serial communication. The application dynamically detects available serial ports, allows users to configure system and network settings, and sends these settings to a connected serial device.

## Features

- Dynamic detection of available serial ports.
- OS-specific port handling (Windows/Linux).
- Easy configuration of network settings (VLAN, IP Address, Subnet Mask, Gateway).
- RESTful API for retrieving available ports and submitting settings.
- Dockerized for easy deployment.

## File Overview

### 1. Dockerfile
- Sets up the Python 3.9 slim environment.
- Installs required system dependencies (`gcc`, `libudev-dev`).
- Installs Python dependencies from `requirements.txt`.
- Copies application files and exposes port 5000.
- Command: Runs the Flask app (`serial-web-interface.py`).

### 2. docker-compose.yaml
- Defines the service for the Flask application.
- Maps port 5000 on the host to port 5000 in the container.
- Mounts the `/dev` directory for serial port access.
- Specifies `privileged: true` for device access.
- Restarts the container unless stopped manually.

### 3. requirements.txt
- Lists Python dependencies:
  - `flask==3.0.0`: For creating the web interface.
  - `pyserial==3.5`: For handling serial communication.

### 4. serial-web-interface.py
- Flask application with the following endpoints:
  - `/`: Renders the main HTML interface for configuration.
  - `/get_ports`: API to retrieve available serial ports.
  - `/submit_settings`: API to submit network and serial settings.
- Handles serial communication and applies network configurations.

### 5. templates/index.html
- HTML front-end for the application.
- Features:
  - Dropdowns for OS selection, serial port, and baud rate.
  - Form fields for VLAN, IP Address, Subnet Mask, and Gateway.
  - Responsive status messages for success and errors.

## Prerequisites

- **Docker** and **Docker Compose** installed on your system.
- Serial device connected to the host machine.
- Python (optional, if running locally).

## Deployment

### Using Docker Compose

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/network-settings-config.git
   cd network-settings-config
   ```

2. Build and run the application:
   ```bash
   docker-compose up --build
   ```

3. Access the application in your browser at `http://localhost:5000`.

### Running Locally

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python serial-web-interface.py
   ```

3. Access the application in your browser at `http://localhost:5000`.

## Usage

1. Open the application in your browser.
2. Select the operating system and available serial port.
3. Configure network settings (VLAN ID, IP Address, Subnet Mask, Gateway).
4. Click "Apply Settings" to send the configuration to the serial device.

## API Endpoints

### `/get_ports`
- **Method**: GET
- **Response**:
  ```json
  {
      "ports": ["COM1", "COM2", ...] // Example for Windows
  }
  ```

### `/submit_settings`
- **Method**: POST
- **Request**:
  ```json
  {
      "port": "COM1",
      "baudrate": 9600,
      "vlan_id": 100,
      "ip_address": "192.168.1.10",
      "subnet_mask": "255.255.255.0",
      "gateway": "192.168.1.1"
  }
  ```
- **Response** (success):
  ```json
  {
      "status": "success",
      "response": "Settings applied successfully!"
  }
  ```
- **Response** (error):
  ```json
  {
      "status": "error",
      "message": "Error details"
  }
  ```

## Directory Structure

```
network-settings-config/
|-- Dockerfile
|-- docker-compose.yaml
|-- requirements.txt
|-- serial-web-interface.py
|-- templates/
    |-- index.html
```

## Contributing

1. Fork the repository.
2. Create a new branch for your feature: `git checkout -b feature-name`.
3. Commit your changes: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature-name`.
5. Open a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

- Flask documentation for their excellent tutorials.
- pySerial library for simplifying serial communication.

---

Feel free to submit issues or suggestions to improve the project!
