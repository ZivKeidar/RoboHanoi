import move
# import PS4Controller
import time
from ikpy import chain
import numpy as np

class Arm:
    
    def __init__(self) -> None:
        """_summary_

        Returns:
            _type_: _description_
        """
        MODE="FORWARD"
        # try:
        #     ctrl=PS4Controller
        #     self.ps4=ctrl.PS4Controller()
        # except:
        #     print("No Controller Found")
        self.M1=move.Motor(1)
        self.M2=move.Motor(2)
        self.M3=move.Motor(3)
        self.M4=move.Motor(4)
        self.M5=move.Motor(5)
        self.M6=move.Motor(6)
        self.RANGES=[[-500000,500000],[-301160,306738],[-278852,278852],[-500000,500000],[-301160,301160],[-500000,500000]]
        self.Sent_Positions=[0,0,0,0,0,0]
        self.motors=[self.M1,self.M2,self.M3,self.M4,self.M5,self.M6]
        for m in self.motors:
            m.SetCurrentLimit(6000)
            m.SetAccelLimit(500)
            m.SetVelocityLimit(100)
        # self.Home()
        
    def EnableTorque(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        for motor in self.motors:
            motor.Enable_Torque()
            
    def DisableTorque(self):   
        """_summary_

        Returns:
            _type_: _description_
        """
        for motor in self.motors:
            motor.Disable_Torque()

    def _map(self,x, in_min, in_max, out_min, out_max):
        """gets a number and maps it from one ragne to another range.

        Returns:
           float: the number in the new range
        """
        return float((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)
    
    def set_range(self,id,min,max):
        """_summary_

        Args:
            int:id
            int:min-angle in degrees
            int-max-angle in degrees
        Returns:
            void
        """
        r0=self._map(min,0,360,-501433,501433)
        r1=self._map(max,0,360,-501433,501433)
        self.RANGES[id][0]=r0
        self.RANGES[id][1]=r1
            
    def set_Ranges(self,ranges):
        """_summary_

        Args:
            ranges (list of ranges [M1[min,max],M2[min,max]...]): list of ranges of every motor min and max in units of degrees.
        """
        for i, r in enumerate(ranges):
            r0=self._map(r[0],0,360,-501433,501433)
            r1=self._map(r[1],0,360,-501433,501433)
            self.RANGES[i][0]=r0
            self.RANGES[i][1]=r1
    
    def get_Ranges(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.RANGES

    def get_Current_Pos(self):
        """return all current positions 

        Returns:
            list: list of current angles
        """
        # self.EnableTorque()
        self.M1_angle=self._map(self.M1.Read_Pos(),-501433,501433,-180,180)
        self.M2_angle=self._map(self.M2.Read_Pos(),-501433,501433,-180,180)
        self.M3_angle=self._map(self.M3.Read_Pos(),-501433,501433,-180,180)
        self.M4_angle=self._map(self.M4.Read_Pos(),-501433,501433,-180,180)
        self.M5_angle=self._map(self.M5.Read_Pos(),-501433,501433,-180,180)
        self.M6_angle=self._map(self.M6.Read_Pos(),-501433,501433,-180,180)
        self.angles=[self.M1_angle,self.M2_angle,self.M3_angle,self.M4_angle,self.M5_angle,self.M6_angle]
        for idx,angle in enumerate(self.angles):
            if angle>360:
                self.angles[idx]=angle-1541769.5
        return self.angles
    
    def set_Current_Pos(self,angles):
        """get all angles and set positions 

        Returns:
            void: setting angles 
        """
        for idx in range(len(self.motors)):
            pos=int(self._map(angles[idx],-180,180,-501433,501433))
            print(pos)
            # if pos>=self.RANGES[idx][0] and pos<=self.RANGES[idx][1]:
            self.motors[idx].Write_Pos(pos)
            self.Sent_Positions[idx]=pos
            # else:
            #     print("Angle "+str(idx)+" is out of range! ")
    
    def inRange(self,value,id):
        return self.motors[id].DXL_MAXIMUM_POSITION_VALUE>value and self.motors[id].DXL_MINIMUM_POSITION_VALUE<value

    def get_sent_pos(self):
        """get all the positions set 

        Returns:
            list: positions for all motors
        """
        return self.Sent_Positions
    def SetXYZ(self,position,orientation,q_init):
        """Inverse Kinemtics

        Args:
            position (List[]): [x,y,z,1],
            orientation (List[,]): [[u_x,v_x,w_x],[u_y,v_y,w_y],[u_z,v_z,w_z]]
            q_init (q_init = np.array([0, 0, 0, 0, 0, 0])): initial values conditions,joint angles.
        """
        # Define the DH parameters of the robot arm
        dh_params = [
        {'alpha': np.pi/2, 'a': 0, 'd': 0.3, 'theta': 0},
        {'alpha': 0, 'a': 0.4, 'd': 0, 'theta': 0},
        {'alpha': 0, 'a': 0.4, 'd': 0, 'theta': 0},
        {'alpha': np.pi/2, 'a': 0, 'd': 0.4, 'theta': 0},
        {'alpha': np.pi/2, 'a': 0, 'd': 0.4, 'theta': 0},
        {'alpha': 0, 'a': 0, 'd': 0, 'theta': 0}
        ]

       # Create an instance of the Chain class
        my_chain = chain.Chain.from_dh_parameters(dh_params)

        # Define the desired position and orientation of the end effector
        end_effector_pose = np.array([orientation, position])
        
        joint_angles = my_chain.inverse_kinematics(end_effector_pose, q_init)
        print(joint_angles)
        return joint_angles

    def Home(self):
        finished=False
        while not finished:
            self.motors[1].Enable_Torque()
            self.motors[1].Write_Pos(0)
            if not self.inRange(self.motors[1].Read_Pos(),1):
                raise Exception("Out of range, Homing failed, Try moving the arm and homing again")
            if self.motors[1].Read_Pos()==0:
                self.motors[0].Enable_Torque()
                self.motors[0].Write_Pos(0)
                if not self.inRange(self.motors[0].Read_Pos(),0):
                    raise Exception("Out of range, Homing failed, Try moving the arm and homing again")
                if self.motors[0].Read_Pos()==0:
                    self.motors[2].Enable_Torque()
                    self.motors[2].Write_Pos(0)
                    if not self.inRange(self.motors[2].Read_Pos(),2):
                        raise Exception("Out of range, Homing failed, Try moving the arm and homing again")
                    if self.motors[2].Read_Pos()==0:
                        self.motors[3].Enable_Torque()
                        self.motors[3].Write_Pos(0)
                        if not self.inRange(self.motors[3].Read_Pos(),3):
                            raise Exception("Out of range, Homing failed, Try moving the arm and homing again")
                        if self.motors[3].Read_Pos()==0:
                            self.motors[4].Enable_Torque()
                            self.motors[4].Write_Pos(0)
                            if not self.inRange(self.motors[4].Read_Pos(),4):
                                raise Exception("Out of range, Homing failed, Try moving the arm and homing again")
                            if self.motors[4].Read_Pos()==0:
                                self.motors[5].Enable_Torque()
                                self.motors[5].Write_Pos(0)
                                if not self.inRange(self.motors[5].Read_Pos(),5):
                                    raise Exception("Out of range, Homing failed, Try moving the arm and homing again")
                                if self.motors[5].Write_Pos(0)==0:
                                    finished=True

        
    def Ps4Control(self):
        start_time = None
        kill=False
        last_press_time = None
        double_press_threshold = 0.5 # seconds

        if self.ps4.options()==1:
            start_time = time.time()
            if self.ps4.options() == 0: # button released
                if start_time is not None:
                    if time.time() - start_time >= 5:
                        print("Started PS4 control")
                        while not kill:
                            kill_btn=self.ps4.kill()
                            mode_btn=self.ps4.share()
                            options_btn=self.ps4.options()
                            #check if to kill the arm
                            if kill_btn==1:
                                kill_btn=self.ps4.kill()
                                if kill_btn==0:
                                    print("Exit")
                                    self.Exit()
                                 
                            if mode_btn==1  :
                                start_time = time.time()
                                mode_btn=self.ps4.share()
                                if mode_btn==0:
                                    if time.time() - start_time >= 5:
                                        if MODE=="FORWARD":
                                            MODE="INVERSE"
                                            print("MODE CHANGED TO INVERSE KINEMATIC!!! PAY ATTENTION!")
                                        elif MODE=="INVERSE":
                                            MODE="FORWARD"  
                                            print("MODE CHANGED TO FORWARD KINEMATIC!!! PAY ATTENTION!")
                                        elif MODE=="SELFAWARENESS":
                                            MODE="FORWARD"  
                                            print("MODE CHANGED TO FORWARD KINEMATIC!!! PAY ATTENTION!")
                            if mode_btn==1 and MODE!="SELFAWARENESS":
                                current_time = time.time()
                                if last_press_time is not None and current_time - last_press_time <= double_press_threshold:
                                    MODE="SELFAWARENESS"
                                    print("MODE CHANGED TO SELFAWARENESS!!! PAY ATTENTION!")   
                                    last_press_time = current_time
                                    
                            if mode_btn==1 and options_btn==1 :
                                start_time = time.time()
                                mode_btn=self.ps4.share()
                                if mode_btn==0 and options_btn==0:
                                    if time.time() - start_time >= 5:
                                        MODE="PLANNING"
                                        print("MODE CHANGED TO PLANNING !!! PAY ATTENTION!")
                            
                            if MODE=="FORWARD":
                            #FORWARD KINEMATICS CONTROL  
                                pass  
                            if MODE=="INVERSE":
                            #INVERSE KINEMATICS CONTROL  
                                pass  
                            if MODE=="SELFAWARENESS":
                            #SELFAWARENESS CONTROL  - POLICY RUNNING NEURAL NETWORK 
                                pass 
                            if MODE=="PLANNING":
                            #PLANNING CONTROL  - Running Predetermined Plan
                                pass 
            

    def Exit(self):
        """Kill motors

        Returns:
            void
        """
        self.M1.Close_Port()

class Gripper():
    def _init_(self) -> None:
        self.HOST = '172.20.10.6'  # replace with the IP address of your ESP
        self.PORT = 80  # replace with the port number you set up on the ESP

    def pickup(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.HOST, self.PORT))
            s.sendall(b'150')
            success = s.recv(1024)
            print('Received', repr(success))
            return success

    def release(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.HOST, self.PORT))
            s.sendall(b'165')
            success = s.recv(1024)
            print('Received', repr(success))
            return success
        
arm=Arm()
# arm.DisableTorque()
arm.EnableTorque()

# arm.Home()
# for motor in arm.motors:
#     motor.Write_Pos(0)

# time.sleep(5)
# arm.motors[1].Write_Pos(int(arm._map(30,-180,180,-501433,501433)))
# print(arm.get_Current_Pos())

angls_HOME=[-90, 41, 97, 0, -45, 0]
# arm.set_Current_Pos(angls)
print(arm.get_Current_Pos())

#1541679

point_left_low_1 = [-77.17947063711472, 56.4177068521617, 90.53325170062601, -0.02256233640946448, -60.43849028693512, 0.003642560448497534]
point_left_mid_2 = [-77.20136787975207, 53.04804430502182, 91.12124650750945, -0.02256233640946448, -52.19758871081285, 0.003642560448497534]
point_left_high_3 = [-78.16700037685223, 49.59007484549281, 90.16063960688666, -0.02292130747810006, -48.085214774357155, 0.003642560448497534]
point_mid_low_4 = [-89.60382244479842, 53.420297427572564, 94.44101205943764, 0.00938609940931201, -53.85459971730597, 0.004001531517133117]
point_mid_mid_5 = [-89.22941549518146, 53.081787596747716, 91.99857209238326, 0.010463013080880046, -53.84490749519318, 0.004001531517133117]
point_mid_high_6 = [-88.82341908081435, 50.64257837039045, 92.04918702997207, 0.013281933977225435, -53.84598440863192, 0.003642560448497534]
point_right_low_7 = [-99.40086412336677, 55.68181591558593, 90.74432675950726, -0.028664846438914537, -59.89034128189087, 0.0032835891470313072]
point_right_mid_8 = [-100.7574162450619, 54.76284967283766, 90.78453153262751, -0.02184439403936267, -61.69919710117392, 0.0032835891470313072]
point_right_high_9 = [-100.95951702422462, 50.80806408832288, 90.31427927559616, -0.02184439403936267, -53.60439679888077, 0.0032835891470313072]

top_right = [-100.32952258829027, 41.592914706451324, 88.01327395683973, -0.04410060774534941, -45.553032010328025, 0.0032835891470313072]
top_mid = [-89.49146446282975, 39.04098852688196, 94.79962427682261, -0.04086986696347594, -45.596108552999794, 0.0032835891470313072]
top_left = [-77.12562495889142, 41.87147634878437, 92.81379566163378, -0.040510895662009716, -45.597903408808634, 0.0032835891470313072]
arm.set_Current_Pos(angls_HOME)
time.sleep(3)
places=[point_left_low_1,point_left_mid_2,point_left_high_3,point_mid_low_4,point_mid_mid_5,point_mid_high_6,point_right_low_7,point_right_mid_8,point_right_high_9,top_right,top_mid,top_left]
for place in places:
    arm.set_Current_Pos([int(item) for item in place])
    time.sleep(1)