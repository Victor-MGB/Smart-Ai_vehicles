import random
import uuid
from datetime import datetime
from faker import Faker
import json
import time

fake = Faker()

def generate_error_code():
    codes = ['OK', 'WARN_TEMP', 'ERR_VIB', 'LOW_BATT', 'BRAKE_WEAR', 'NONE']
    return random.choices(codes, weights=[60, 10, 10, 10, 5, 5])[0]

def generate_random_coordinates():
    # Nigeria bounding box (roughly): lat 4.3–13.9, lon 3.3–14.7
    latitude = round(random.uniform(4.3, 13.9), 6)
    longitude = round(random.uniform(3.3, 14.7), 6)
    return latitude, longitude

def generate_component_data(component_id: str):
    temperature = round(random.gauss(65, 5), 2)
    vibration = round(random.gauss(0.5, 0.1), 3)
    voltage = round(random.uniform(11.5, 13.0), 2)
    brake_thickness = round(random.uniform(0.4, 1.5), 2)

    # Inject occasional anomalies
    if random.random() < 0.05:
        temperature += random.uniform(15, 30)
        vibration += random.uniform(0.5, 1.2)
        voltage -= random.uniform(1.0, 2.0)
        brake_thickness -= random.uniform(0.2, 0.4)

    lat, lon = generate_random_coordinates()

    return {
        "component_id": component_id,
        "vehicle_id": f"VH-{random.randint(1000,9999)}",
        "timestamp": datetime.now().isoformat(),
        "location": {
            "latitude": lat,
            "longitude": lon
        },
        "battery": {
            "temperature": temperature,
            "voltage": voltage,
            "error_code": generate_error_code()
        },
        "motor": {
            "vibration_level": vibration,
            "torque": round(random.uniform(10.0, 50.0), 2),
            "error_code": generate_error_code()
        },
        "brake_system": {
            "brake_pad_thickness": brake_thickness,
            "temperature": round(temperature + random.uniform(5, 15), 2),
            "error_code": generate_error_code()
        },
        "last_service_date": fake.date_between(start_date="-90d", end_date="-1d").isoformat(),
        "component_age_days": random.randint(5, 365)
    }

# Run as standalone script
if __name__ == "__main__":
    with open("data/sensor_data_stream.jsonl", "w") as f:
        for _ in range(1000):
            data = generate_component_data(str(uuid.uuid4()))
            f.write(json.dumps(data) + "\n")
            time.sleep(0.1)  # Simulate streaming
