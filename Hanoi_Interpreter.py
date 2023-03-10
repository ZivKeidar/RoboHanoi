import cv2
import numpy as np
import matplotlib.pyplot as plt

DISK_COLORS = {'disk1': 'yellow',
               'disk2': 'orange',
               'disk3': 'green'}

COLORS = {'green': [98, 155, 75],
          'orange': [108, 158, 255],
          'yellow': [119, 214, 253]}


CONV_SIZE = (5,10)

MEAN_KERNEL = np.ones(CONV_SIZE) / (CONV_SIZE[0]*CONV_SIZE[1])

THRESH_PEG_X = 80

class HanoiInterpreter:
    def __init__(self, image: np.ndarray, pegs_x, y_range):
        self.image = image
        self.pegs_x = pegs_x
        self.y_range = y_range
        self.state_map = self.extract_state(self.image)
        #print(self.state_map)
        #
        # plt.imshow(self.image)
        # plt.show()
        # plt.scatter([value[1] for value in self.state_dict.values()],
        #             [value[0] for value in self.state_dict.values()])
        # plt.show()
    def extract_state(self, image):
        mean_filter = cv2.filter2D(image, ddepth=-1, kernel=MEAN_KERNEL)
        disk_loactions = {disk: self.get_closest_idx(mean_filter, COLORS[DISK_COLORS[disk]]) for disk in DISK_COLORS.keys()}
        disk_location_y_sorted = {k: v for k, v in sorted(disk_loactions.items(), key=lambda item: item[1][0])}
        disks_on_pegs = {'peg1': [disk for disk in disk_location_y_sorted.keys() if np.abs(disk_loactions[disk][1]-self.pegs_x['peg1']) < THRESH_PEG_X][::-1],
                         'peg2': [disk for disk in disk_location_y_sorted.keys() if np.abs(disk_loactions[disk][1]-self.pegs_x['peg2']) < THRESH_PEG_X][::-1],
                         'peg3': [disk for disk in disk_location_y_sorted.keys() if np.abs(disk_loactions[disk][1]-self.pegs_x['peg3']) < THRESH_PEG_X][::-1]}

        state_map = {}
        for peg, disks in disks_on_pegs.items():
            if disks:
                state_map[disks[0]] = peg
                for i in range(1, len(disks)):
                    state_map[disks[i]] = disks[i-1]
        return state_map

    def get_closest_idx(self, filter, color):
        dists = np.sum(np.abs(filter - color), axis=-1)
        #need to do all combinations
        y = list(range(0, self.y_range['top'])) + list(range(self.y_range['bottom']+1, 480))
        x = list(range(0, self.pegs_x['peg1']-10))+list(range(self.pegs_x['peg1']+10, self.pegs_x['peg2']-10))+list(range(self.pegs_x['peg2']+11, self.pegs_x['peg3']-10))+list(range(self.pegs_x['peg3']+10, 640))
        len_y = len(y)
        len_x = len(x)
        y_plus = [[item]*len_x for item in y]
        y_plus = np.concatenate(y_plus)
        x_plus = np.array(x*len_y)
        y_2 = list(range(self.y_range['top']+1, self.y_range['bottom']))
        len_y_2 = len(y_2)
        y_2_plus = [[item] * len_x for item in y_2]
        y_2_plus = np.concatenate(y_2_plus)
        x_2_plus = np.array(x * len_y_2)


        dists[y_plus, x_plus] = 10000
        dists[y_2_plus, x_2_plus] = 10000
        min_indexes = np.where(dists == dists.min())
        return min_indexes[0][0], min_indexes[1][0]



if __name__ == '__main__':
    im = cv2.imread('hanoi1.png')
    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    HanoiInterpreter(im)
