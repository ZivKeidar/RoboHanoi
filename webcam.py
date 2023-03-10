import cv2
import matplotlib.pyplot as plt
from Hanoi_Interpreter import HanoiInterpreter
# pegs_x = {'peg1': 110,
#           'peg2': 320,
#           'peg3': 510}
pegs_x = {'peg1': 150,
          'peg2': 260,
          'peg3': 420}
y_range = {'top': 120,
           'bottom': 280}



cv2.namedWindow("preview")
vc = cv2.VideoCapture(4)

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:
    state = HanoiInterpreter(frame, pegs_x, y_range).state_map
    frame = cv2.putText(frame, str(state), (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
    frame = cv2.rectangle(frame, (pegs_x['peg1']-10, y_range['top']), (pegs_x['peg1']+10, y_range['bottom']), (255, 0, 0), 2)
    frame = cv2.rectangle(frame, (pegs_x['peg2']-10, y_range['top']), (pegs_x['peg2']+10, y_range['bottom']), (255, 0, 0), 2)
    frame = cv2.rectangle(frame, (pegs_x['peg3']-10, y_range['top']), (pegs_x['peg3']+10, y_range['bottom']), (255, 0, 0), 2)
    cv2.imshow('preview', frame)
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break

vc.release()
cv2.destroyWindow("preview")