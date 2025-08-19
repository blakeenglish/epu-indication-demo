class Engine:
    def __init__(self, name, power=0.0, temp=20.0, heat_gen_coeff=1.0, heat_rej_coeff=0.1):
        self.name = name
        self.power = power  # 0.0 to 1.0
        self.temp = temp
        self.heat_gen_coeff = heat_gen_coeff
        self.heat_rej_coeff = heat_rej_coeff
        self.temperature_upper_redline = 100.0
        self.temperature_lower_redline = 0
        self.temperature_inverter_60 = 50.0

    def update(self, outside_temp, dt=1.0):
        # Heat generated is proportional to power
        heat_generated = self.heat_gen_coeff * self.power
        # Heat rejected is proportional to (engine temp - outside temp)
        heat_rejected = self.heat_rej_coeff * (self.temp - outside_temp)
        # Update engine temperature
        self.temp += (heat_generated - heat_rejected) * dt

    def set_power(self, power):
        self.power = max(0.0, min(1.0, power))
