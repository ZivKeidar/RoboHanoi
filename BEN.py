# !! disk3 > disk2 > disk1 !!
import Control
from Control import Arm
from Control import Gripper
import time
# from Control import Arm

point_left_low_1 = [-79.5, 25, 100, -1.5, -5.5, -1.5]
point_left_mid_2 = [-78.5, 24, 100, -1.5, -8.5, -1.5]
point_left_high_3 = [-78.5, 18, 104, -1.5, -4.5, -1.5]
point_mid_low_4 = [-89.5, 24, 100, -1.5, 1, -1.5]
point_mid_mid_5 = [-89.5, 21, 99, -1.5, 1, -1.5]
point_mid_high_6 = [-89.5, 19, 102, -1.5, -2.5, -1.5]
point_right_low_7 = [-102.5, 25, 97, -1.5, 0, -1.5]
point_right_mid_8 = [-102.5, 24, 100, -1.5, -5.5, -1.5]
point_right_high_9 = [-103.5, 22, 101, -1.5, -3.5, -1.5]

top_right = [-101.5, 12, 98, -1.5, -2, -1.5]
top_mid = [-89.5, 13, 100, -1.5, -2, -1.5]
top_left = [-78.5, 12, 97, -1.5, -2, -1.5]

places = [[point_left_low_1, point_left_mid_2, point_left_high_3], [point_mid_low_4, point_mid_mid_5, point_mid_high_6], [point_right_low_7, point_right_mid_8, point_right_high_9]] # order frome low to high --> [peg1[low,mid,high] , peg2[low,med.high] , peg3[low,med,high]]
top_places = [top_left, top_mid, top_right]  # coordinates above [peg1,peg2,peg3]
home = [-90.5, -4.5, 98, -0.5, 19, -0.5]


class Execution:
    def __init__(self, plan, state):
        self.arm = Arm()
        self.gripper = Gripper()
        self.actions = self.string2actions(plan)
        self.disk_locations = self.position2locations(state)
        self.arm.set_Current_Pos(home)
        time.sleep(4)

    def arm_execution(self, place_from, peg_from, peg_to, place_to):
        # use self.arm to send specific orders to the arm
        # for example:
        self.arm.set_Current_Pos(place_from)
        time.sleep(2)
        self.gripper.pickup()
        self.arm.set_Current_Pos(top_places[peg_from])
        time.sleep(7)
        self.arm.set_Current_Pos(home)
        time.sleep(4)
        self.arm.set_Current_Pos(top_places[peg_to])
        self.gripper.release()
        time.sleep(2)
        self.arm.set_Current_Pos(home)
        
        
        # self.arm.set_Current_Pos(top_places[peg_from])
        # time.sleep(9)
        # self.arm.set_Current_Pos(place_from)       # arm goes to disk's position
        # time.sleep(7)
        # self.gripper.pickup()
        # time.sleep(5)
        # self.arm.set_Current_Pos(top_places[peg_from])      # arm goes up
        # time.sleep(7)
        # self.arm.set_Current_Pos(top_places[peg_to])
        # time.sleep(7)
        # self.arm.set_Current_Pos(place_to)      # arm goes down
        # time.sleep(7)
        # self.gripper.release()
        # time.sleep(5)
        # self.arm.get_sent_pos(home)

    def execute_next(self):
        disk, peg_from, peg_to = self.actions[0][0], self.actions[0][1], self.actions[0][2]
        disk_num = int(disk[-1])
        peg_from_num = int(peg_from[-1]) - 1
        peg_to_num = int(peg_to[-1]) - 1
        place_from = places[peg_from_num][self.disk_locations[peg_from_num].index(disk_num)]
        if self.disk_locations[peg_to_num][0] == 0:
            place_to = places[peg_to_num][0]
        elif self.disk_locations[peg_to_num][1] == 0:
            place_to = places[peg_to_num][1]
        else:
            place_to = places[peg_to_num][2]
        print(f"need to move disk {disk_num} from peg index {peg_from_num} and place {place_from} to peg {peg_to_num} and place {place_to}")
        self.arm_execution(place_from, peg_from_num, peg_to_num, place_to)
        # TODO send disk_num, place_from and place_to to arm_execution


    def string2actions(self, plan):
        actions = plan.split('-')[:-1]
        actions = [[action.split()[1], action.split()[2], action.split()[3].replace(')', '')] for action in actions]
        return actions

    # def execute_arm(self, actions, loc):
    #     for action in actions:
    #         self.move_disc(action[0], action[1], action[2], loc)

    def position2locations(self, state): # dictionary of strings to list of intigers
        loc = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        loc[int(state['disk3'][-1])-1][0] = 3
        if state['disk2'].startswith('peg'):
            loc[int(state['disk2'][-1])-1][0] = 2
        else:
            loc[int(state[state['disk2']][-1])-1][1] = 2
        if state['disk1'].startswith('peg'):
            loc[int(state['disk1'][-1])-1][0] = 1
        elif state[state['disk1']].startswith('peg'):
            loc[int(state[state['disk1']][-1])-1][1] = 1
        else:
            loc[int(state[state[state['disk1']]][-1])-1][2] = 1
        print(loc)
        return loc

if __name__ == "__main__":
    plan = "(move disk1 peg1 peg3)-(move disk2 peg1 peg2)-(move disk1 peg3 peg2)-(move disk3 peg1 peg3)-"
    state = {'disk1': 'disk2', 'disk2': 'disk3', 'disk3': 'peg1'}
    exec = Execution(plan, state).execute_next()