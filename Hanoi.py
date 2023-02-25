from unified_planning.shortcuts import *
from unified_planning.io import PDDLWriter
import time

class Hanoi:
    def __init__(self, state_map: dict):
        self.state_map = state_map
        self.hanoi_plan = self.plan()

    def plan(self):
        # Objects
        Peg = UserType("Peg")
        Disk = UserType("Disk")
        # Fluents
        OnDisk = Fluent("OnDisk", BoolType(), up_disk=Disk, down_disk=Disk)
        OnPeg = Fluent("OnPeg", BoolType(), disk=Disk, peg=Peg)
        FreeDisk = Fluent("FreeDisk", BoolType(), disk=Disk)
        FreePeg = Fluent("FreePeg", BoolType(), peg=Peg)
        Bigger = Fluent("Bigger", BoolType(), bigDisk=Disk, smallDisk=Disk)
        # Actions
        movePegToPeg = InstantaneousAction("movePegToPeg", d=Disk, p_from=Peg, p_to=Peg)
        d = movePegToPeg.parameter("d")
        p_from = movePegToPeg.parameter("p_from")
        p_to = movePegToPeg.parameter("p_to")
        movePegToPeg.add_precondition(FreeDisk(d))
        movePegToPeg.add_precondition(OnPeg(d, p_from))
        movePegToPeg.add_precondition(FreePeg(p_to))
        movePegToPeg.add_effect(OnPeg(d, p_to), True)
        movePegToPeg.add_effect(OnPeg(d, p_from), False)
        movePegToPeg.add_effect(FreePeg(p_from), True)
        movePegToPeg.add_effect(FreePeg(p_to), False)

        movePegToDisk = InstantaneousAction("movePegToDisk", d=Disk, p_from=Peg, d_to=Disk)
        d = movePegToDisk.parameter("d")
        p_from = movePegToDisk.parameter("p_from")
        d_to = movePegToDisk.parameter("d_to")
        movePegToDisk.add_precondition(FreeDisk(d))
        movePegToDisk.add_precondition(OnPeg(d, p_from))
        movePegToDisk.add_precondition(FreeDisk(d_to))
        movePegToDisk.add_precondition(Bigger(d_to, d))
        movePegToDisk.add_effect(OnDisk(d, d_to), True)
        movePegToDisk.add_effect(OnPeg(d, p_from), False)
        movePegToDisk.add_effect(FreePeg(p_from), True)
        movePegToDisk.add_effect(FreeDisk(d_to), False)

        moveDiskToPeg = InstantaneousAction("moveDiskToPeg", d=Disk, d_from=Disk, p_to=Peg)
        d = moveDiskToPeg.parameter("d")
        d_from = moveDiskToPeg.parameter("d_from")
        p_to = moveDiskToPeg.parameter("p_to")
        moveDiskToPeg.add_precondition(FreeDisk(d))
        moveDiskToPeg.add_precondition(OnDisk(d, d_from))
        moveDiskToPeg.add_precondition(FreePeg(p_to))
        moveDiskToPeg.add_effect(OnPeg(d, p_to), True)
        moveDiskToPeg.add_effect(OnDisk(d, d_from), False)
        moveDiskToPeg.add_effect(FreeDisk(d_from), True)
        moveDiskToPeg.add_effect(FreePeg(p_to), False)

        moveDiskToDisk = InstantaneousAction("moveDiskToDisk", d=Disk, d_from=Disk, d_to=Disk)
        d = moveDiskToDisk.parameter("d")
        d_from = moveDiskToDisk.parameter("d_from")
        d_to = moveDiskToDisk.parameter("d_to")
        moveDiskToDisk.add_precondition(FreeDisk(d))
        moveDiskToDisk.add_precondition(OnDisk(d, d_from))
        moveDiskToDisk.add_precondition(FreeDisk(d_to))
        moveDiskToDisk.add_precondition(Bigger(d_to, d))
        moveDiskToDisk.add_effect(OnDisk(d, d_to), True)
        moveDiskToDisk.add_effect(OnDisk(d, d_from), False)
        moveDiskToDisk.add_effect(FreeDisk(d_from), True)
        moveDiskToDisk.add_effect(FreeDisk(d_to), False)

        # Problem definition
        # Objects
        problem_hanoi = Problem("hanoi")
        pegs = [Object(f"peg{i}", Peg) for i in range(1, 4)]
        disks = [Object(f"disk{i}", Disk) for i in range(1, len(self.state_map.keys())+1)]
        problem_hanoi.add_objects(pegs+disks)

        # Fluents
        problem_hanoi.add_fluent(OnDisk, default_initial_value=False)
        problem_hanoi.add_fluent(OnPeg, default_initial_value=False)
        problem_hanoi.add_fluent(FreeDisk, default_initial_value=False)
        problem_hanoi.add_fluent(FreePeg, default_initial_value=False)
        problem_hanoi.add_fluent(Bigger, default_initial_value=False)

        # Actions
        problem_hanoi.add_action(movePegToPeg)
        problem_hanoi.add_action(movePegToDisk)
        problem_hanoi.add_action(moveDiskToPeg)
        problem_hanoi.add_action(moveDiskToDisk)

        # Initial values
        non_free_disks = []
        non_free_pegs = []
        # setting positions
        for k, v in self.state_map.items():
            top = disks[int(k[4])-1]
            bottom = disks[int(v[4])-1] if v.startswith('disk') else pegs[int(v[3])-1]
            if v.startswith('disk'):
                problem_hanoi.set_initial_value(OnDisk(top, bottom), True)
                non_free_disks.append(int(v[4])-1)
            else:
                problem_hanoi.set_initial_value(OnPeg(top, bottom), True)
                non_free_pegs.append(int(v[3]) - 1)
        # setting free object
        for i in range(len(disks)):
            if i not in non_free_disks:
                problem_hanoi.set_initial_value(FreeDisk(disks[i]), True)
        for i in range(len(pegs)):
            if i not in non_free_pegs:
                problem_hanoi.set_initial_value(FreePeg(pegs[i]), True)
        # setting disk size order
        for i in range(1, len(disks)):
            for j in range(i):
                problem_hanoi.set_initial_value(Bigger(disks[i], disks[j]), True)

        # Goal
        for i in range(len(disks)-1):
            problem_hanoi.add_goal(OnDisk(disks[i], disks[i+1]))
        problem_hanoi.add_goal(OnPeg(disks[-1], pegs[-1]))

        # Writing the PDDl files
        w = PDDLWriter(problem_hanoi)
        w.write_domain('domain_upf_hanoi.pddl')
        w.write_problem('problem_upf_hanoi3.pddl')

        # Solving the problem
        FD_planner = OneshotPlanner(name='fast-downward')
        start_time = time.time()
        result_hanoi = FD_planner.solve(problem_hanoi)
        solve_time = time.time() - start_time
        plan_hanoi = result_hanoi.plan
        # print("The amazing plan for the Hanoi problem is: ", plan_hanoi)
        # print(f"It took the solver {solve_time} seconds to solve it")
        return plan_hanoi

if __name__ == '__main__':
    state_map = {'disk1': 'disk2',
                 'disk2': 'disk3',
                 'disk3': 'peg1'}
    Hanoi(state_map)

