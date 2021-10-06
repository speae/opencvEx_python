from pyrplidar import PyRPlidar

lidar = PyRPlidar()

# 115200 | 256000
lidar.connect("COM3", baudrate=115200, timeout=1)

info = lidar.get_info()
print("info : ", info)

health = lidar.get_health()
print("health : ", health)

samplerate = lidar.get_samplerate()
print("samplerate : ", samplerate)

scan_modes = lidar.get_scan_modes()
print("scan modes : ")
for scan_modes in scan_modes:
    print(scan_modes)

lidar.disconnect()