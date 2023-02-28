import os
import time
if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

from dynamixel_sdk import *

class Motor:
    def __init__(self,id) -> None:
        MY_DXL = 'P_SERIES' 
        self.ADDR_TORQUE_ENABLE          = 512        # Control table address is different in DYNAMIXEL model
        self.ADDR_GOAL_POSITION          = 564
        self.ADDR_PRESENT_POSITION       = 580
        self.ADDR_DXL_MAX_VELOCITY       = 44
        self.ADDR_DXL_MAX_Accel          = 40
        self.ADDR_DXL_Current_LIMIT      = 38
        self.ADDR_DXL_LED_Green          = 514 
        self.ADDR_DXL_LED_Red            = 513
        self.ADDR_DXL_LED_Blue           = 515
        self.ADDR_DXL_Present_current    = 574
        self.DXL_MINIMUM_POSITION_VALUE  = -501433   # Refer to the Minimum Position Limit of product eManual
        self.DXL_MAXIMUM_POSITION_VALUE  = 501433    # Refer to the Maximum Position Limit of product eManual
        BAUDRATE                    = 1000000
        PROTOCOL_VERSION            = 2.0
        # Factory default ID of all DYNAMIXEL is 1
        self.DXL_ID                      = id
        # Use the actual port assigned to the U2D2.
        # ex) Windows: "COM*", Linux: "/dev/ttyUSB*", Mac: "/dev/tty.usbserial-*"
        DEVICENAME                  = '/dev/ttyUSB0'
        self.TORQUE_ENABLE               = 1     # Value for enabling the torque
        self.TORQUE_DISABLE              = 0     # Value for disabling the torque
        self.DXL_MOVING_STATUS_THRESHOLD = 20    # Dynamixel moving status threshold
        self.portHandler = PortHandler(DEVICENAME)
        self.packetHandler = PacketHandler(PROTOCOL_VERSION)
        if self.portHandler.openPort():
            print("Succeeded to open the port")
        else:
            print("Failed to open the port")
            print("Press any key to terminate...")
            getch()
            quit()
        if self.portHandler.setBaudRate(BAUDRATE):
            print("Succeeded to change the baudrate")
        else:
            print("Failed to change the baudrate")
            print("Press any key to terminate...")
            getch()
            quit()
            
    def Enable_Torque(self):
        dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, self.DXL_ID, self.ADDR_TORQUE_ENABLE, self.TORQUE_ENABLE)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(dxl_error))
        else:
            print("Dynamixel has been successfully connected")

    def Disable_Torque(self):
        
        dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, self.DXL_ID, self.ADDR_TORQUE_ENABLE, self.TORQUE_DISABLE)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(dxl_error))

    def SetGreenLed(self,value):
        dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(self.portHandler, self.DXL_ID, self.ADDR_DXL_LED_Green, value)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(dxl_error))
        else:
            print("Green Led changed!")

    def SetBlueLed(self,value):
        dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(self.portHandler, self.DXL_ID, self.ADDR_DXL_LED_Blue, value)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(dxl_error))
        else:
            print("Blue Led changed!")

    def SetRedLed(self,value):
        dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(self.portHandler, self.DXL_ID, self.ADDR_DXL_LED_Red, value)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(dxl_error))
        else:
            print("Red Led changed!")

    def SetCurrentLimit(self,value):
        """
        Enter Current limit in mA
        """
        dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(self.portHandler, self.DXL_ID, self.ADDR_DXL_Current_LIMIT, value)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(dxl_error))
        else:
            print("Current limit is now :"+str(value)+"mA")


    def GetCurrentLimit(self):
        """
        Get Current limit in mA
        """
        self.dxl_current_limit,dxl_comm_result, dxl_error = self.packetHandler.read2ByteTxRx(self.portHandler, self.DXL_ID, self.ADDR_DXL_Current_LIMIT)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(dxl_error))
        return self.dxl_current_limit
    

    def SetVelocityLimit(self,value):
        """
        Enter Velocity limit in rev/min
        """
        dxl_comm_result, dxl_error = self.packetHandler.write4ByteTxRx(self.portHandler, self.DXL_ID, self.ADDR_DXL_MAX_VELOCITY, value)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(dxl_error))
        else:
            print("Velocity limit is now :"+str(value)+"rev/min")


    def GetVelocityLimit(self):
        """
        Get Velocity limit in rev/min
        """
        self.dxl_current_limit,dxl_comm_result, dxl_error = self.packetHandler.read4ByteTxRx(self.portHandler, self.DXL_ID, self.ADDR_DXL_MAX_VELOCITY)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(dxl_error))
        return self.dxl_current_limit


    def SetAccelLimit(self,value):
        """
        Enter Acceleration limit in rev/min^2
        """
        dxl_comm_result, dxl_error = self.packetHandler.write4ByteTxRx(self.portHandler, self.DXL_ID, self.ADDR_DXL_MAX_Accel, value)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(dxl_error))
        else:
            print("Acceleration limit is now :"+str(value)+"rev/min^2")


    def GetAccelLimit(self):
        """
        Get Acceleration limit in rev/min^2
        """
        self.dxl_current_limit,dxl_comm_result, dxl_error = self.packetHandler.read4ByteTxRx(self.portHandler, self.DXL_ID, self.ADDR_DXL_MAX_Accel)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(dxl_error))
        return self.dxl_current_limit

    def GetPresentCurrent(self):
        """
        Get Present Current in mA
        """
        self.dxl_present_current,dxl_comm_result, dxl_error = self.packetHandler.read2ByteTxRx(self.portHandler, self.DXL_ID, self.ADDR_DXL_Present_current)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(dxl_error))
        return self.dxl_present_current

    def Close_Port(self):
        self.portHandler.closePort()
        
    
    def Write_Pos(self,angle):
        dxl_comm_result, dxl_error = self.packetHandler.write4ByteTxRx(self.portHandler, self.DXL_ID, self.ADDR_GOAL_POSITION, angle)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(dxl_error))
        # while 1:
        #     self.Read_Pos()
        #     if not abs(angle - self.dxl_present_position) > self.DXL_MOVING_STATUS_THRESHOLD:
        #         break
            
    def Read_Pos(self):
        #self.portHandler.ser.reset_input_buffer()
        self.dxl_present_position, dxl_comm_result, dxl_error = self.packetHandler.read4ByteTxRx(self.portHandler, self.DXL_ID, self.ADDR_PRESENT_POSITION)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(dxl_error))
        #print("[ID:%03d] PresPos:%03d" % (self.DXL_ID,self.dxl_present_position))
        return self.dxl_present_position
        

    def set_Max(self,max):
        self.max=max
    
    def get_Max(self):
        return self.max
    
    def set_Min(self,min):
        self.min=min
    
    def get_Min(self):
        return self.min


