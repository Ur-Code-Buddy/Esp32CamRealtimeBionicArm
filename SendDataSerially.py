import serial
import time

SerialObj = serial.Serial('COM11')
SerialObj.baudrate = 9600  # set Baud rate to 9600
SerialObj.bytesize = 8  # Number of data bits = 8
SerialObj.parity = 'N'  # No parity
SerialObj.stopbits = 1  # Number of Stop bits = 1
SerialObj.dtr = False

time.sleep(3)  # dont take ths out, arduino needs it


def send_data(data):

    try:
        BytesWritten = SerialObj.write(data.encode())
        print(f"sent{data}")
        time.sleep(0.5)

    except serial.SerialException as e:
        print('BytesWritten =', BytesWritten)
    # finally:
    #     SerialObj.close()

if __name__ == '__main__':
    while True:
        send_data("00010")
        time.sleep(1)
        send_data("11111")
        time.sleep(1)



