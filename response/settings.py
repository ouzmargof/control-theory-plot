class Settings:
    def __init__(self):
        self.settings = {
            'step': {
                'Default': True,
                'TimeMax': 10.0,
                'Step': 0.1
            },
            'bode': {
                'Default': True,
                'FreqMin': 0.10,
                'FreqMax': 10.0,
            },
            'rlocus':{
                'Default': True,
                'zeta': 0.7,
                'omega': 1,
                'xmin': -1,
                'xmax': 1,
                'ymin': -1,
                'ymax': 1
            },
            'nyquist':{
                'Default': True,
                'xmin': -2,
                'xmax': 2,
                'ymin': -2,
                'ymax': 2
            }
        }


    def is_step_default(self):
        return self.settings['step']['Default']
    def set_step_default(self, value):
        self.settings['step']['Default'] = value
    def get_step_time_max(self):
        return self.settings['step']['TimeMax']
    def set_step_time_max(self, value):
        self.settings['step']['TimeMax'] = value
    def get_step_step(self):
        return self.settings['step']['Step']
    def set_step_step(self, value):
        self.settings['step']['Step'] = value


    def is_bode_default(self):
        return self.settings['bode']['Default']
    def set_bode_default(self, value):
        self.settings['bode']['Default'] = value
    def get_bode_freq_min(self):
        return self.settings['bode']['FreqMin']
    def set_bode_freq_min(self, value):
        self.settings['bode']['FreqMin'] = value
    def get_bode_freq_max(self):
        return self.settings['bode']['FreqMax']
    def set_bode_freq_max(self, value):
        self.settings['bode']['FreqMax'] = value


    def is_rlocus_default(self):
        return self.settings['rlocus']['Default']
    def set_rlocus_default(self, value):
        self.settings['rlocus']['Default'] = value
    def get_rlocus_zeta(self):
        return self.settings['rlocus']['zeta']
    def set_rlocus_zeta(self, value):
        self.settings['rlocus']['zeta'] = value
    def get_rlocus_omega(self):
        return self.settings['rlocus']['omega']
    def set_rlocus_omega(self, value):
        self.settings['rlocus']['omega'] = value
    def get_rlocus_xmin(self):
        return self.settings['rlocus']['xmin']
    def set_rlocus_xmin(self, value):
        self.settings['rlocus']['xmin'] = value
    def get_rlocus_xmax(self):
        return self.settings['rlocus']['xmax']
    def set_rlocus_xmax(self, value):
        self.settings['rlocus']['xmax'] = value
    def get_rlocus_ymin(self):
        return self.settings['rlocus']['ymin']
    def set_rlocus_ymin(self, value):
        self.settings['rlocus']['ymin'] = value
    def get_rlocus_ymax(self):
        return self.settings['rlocus']['ymax']
    def set_rlocus_ymax(self, value):
        self.settings['rlocus']['ymax'] = value

    
    def is_nyquist_default(self):
        return self.settings['nyquist']['Default']
    def set_nyquist_default(self, value):
        self.settings['nyquist']['Default'] = value
    def get_nyquist_xmin(self):
        return self.settings['nyquist']['xmin']
    def set_nyquist_xmin(self, value):
        self.settings['nyquist']['xmin'] = value
    def get_nyquist_xmax(self):
        return self.settings['nyquist']['xmax']
    def set_nyquist_xmax(self, value):
        self.settings['nyquist']['xmax'] = value
    def get_nyquist_ymin(self):
        return self.settings['nyquist']['ymin']
    def set_nyquist_ymin(self, value):
        self.settings['nyquist']['ymin'] = value
    def get_nyquist_ymax(self):
        return self.settings['nyquist']['ymax']
    def set_nyquist_ymax(self, value):
        self.settings['nyquist']['ymax'] = value