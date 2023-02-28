import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QSlider, QLineEdit, QTextEdit
from PyQt5.QtCore import Qt, QTimer
import qdarkstyle

class ArmControlGUI(QWidget):
    def __init__(self):
        super().__init__()
       
        self.initUI()

    def initUI(self):
        self.setWindowTitle("6-DOF Arm Control")

    
        motor1_label = QLabel("Motor 1:")
        self.motor1_slider = QSlider(Qt.Horizontal)
        self.motor1_slider.setMinimum(-180)
        self.motor1_slider.setMaximum(180)
        self.motor1_slider.setTickInterval(10)
        self.motor1_slider.setTickPosition(QSlider.TicksBelow)
        self.motor1_angle = QLabel("0")
        
        motor2_label = QLabel("Motor 2:")
        self.motor2_slider = QSlider(Qt.Horizontal)
        self.motor2_slider.setMinimum(-180)
        self.motor2_slider.setMaximum(180)
        self.motor2_slider.setTickInterval(10)
        self.motor2_slider.setTickPosition(QSlider.TicksBelow)
        self.motor2_angle = QLabel("0")
        
        motor3_label = QLabel("Motor 3:")
        self.motor3_slider = QSlider(Qt.Horizontal)
        self.motor3_slider.setMinimum(-180)
        self.motor3_slider.setMaximum(180)
        self.motor3_slider.setTickInterval(10)
        self.motor3_slider.setTickPosition(QSlider.TicksBelow)
        self.motor3_angle = QLabel("0")
        
        motor4_label = QLabel("Motor 4:")
        self.motor4_slider = QSlider(Qt.Horizontal)
        self.motor4_slider.setMinimum(-180)
        self.motor4_slider.setMaximum(180)
        self.motor4_slider.setTickInterval(10)
        self.motor4_slider.setTickPosition(QSlider.TicksBelow)
        self.motor4_angle = QLabel("0")
        
        motor5_label = QLabel("Motor 5:")
        self.motor5_slider = QSlider(Qt.Horizontal)
        self.motor5_slider.setMinimum(-180)
        self.motor5_slider.setMaximum(180)
        self.motor5_slider.setTickInterval(10)
        self.motor5_slider.setTickPosition(QSlider.TicksBelow)
        self.motor5_angle = QLabel("0")
        
        motor6_label = QLabel("Motor 6:")
        self.motor6_slider = QSlider(Qt.Horizontal)
        self.motor6_slider.setMinimum(-180)
        self.motor6_slider.setMaximum(180)
        self.motor6_slider.setTickInterval(10)
        self.motor6_slider.setTickPosition(QSlider.TicksBelow)
        self.motor6_angle = QLabel("0")
        
        self.motor1_slider.valueChanged.connect(self.update_motor1_angle)
        self.motor2_slider.valueChanged.connect(self.update_motor2_angle)
        self.motor3_slider.valueChanged.connect(self.update_motor3_angle)
        self.motor4_slider.valueChanged.connect(self.update_motor4_angle)
        self.motor5_slider.valueChanged.connect(self.update_motor5_angle)
        self.motor6_slider.valueChanged.connect(self.update_motor6_angle)
        
        get_button = QPushButton("Get Position")
        get_button.clicked.connect(self.get_position)
        set_button = QPushButton("Set")
        set_button.clicked.connect(self.set_arm)
        
        x_label = QLabel("X:")
        self.x_input = QLineEdit()
        y_label = QLabel("Y:")
        self.y_input = QLineEdit()
        z_label = QLabel("Z:")
        self.z_input = QLineEdit()
        get_ik_button = QPushButton("Get IK")
        get_ik_button.clicked.connect(self.get_ik)
        set_ik_button = QPushButton("Set IK")
        set_ik_button.clicked.connect(self.set_ik)
        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self.clear_log)
        
        self.message_log = QTextEdit()
        self.message_log.setReadOnly(True)
        self.message_log.append("Welcome to the 6-DOF Arm Control")
        
        hbox1 = QHBoxLayout()
        hbox1.addWidget(motor1_label)
        hbox1.addWidget(self.motor1_slider)
        hbox1.addWidget(self.motor1_angle)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(motor2_label)
        hbox2.addWidget(self.motor2_slider)
        hbox2.addWidget(self.motor2_angle)

        hbox3 = QHBoxLayout()
        hbox3.addWidget(motor3_label)
        hbox3.addWidget(self.motor3_slider)
        hbox3.addWidget(self.motor3_angle)

        hbox4 = QHBoxLayout()
        hbox4.addWidget(motor4_label)
        hbox4.addWidget(self.motor4_slider)
        hbox4.addWidget(self.motor4_angle)

        hbox5 = QHBoxLayout()
        hbox5.addWidget(motor5_label)
        hbox5.addWidget(self.motor5_slider)
        hbox5.addWidget(self.motor5_angle)

        hbox6 = QHBoxLayout()
        hbox6.addWidget(motor6_label)
        hbox6.addWidget(self.motor6_slider)
        hbox6.addWidget(self.motor6_angle)

        hbox7 = QHBoxLayout()
        hbox7.addWidget(get_button)
        hbox7.addWidget(set_button)

        hbox8 = QHBoxLayout()
        hbox8.addWidget(x_label)
        hbox8.addWidget(self.x_input)
        hbox8.addWidget(y_label)
        hbox8.addWidget(self.y_input)
        hbox8.addWidget(z_label)
        hbox8.addWidget(self.z_input)
        hbox8.addWidget(get_ik_button)
        hbox8.addWidget(set_ik_button)
        hbox8.addWidget(clear_button)
        
        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)
        vbox.addLayout(hbox5)
        vbox.addLayout(hbox6)
        vbox.addLayout(hbox7)
        vbox.addLayout(hbox8)
        vbox.addWidget(self.message_log)
        self.setLayout(vbox)


    def get_position(self):
        # Get current angles from robot arm here
        self.motor1_angle.setText(str(self.motor1_slider.value()))
        self.motor2_angle.setText(str(self.motor2_slider.value()))
        self.motor3_angle.setText(str(self.motor3_slider.value()))
        self.motor4_angle.setText(str(self.motor4_slider.value()))
        self.motor5_angle.setText(str(self.motor5_slider.value()))
        self.motor6_angle.setText(str(self.motor6_slider.value()))
        self.message_log.append("Current position retrieved.")
        self.message_log.append(self.motor1_angle.text()+","+self.motor2_angle.text()+","+self.motor3_angle.text()+","+self.motor4_angle.text()+","+self.motor5_angle.text()+","+self.motor6_angle.text())

    def set_arm(self):
        # Send angles from sliders to robot arm here
        self.message_log.append("Setting arm position...")
        self.message_log.append(self.motor1_angle.text()+","+self.motor2_angle.text()+","+self.motor3_angle.text()+","+self.motor4_angle.text()+","+self.motor5_angle.text()+","+self.motor6_angle.text())

        pass

    def get_ik(self):
        # Get inverse kinematics solution here
        x = self.x_input.text()
        y = self.y_input.text()
        z = self.z_input.text()
        self.message_log.append(f"Getting IK solution for x:{x}, y:{y}, z:{z}")
        
        pass

    def set_ik(self):
        # Send inverse kinematics solution to robot arm here
        x = self.x_input.text()
        y = self.y_input.text()
        z = self.z_input.text()
        self.message_log.append("Setting arm position using IK...")
        self.message_log.append(f"Setting arm position using IK for x:{x}, y:{y}, z:{z}")

        pass

    def clear_log(self):
        self.message_log.clear()
        
    def update_motor1_angle(self, angle):
        self.motor1_angle.setText(str(angle))

    def update_motor2_angle(self, angle):
        self.motor2_angle.setText(str(angle))
        
    def update_motor3_angle(self, angle):
        self.motor3_angle.setText(str(angle))

    def update_motor4_angle(self, angle):
        self.motor4_angle.setText(str(angle))
        
    def update_motor5_angle(self, angle):
        self.motor5_angle.setText(str(angle))

    def update_motor6_angle(self, angle):
        self.motor6_angle.setText(str(angle))
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    ex = ArmControlGUI()
    ex.show()
    sys.exit(app.exec_())


