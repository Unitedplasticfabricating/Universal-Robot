import serial
import time

def main():
    # Configure the serial connection
    ser = serial.Serial(
        port='COM7',        # Replace with your port
        baudrate=1200,      # Baud rate
        bytesize=serial.EIGHTBITS,  # 8 data bits
        parity=serial.PARITY_NONE,   # No parity
        stopbits=serial.STOPBITS_ONE, # 1 stop bit
        timeout=1           # Read timeout
    )

    # Allow time for the connection to establish
    time.sleep(2)

    try:
        while True:
            # Get user input
            command = input("Enter command to send (or 'exit' to quit): ")
            if command.lower() == 'exit':
                break

            # Send the command
            ser.write(command.encode('latin-1'))
            print(f"Sent: {command}")

            # Read response from the device
            response = ser.readline().decode('latin-1').strip()
            print(f"Received: {response}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the serial connection
        ser.close()

if __name__ == "__main__":
    main()
