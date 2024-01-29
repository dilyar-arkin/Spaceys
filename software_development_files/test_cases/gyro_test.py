from MinIMU_v5_pi import MinIMU_v5_pi


def main():
#Setup the MinIMU_v5_pi
    IMU = MinIMU_v5_pi()

#Initiate tracking of Yaw on the IMU
    IMU.trackYaw()

    while True: #Main loop             
        time.sleep(1)
        yaw = IMU.prevYaw[0]
        print (yaw)

main()
