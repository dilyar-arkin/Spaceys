#Regulating the temperature with PID- control algorithm
#pid = PIDController(Kp=1.0, Ki=0.1, Kd=0.01, setpoint=desired_temperature)
#Kp = proportional gain, Ki = integral gain, Kd = derivative gain, de/dt

class PID_Controller:
    def __init__(self, Kp, Ki, Kd, setpoint):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.setpoint = setpoint
        self.previous_error = 0
        self.integral = 0

    def calculate(self, temperature):
        error = self.setpoint - temperature
        self.integral += error
        derivative = error - self.previous_error
        output = self.Kp * error + self.Ki * self.integral + self.Kd * derivative
        self.previous_error = error
        return output
