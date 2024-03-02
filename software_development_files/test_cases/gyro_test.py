from MinIMU_v5_pi import MinIMU_v5_pi
import time

def main():
#Setup the MinIMU_v5_pi
    IMU = MinIMU_v5_pi()

#Initiate tracking of Yaw on the IMU
    IMU.trackYaw()

    while True: #Main loop       
        time.sleep(1)
        if IMU.prevYaw:   #check if there's yaw data
                yaw = IMU.prevYaw[0]
                print (yaw)
        else: #if no yaw data
             print("No yaw data.");
        
main()
