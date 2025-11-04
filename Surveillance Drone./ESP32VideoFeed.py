import cv2
import serial
import numpy as np

ser = serial.Serial('COM3', 115200, timeout=1)

start_sequence = b'\xff\xd8'  # JPEG start
end_sequence = b'\xff\xd9'    # JPEG end

buffer = bytearray()

while True:
    # Read data from the serial port
    if ser.in_waiting > 0:
        data = ser.read(ser.in_waiting)
        buffer.extend(data)
        
        # Check for a full JPEG frame in the buffer
        start_index = buffer.find(start_sequence)
        end_index = buffer.find(end_sequence)

        if start_index != -1 and end_index != -1 and end_index > start_index:
            jpg_data = buffer[start_index:end_index + 2]
            buffer = buffer[end_index + 2:]  
            
            # Convert the JPEG data to an image
            np_arr = np.frombuffer(jpg_data, np.uint8)
            img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            
            if img is not None:
                cv2.imshow('ESP32-CAM Video Feed', img)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

ser.close()
cv2.destroyAllWindows()
