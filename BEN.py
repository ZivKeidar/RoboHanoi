# !! disk3 > disk2 > disk1 !!
# from Nir import Arm
# from Control import Arm
places = [[1, 2, 3], [4, 5, 6], [7, 8, 9]] # order frome low to high --> [peg1[low,mid,high] , peg2[low,med.high] , peg3[low,med,high]]
top_places = [111, 222, 333]  # coordinates above [peg1,peg2,peg3]
home = []


class Execution:
    def __init__(self, plan, state):
        # self.arm = Arm()
        self.actions = self.string2actions(plan)
        self.disk_locations = self.position2locations(state)

    def arm_execution(self, disk_num, place_from, place_to):
        # use self.arm to send specific orders to the arm
        # for example:
        # arm.get_sent_pos(from_)       # arm goes to disk's position
        # gripper = Gripper()
        # gripper.pickup()
        # arm.get_sent_pos(top_places[peg_from])      # arm goes up
        # arm.get_sent_pos(top_places[peg_to])
        # arm.get_sent_pos(to)      # arm goes down
        # gripper.release()
        # arm.get_sent_pos(home)
        pass

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
        print(f"need to move disk {disk_num} from {place_from} to {place_to}")
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
        return loc

if __name__ == "__main__":
    plan = "(move disk1 peg1 peg3)-(move disk2 peg1 peg2)-(move disk1 peg3 peg2)-(move disk3 peg1 peg3)-"
    state = {'disk1': 'disk2', 'disk2': 'disk3', 'disk3': 'peg1'}
    exec = Execution(plan, state).execute_next()