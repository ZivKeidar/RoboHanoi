#Import all the necessary libraries
import os.path
from tkinter import *
from PIL import Image
from PIL import ImageTk as itk, ImageTk
import numpy as np
from Hanoi import Hanoi
from Hanoi_Interpreter import HanoiInterpreter
from BEN import Execution
import cv2
from threading import Thread
import BEN

pegs_x = {'peg1': 110,
          'peg2': 320,
          'peg3': 510}

y_range = {'top': 170,
           'bottom': 350}

pegs_x = {'peg1': 150,
          'peg2': 260,
          'peg3': 420}
y_range = {'top': 120,
           'bottom': 280}

CURRENT_STATE = {}

def webcam():
   cv2.namedWindow("Hanoi")
   vc = cv2.VideoCapture(4)
   if vc.isOpened(): # try to get the first frame
      rval, frame = vc.read()
   else:
      rval = False

   while rval:
      state = HanoiInterpreter(frame, pegs_x, y_range).state_map
      for k, v in state.items():
         CURRENT_STATE[k] = v
      frame = cv2.putText(frame, str(state), (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
      frame = cv2.rectangle(frame, (pegs_x['peg1']-10, y_range['top']), (pegs_x['peg1']+10, y_range['bottom']), (255, 0, 0), 2)
      frame = cv2.rectangle(frame, (pegs_x['peg2']-10, y_range['top']), (pegs_x['peg2']+10, y_range['bottom']), (255, 0, 0), 2)
      frame = cv2.rectangle(frame, (pegs_x['peg3']-10, y_range['top']), (pegs_x['peg3']+10, y_range['bottom']), (255, 0, 0), 2)
      cv2.imshow('Hanoi', frame)
      rval, frame = vc.read()
      key = cv2.waitKey(20)
      if key == 27: # exit on ESC
         break

   vc.release()
   cv2.destroyWindow("preview")
      


def translate_plan(plan, state):
   new_plan = ""
   plan = str(plan)
   for action in plan.split('),'):
      cur_disk = action[action.index('disk'):action.index('disk') + 5]
      if 'moveDiskToPeg' in action:
         on = action[action.index('disk') + 7:action.index('disk') + 12]
         to = action[action.index('peg'):action.index('peg') + 4]
         if state[on].startswith('peg'):
            new_action = f"(move {cur_disk} {state[on]} {to})-"
            new_plan += new_action
         else:
            new_action = f"(move {cur_disk} {state[state[on]]} {action[action.index('peg'):action.index('peg') + 4]})-"
            new_plan += new_action
      elif 'moveDiskToDisk' in action:
         on = action[action.index('disk') + 7:action.index('disk') + 12]
         to = action[action.index('disk') + 14:action.index('disk') + 19]
         new_action = f"(move {cur_disk} {state[on]} {state[to]})-"
         new_plan += new_action
      elif 'movePegToDisk' in action:
         on = action[action.index('peg'):action.index('peg') + 4]
         to = action[action.index('disk') + 13:action.index('disk') + 18]
         if state[to].startswith('peg'):
            new_action = f"(move {cur_disk} {on} {state[to]})-"
            new_plan += new_action
         else:
            new_action = f"(move {cur_disk} {on} {state[state[to]]})-"
            new_plan += new_action
      elif 'movePegToPeg' in action:
         on = action[action.index('peg'):action.index('peg') + 4]
         to = action[action.index('peg') + 6:action.index('peg') + 10]
         new_action = f"(move {cur_disk} {on} {to})-"
         new_plan += new_action
      state[cur_disk] = to
   return new_plan

def perform_planning(state):
   current_plan = Hanoi(state).hanoi_plan
   current_plan = translate_plan(current_plan, state.copy())
   execution = Execution(current_plan, state)
   execution.execute_next()


class Game:
   def __init__(self):
      self.player_2 = "Human's"
      # self.vc = cv2.VideoCapture(4)
      thread = Thread(target=webcam)
      thread.start()
      self.turn = "Robot's"
      self.win = Toplevel()
      self.win.title("Click The Jedi to change Turns")
      self.started = False
      #Define the size of the tkinter frame
      self.win.geometry("700x900")
      #Define the working of the button
      self.i = 0
      #Import the image using PhotoImage function
      im = Image.open("jedi.jpg")
      im = im.resize((int(im.size[0]*0.5), int(im.size[1]*0.5)))
      click_btn = itk.PhotoImage(im)
      #Let us create a label for button event
      img_label = Label(image=click_btn)
      self.text = Label(self.win, text="Click The Jedi to Start or Switch Turns ", font=("Arial", 20))
      button = Button(self.win, image=click_btn, command=lambda: self.click_command(), borderwidth=0)
      button.pack(pady=30)
      self.text.pack(pady=0)
      self.win.mainloop()

   def planning(self):
      if self.turn == "Robot's":
         current_plan = Hanoi(self.current_state).hanoi_plan
         self.current_plan = self.translate_plan(current_plan, self.current_state.copy())
         execution = Execution(self.current_plan, self.current_state)
         execution.execute_next()

   def click_command(self):
      self.text.config(text=f"{self.turn} Turn!\n Identified State:")
      self.i += 1
      self.current_state = self.identify_state()
      width = 489
      height = 204
      state = dict(sorted(self.current_state.items()))
      state = str(state).replace(':', '')
      image_path = os.path.join('state_images', state+'.png')
      image = Image.open(image_path)
      image = image.resize((width, height))
      self.state_image = ImageTk.PhotoImage(image)

      if not self.started:
         self.initimg = Label(self.win, image=self.state_image)
         self.initimg.image = self.state_image
         self.initimg.pack()
         self.started = True
      else:
         self.initimg.configure(image=self.state_image)
         self.initimg.image = self.state_image
      if state == "{'disk1' 'disk2', 'disk2' 'disk3', 'disk3' 'peg3'}":
         self.finisher = self.player_2 if self.turn == "Robot's" else "Robot's"
         self.finish()
      if self.turn == "Robot's":
         thread = Thread(target=perform_planning, args=(self.current_state,))
         thread.start()
      self.turn = self.player_2 if self.turn == "Robot's" else "Robot's"

   def translate_plan(self, plan, state):
      new_plan = ""
      plan = str(plan)
      for action in plan.split('),'):
         cur_disk = action[action.index('disk'):action.index('disk')+5]
         if 'moveDiskToPeg' in action:
            on = action[action.index('disk')+7:action.index('disk')+12]
            to = action[action.index('peg'):action.index('peg')+4]
            if state[on].startswith('peg'):
               new_action = f"(move {cur_disk} {state[on]} {to})-"
               new_plan += new_action
            else:
               new_action = f"(move {cur_disk} {state[state[on]]} {action[action.index('peg'):action.index('peg') + 4]})-"
               new_plan += new_action
         elif 'moveDiskToDisk' in action:
            on = action[action.index('disk') + 7:action.index('disk') + 12]
            to = action[action.index('disk') + 14:action.index('disk') + 19]
            new_action = f"(move {cur_disk} {state[on]} {state[to]})-"
            new_plan += new_action
         elif 'movePegToDisk' in action:
            on = action[action.index('peg'):action.index('peg') + 4]
            to = action[action.index('disk') + 13:action.index('disk') + 18]
            if state[to].startswith('peg'):
               new_action = f"(move {cur_disk} {on} {state[to]})-"
               new_plan += new_action
            else:
               new_action = f"(move {cur_disk} {on} {state[state[to]]})-"
               new_plan += new_action
         elif 'movePegToPeg' in action:
            on = action[action.index('peg'):action.index('peg') + 4]
            to = action[action.index('peg') + 6:action.index('peg') + 10]
            new_action = f"(move {cur_disk} {on} {to})-"
            new_plan += new_action
         state[cur_disk] = to
      return new_plan


   def identify_state(self):
      # if self.vc.isOpened():  # try to get the first frame
      #    rval, frame = self.vc.read()
      # else:
      #    print("Problem occurred while reading frame from webcam")
      # state = HanoiInterpreter(frame, pegs_x, y_range).state_map
      # # self.vc.release()
      # return state
      return CURRENT_STATE
      
   def finish(self):
      # root = Tk()
      # print(os.listdir())
      self.text.config(text=f" The {self.finisher[:-2]} Has Finished The Game!\n Identified State:")
      frameCnt = 25
      frames = [PhotoImage(file='gif.gif', format='gif -index %i' % (i)) for i in range(frameCnt)]

      def update(ind):
         frame = frames[ind]
         ind += 1
         if ind == frameCnt:
            ind = 0
         label.configure(image=frame)
         self.win.after(25, update, ind)

      label = Label(self.win)
      label.pack()
      self.win.after(0, update, 0)

if __name__ == '__main__':
   Game()