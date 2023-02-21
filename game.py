#Import all the necessary libraries
import os.path
from tkinter import *
from PIL import Image
from PIL import ImageTk as itk, ImageTk
import numpy as np
from Hanoi_Interpreter import HanoiInterpreter
import cv2

pegs_x = {'peg1': 110,
          'peg2': 320,
          'peg3': 510}

y_range = {'top': 170,
           'bottom': 350}


class Game:
   def __init__(self):
      self.vc = cv2.VideoCapture(1)
      #Define the tkinter instance
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
      button = Button(self.win, image=click_btn, command=self.click_command, borderwidth=0)
      button.pack(pady=30)


      self.text.pack(pady=0)
      self.win.mainloop()


   def click_command(self):
      self.text.config(text=f"{self.turn} Turn!\n Identified tate:")
      self.i += 1
      current_state = self.identify_state()
      width = 489
      height = 204
      state = dict(sorted(current_state.items()))
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
         self.finisher = "Human's" if self.turn == "Robot's" else "Robot's"
         self.finish()
      self.turn = "Human's" if self.turn == "Robot's" else "Robot's"


   def identify_state(self):
      if self.vc.isOpened():  # try to get the first frame
         rval, frame = self.vc.read()
      else:
         print("Problem occurred while reading frame from webcam")

      state = HanoiInterpreter(frame, pegs_x, y_range).state_map

      # self.vc.release()
      return state

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