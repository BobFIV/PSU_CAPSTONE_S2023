import binascii
import face_recognition
import numpy as np
import os
import time

# ab_image = face_recognition.load_image_file("ab.png")
# ab_encoding = face_recognition.face_encodings(ab_image)[0]
#
# np.savetxt("abencoding.txt", ab_encoding)
#
# hexstring = binascii.hexlify(bytearray(np.loadtxt("abencoding.txt")))
# print(hexstring)
#
# unhexed = binascii.unhexlify(hexstring).hex()
# b = np.loadtxt("abencoding.txt")
#
# print(unhexed)

file_name = ""
file_data_hex = ""
file_location = "/media/ab/5021-0080/TEST.txt"

def refresh_usb_ports():
    cmd = "echo '1-1' | sudo tee /sys/bus/usb/drivers/usb/unbind ; echo '1-1' | sudo tee /sys/bus/usb/drivers/usb/bind"
    os.system(cmd)

def parse_data():
    with open(file_location, 'rb') as fp:
        data = fp.read()
    data = data.decode()
    
    data_found = False

    # Get header
    header_start_index = data.find('Header:') + 7
    if(header_start_index == 6):
        print('No data found')
        return
    else:
        data_found = True
    header_end_index = data.find('EndHeader')
    header = data[header_start_index:header_end_index]

    # Get name from header, unnecessary rn but whatever
    name = data[header_start_index+5:header_end_index]

    # Get data
    payload_start_index = data.find('Data:') + 5
    payload_end_index = data.find('EndData')
    payload = data[payload_start_index:payload_end_index]

    #print(payload)
    # Create file with name and unhexed payload
    with open(name, 'wb') as fp:
        fp.write(binascii.unhexlify(payload))
    #with open(file_location, 'wb') as fp:
    #    fp.truncate(0)
    if data_found:
        file = open(file_location, 'w')
        file.close()
    #b = np.loadtxt(name)
    #print(b)


#parse_data()
while(1):
    refresh_usb_ports()
    time.sleep(3)
    parse_data()
#    break
