from flask import Flask, render_template, request, jsonify
import serial
import json
import platform
import serial.tools.list_ports
import os

app = Flask(__name__)

# Verify template directory exists
template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
if not os.path.exists(template_dir):
    os.makedirs(template_dir)
    print(f"Created template directory at: {template_dir}")

def get_available_ports():
    """Get list of available serial ports based on OS"""
    try:
        return [port.device for port in serial.tools.list_ports.comports()]
    except:
        return []

def get_os_type():
    """Detect operating system"""
    system = platform.system()
    return "Windows" if system == "Windows" else "Linux"

@app.route('/get_ports')
def get_ports():
    """API endpoint to get available ports"""
    try:
        ports = get_available_ports()
        return jsonify({"ports": ports})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def index():
    try:
        return render_template('index.html', 
                             os_type=get_os_type(),
                             available_ports=get_available_ports())
    except Exception as e:
        return f"""
        Error: Could not find template file. 
        Please ensure 'index.html' exists in the 'templates' folder.
        Current working directory: {os.getcwd()}
        Template directory: {template_dir}
        Error message: {str(e)}
        """

@app.route('/submit_settings', methods=['POST'])
def submit_settings():
    try:
        data = request.json
        
        # Check if we received any data
        if not data:
            return jsonify({"status": "error", "message": "No settings provided"}), 400

        # Configure serial connection if port is specified
        if 'port' in data:
            ser = serial.Serial(
                port=data['port'],
                baudrate=int(data.get('baudrate', 9600)),
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1
            )
            
            # Prepare network settings data (only include provided values)
            network_settings = {}
            for key in ['vlan_id', 'ip_address', 'subnet_mask', 'gateway']:
                if key in data and data[key]:
                    network_settings[key] = data[key]
            
            # Only send data if we have network settings
            if network_settings:
                serial_data = json.dumps(network_settings) + '\n'
                ser.write(serial_data.encode())
                response = ser.readline().decode().strip()
            else:
                response = "No network settings to apply"
            
            ser.close()
            
            return jsonify({"status": "success", "response": response})
        else:
            # Handle case where only network settings are provided (no serial port)
            return jsonify({"status": "success", "message": "Settings stored (no serial port specified)"})
            
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    print(f"Template directory is at: {template_dir}")
    print(f"Current working directory: {os.getcwd()}")
    print("Available ports:", get_available_ports())
    app.run(host='0.0.0.0', port=5000, debug=True)