import math

print("단위는 mm로..........................")
x1 = input("x1 = ")
x2 = input("x2 = ")
y1 = input("y1 = ")
y2 = input("y2 = ")

dx = int(x2) - int(x1)
dy = int(y2) - int(y1)

radian = math.atan2(dy, dx)
degree = math.degrees(radian)

sin_radian = math.sin(radian)
sin_degree = math.degrees(sin_radian)

myRPlidar_degree = 90 - degree

print(myRPlidar_degree)
print(sin_degree)