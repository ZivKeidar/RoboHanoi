from Robot.Code.Control import Arm
from Robot.Code.Control import Gripper
# from Control import Arm
places = [[1, 2, 3], [4, 5, 6], [7, 8, 9]] # order frome low to high --> [peg1[low,mid,high] , peg2[low,med.high] , peg3[low,med,high]]
top_places = [111, 222, 333]  # coordinates above [peg1,peg2,peg3]
home = []

place_from = places[0][2]
peg_from, peg_to = 0, 1
place_to = places[1][0]

arm = Arm()
gripper = Gripper()

arm.set_Current_Pos(place_from)       # arm goes to disk's position
gripper.pickup()
arm.set_Current_Pos(top_places[peg_from])      # arm goes up
arm.set_Current_Pos(top_places[peg_to])
arm.set_Current_Pos(place_to)      # arm goes down
gripper.release()
arm.get_sent_pos(home)