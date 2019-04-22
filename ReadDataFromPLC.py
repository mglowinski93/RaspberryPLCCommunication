from pylogix import PLC
from socket import timeout  # This is raised when no connection with PLC
from configparser import ConfigParser
from time import sleep

config = ConfigParser()
config.read("config.ini")
plc_ip_address = config.get("NETWORK", "PLC_IP_address")
delay = int(config.get("DELAY", "Delay"))
print(f"PLC address is: {plc_ip_address}")
print(f"Expected delay in read-loop: {delay} seconds")
read = True

with PLC() as comm:
    comm.Micro800 = True
    comm.IPAddress = plc_ip_address
    while read:
        try:
            analog_value = comm.Read('My_Variable')
            digital_value = comm.Read('_IO_EM_DI_00')
        except timeout:
            analog_value = None
            digital_value = None
        except KeyboardInterrupt:
            print("Exiting")
            read = False
        print(f'Analog value: {analog_value}')
        print(f'Digital value: {digital_value}')
        sleep(delay)
