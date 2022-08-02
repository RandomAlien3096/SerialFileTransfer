"""**************************************************************************
    Author: i.R.
    File_name: main_client-t.py
    Description:


**************************************************************************"""

import serial
import base64
from csv import *
import time

def main():
    print("#########################################################################")
    print("##################### Welcome to i.R File Transfer ######################")
    print("#########################################################################")
    file_name = input('Enter the file location (use // instead of \): ')
    #getFile_list = getPath()
    #file_name = setPath(getFile_list)

    print("Loading file...")
    
    encoded_file, file_len_byte = file_converter(file_name)
    #print(file_len_byte)
    print("File loaded.")
    
    print("Opening port...")
    ser = open_port()
    print("Number of port:", ser.name)
    print("Port Opened.")
    
    print("Sending data stream...")
    write_data(ser, file_len_byte, encoded_file)
    
    print("Data sent.")
    
# =============================================================================
#     print("Receiving data...")
#     rx_data = read_data(ser)
#     print("Data received.")
#     
#     rx_file_name = input('Enter the new file name with the data type: ')
#     print("Decoding and saving file...")
#     file_decoder(rx_data, rx_file_name)
#     print("File decoded and Saved.")
# =============================================================================
    
    
    ser.close()    
    return

def getPath():
    file_name_list = []
    with open("temp.csv","r") as file_path:
        csv_reader = reader(file_path)
        for row in csv_reader:
            file_name_list.append(row)
    getFile = file_name_list[0]
    return getFile

def setPath(getFile):
    FileStr = str(getFile)
    fileStrip = FileStr.strip("['']")
    file_name = fileStrip.replace('/','//')
    return file_name


def file_converter(file_name):
    str1 = '\n'
    file_data = open(file_name,'rb')
    encoded_file = base64.b64encode(file_data.read())
    file_len = len(encoded_file)
    file_len_str = str(file_len) + str1
    file_len_byte = file_len_str.encode()
    print("The length of the file is: ", file_len)
    return encoded_file, file_len_byte

def open_port():
    ser = serial.Serial(
        port = 'COM3',
        baudrate = 4800,
        bytesize = serial.EIGHTBITS,
        parity = serial.PARITY_ODD,
        stopbits = serial.STOPBITS_ONE,
        timeout = 300.0,
        write_timeout = 300.0)
    return ser

def write_data(ser, file_len_byte, encoded_file):
    ser.write(file_len_byte)
    ser.write(encoded_file)
    return

def read_data(ser):
    rx_len_byte = ser.readline()
    rx_len_str = rx_len_byte.decode()
    rx_len_int = int(rx_len_str)
    
    rx_data = ser.read(rx_len_int)
    
    return rx_data

def file_decoder(rx_data, rx_file_name):
    decoded_file = base64.b64decode(rx_data)
    with open(rx_file_name, 'wb') as file_result:
        file_result.write(decoded_file)
        file_result.close()
    return
'''
# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()
'''

if __name__ == '__main__':
    main()
