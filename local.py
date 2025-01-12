from flask import Flask, jsonify
from flask_cors import CORS
import psutil

app = Flask(__name__)
CORS(app)

@app.route('/status', methods=['GET'])
def get_status():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()

    # Obtenir les températures
    try:
        temperatures = psutil.sensors_temperatures()
        temp_data = []
        if temperatures:
            for sensor_name, sensors in temperatures.items():
                for sensor in sensors:
                    temp_data.append({
                        "label": sensor.label or sensor_name,
                        "current": sensor.current
                    })
        else:
            temp_data = [{"label": "No sensors detected", "current": None}]
    except Exception as e:
        temp_data = [{"label": "Error reading temperature", "current": None}]

    # Renvoi des données
    return jsonify({
        "cpu_usage": cpu_usage,
        "memory": {
            "total": memory.total,
            "available": memory.available,
            "used": memory.used,
            "percent": memory.percent,
        },
        "temperature": temp_data
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
