import evdev
from evdev import InputDevice, categorize, ecodes

class PS4Controller:
    def __init__(self) -> None:     
        # Connect to the controller
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        for device in devices:
            if device.name == 'Wireless Controller':
                self.ps4 = InputDevice(device.fn)
                break

        # Print out device information
        print(self.ps4)
        self.left_x_value=0
        self.left_y_value=0
        self.right_x_value=0
        self.right_y_value=0
        
    def _map(self,x, in_min, in_max, out_min, out_max):
        """gets a number and maps it from one ragne to another range.

        Returns:
           float: the number in the new range
        """
        return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)    
    
    def get_Left_thumb(self) ->list:
        for event in self.ps4.read_loop():
            if event.type == evdev.ecodes.EV_ABS:
                if event.code == evdev.ecodes.ABS_X:
                    self.left_x_value = event.value
                if event.code == evdev.ecodes.ABS_Y:
                    self.left_y_value = event.value
            return [self._map(self.left_x_value,0,255,-100,100),self._map(self.left_y_value,255,0,-100,100)]
    
    def get_Right_thumb(self) ->list:
        for event in self.ps4.read_loop():
            if event.type == evdev.ecodes.EV_ABS:
                if event.code == evdev.ecodes.ABS_RX:
                    self.right_x_value = event.value
                if event.code == evdev.ecodes.ABS_RY:
                    self.right_y_value = event.value
            return [self._map(self.right_x_value,0,255,-100,100),self._map(self.right_y_value,255,0,-100,100)]
    
    def Tri(self):
        for event in self.ps4.read_loop():
            if event.type == evdev.ecodes.EV_KEY:
                if event.code == evdev.ecodes.BTN_WEST:
                    return event.value#1-pressed,0-released
                
    def Square(self):
        for event in self.ps4.read_loop():
            if event.type == evdev.ecodes.EV_KEY:
                if event.code == evdev.ecodes.BTN_NORTH:
                    return event.value#1-pressed,0-released
                     
    def X(self):
        for event in self.ps4.read_loop():
            if event.type == evdev.ecodes.EV_KEY:
                if event.code == evdev.ecodes.BTN_SOUTH:
                    return event.value#1-pressed,0-released
                  
    def Circle(self):
        for event in self.ps4.read_loop():
            if event.type == evdev.ecodes.EV_KEY:
                if event.code == evdev.ecodes.BTN_EAST:
                    return event.value#1-pressed,0-released
    def R1(self):
        for event in self.ps4.read_loop():
            if event.type == evdev.ecodes.EV_KEY:
               if event.code == evdev.ecodes.BTN_TR:
                    return event.value#1-pressed,0-released
    def R2(self):
        for event in self.ps4.read_loop():
            if event.type == evdev.ecodes.EV_KEY:
               if event.code == evdev.ecodes.BTN_TR2:
                    return event.value#1-pressed,0-released
    def L1(self):
        for event in self.ps4.read_loop():
            if event.type == evdev.ecodes.EV_KEY:
                if event.code == evdev.ecodes.BTN_TL:
                    return event.value#1-pressed,0-released
    def L2(self):
        for event in self.ps4.read_loop():
            if event.type == evdev.ecodes.EV_KEY:
                if event.code == evdev.ecodes.BTN_TL2:
                    return event.value#1-pressed,0-released
    def options(self):
        for event in self.ps4.read_loop():
            if event.type == evdev.ecodes.EV_KEY:
                if event.code == evdev.ecodes.BTN_START:
                    return event.value#1-pressed,0-released
    def share(self):
        for event in self.ps4.read_loop():
            if event.type == evdev.ecodes.EV_KEY:
                if event.code == evdev.ecodes.BTN_SELECT:
                    return event.value#1-pressed,0-released
    def ThumbR(self):
        for event in self.ps4.read_loop():
            if event.type == evdev.ecodes.EV_KEY:
                if event.code == evdev.ecodes.BTN_THUMBR:
                    return event.value#1-pressed,0-released
    def ThumbL(self):
        for event in self.ps4.read_loop():
            if event.type == evdev.ecodes.EV_KEY:
                if event.code == evdev.ecodes.BTN_THUMBL:
                    return event.value#1-pressed,0-released
    def UP(self):
        for event in self.ps4.read_loop():
            if event.type == evdev.ecodes.EV_KEY:
                if event.code == evdev.ecodes.BTN_DPAD_UP:
                    return event.value#1-pressed,0-released
    def DOWN(self):
        for event in self.ps4.read_loop():
            if event.type == evdev.ecodes.EV_KEY:
                if event.code == evdev.ecodes.BTN_DPAD_DOWN:
                    return event.value#1-pressed,0-released
    def LEFT(self):
        for event in self.ps4.read_loop():
            if event.type == evdev.ecodes.EV_KEY:
                if event.code == evdev.ecodes.BTN_DPAD_LEFT:
                    return event.value#1-pressed,0-released
                
    def RIGHT(self):
        for event in self.ps4.read_loop():
            if event.type == evdev.ecodes.EV_KEY:
                if event.code == evdev.ecodes.BTN_DPAD_RIGHT:
                    return event.value#1-pressed,0-released
    def kill(self):
        for event in self.ps4.read_loop():
            if event.type == evdev.ecodes.EV_KEY:
                if event.code == evdev.ecodes.BTN_MODE:
                    return event.value#1-pressed,0-released
        


