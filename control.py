from motor5a import Lmotor, Rmotor

class controller():

    def __init__(self):
        self.motorL = Lmotor(17)
        self.motorR = Rmotor(18) 
    
    def move():
        self.motorL.run(10)
        self.motorR.run(10)

    def turn_left():
        self.motorL.run(-6)
        self.motorR.run(6)

    def turn_right():
        self.motorL.run(6)
        self.motorR.run(-6)

    def stop():
        self.motorL.stop()
        self.motorR.stop()