# src/sensor_integration.py
import serial

def read_from_serial(port='/dev/ttyUSB0', baudrate=115200, timeout=1.0):
    """
    Read a line of data from a serial port and parse it.
    Assumes the Arduino sends CSV: ax,ay,az,gx,gy,gz,temp
    """
    try:
        ser = serial.Serial(port, baudrate, timeout=timeout)
        line = ser.readline().decode('utf-8').strip()
        ser.close()
        if not line:
            return None
        parts = line.split(',')
        if len(parts) != 7:
            return None
        # Parse sensor values
        ax, ay, az, gx, gy, gz, temp = map(float, parts)
        return {'acc': (ax, ay, az), 'gyro': (gx, gy, gz), 'temp': temp}
    except Exception as e:
        print(f"Serial read error: {e}")
        return None

# Example usage
if __name__ == "__main__":
    data = read_from_serial()
    if data:
        print("IMU Acc:", data['acc'], "Gyro:", data['gyro'], "Temp:", data['temp'])