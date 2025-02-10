# lists all serial ports and attached devices
sudo dmesg | grep tty

# save the port to a text file
ls /dev/ttyUSB0 >connected_spectrometer_port.txt

#freexe requirements.txt file
pip3 freeze > requirements.txt

