from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import(
    QDialog, QDialogButtonBox,
    QVBoxLayout, QGridLayout, QFrame,
    QLabel, QDoubleSpinBox, QCheckBox, QLineEdit)


class ConfigZpk(QDialog):
    def __init__(self):
        super().__init__()
        self.setupUi()


    def setupUi(self):
        self.setWindowTitle("ZPK")
        self.label_infos = QLabel(
            "Values must be seperated by spaces.\n Complex form: -1-1j -1+1j"
            )
        self.label_zeros = QLabel("Zeros")       
        self.line_zeros = QLineEdit()
        self.label_poles = QLabel("Poles")
        self.line_poles = QLineEdit()
        self.label_gain = QLabel("Gain")
        self.line_gain = QLineEdit()
        
        self.grid = QGridLayout()
        self.grid.addWidget(self.label_infos, 0, 0, 1, 2)
        self.grid.addWidget(self.label_gain, 1, 0)
        self.grid.addWidget(self.line_gain, 1, 1)
        self.grid.addWidget(self.label_zeros, 2, 0)
        self.grid.addWidget(self.line_zeros, 2, 1)
        self.grid.addWidget(self.label_poles, 3, 0)
        self.grid.addWidget(self.line_poles, 3, 1)

        self.buttonBox = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        
        self.layout = QVBoxLayout()
        self.layout.addLayout(self.grid)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


    def value(self):
        gain = self.line_gain.text()
        zeros = self.line_zeros.text().split()
        poles = self.line_poles.text().split()
        return [zeros, poles, gain]


class ConfigResponseStep(QDialog):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.setupUi()
        
        self.widgets = [
            self.label_time, self.spinbox_time,
            self.label_step, self.spinbox_step
        ]
        # Run at launch
        self.populateWidgets()
        if self.settings.is_step_default():
            self.disableWidgets()
            self.radio_default.setChecked(True)

        # Slots
        self.radio_default.toggled.connect(self.onRadioDefaultToggle)
        self.accepted.connect(self.onAccpted)


    def setupUi(self):
        self.setWindowTitle("Step")

        self.radio_default = QCheckBox("Default values")

        self.label_time = QLabel("Time")
        self.spinbox_time = QDoubleSpinBox()

        self.label_step = QLabel("Step")
        self.spinbox_step = QDoubleSpinBox()
        self.spinbox_step.setRange(0.01, 1)
        self.spinbox_step.setSingleStep(0.01)

        self.grid = QGridLayout()
        self.grid.addWidget(self.radio_default, 0, 0)
        self.grid.addWidget(self.label_time, 1, 0)
        self.grid.addWidget(self.spinbox_time, 1, 1)
        self.grid.addWidget(self.label_step, 2, 0)
        self.grid.addWidget(self.spinbox_step, 2, 1)

        self.buttonBox = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        
        self.layout = QVBoxLayout()
        self.layout.addLayout(self.grid)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


    def populateWidgets(self):
        self.spinbox_time.setValue(self.settings.get_step_time_max())
        self.spinbox_step.setValue(self.settings.get_step_step())


    def disableWidgets(self):
        for w in self.widgets:
            w.setEnabled(False)


    def enableWidgets(self):
        for w in self.widgets:
            w.setEnabled(True)


    def onRadioDefaultToggle(self):        
        if self.radio_default.isChecked():
            self.settings.set_step_default(True)
            self.disableWidgets()
        else:
            self.settings.set_step_default(False)
            self.enableWidgets()


    def onAccpted(self):
        self.settings.set_step_time_max(self.spinbox_time.value())
        self.settings.set_step_step(self.spinbox_step.value())


class ConfigResponseRlocus(QDialog):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.setupUi()
        self.widgets = [
            self.label_zeta, self.spinbox_zeta,
            self.label_omega, self.spinbox_omega,
            self.label_xmin, self.spinbox_xmin,
            self.label_xmax, self.spinbox_xmax,
            self.label_ymin, self.spinbox_ymin,
            self.label_ymax, self.spinbox_ymax
        ]
        
        # Run at launch
        self.populateWidgets()
        if self.settings.is_rlocus_default():
            self.disableWidgets()
            self.radio_default.setChecked(True)

        # Slots
        self.radio_default.toggled.connect(self.onRadioDefaultToggle)
        self.accepted.connect(self.onAccpted)


    def setupUi(self):
        self.setWindowTitle("Root locus")

        self.radio_default = QCheckBox("Default values")

        self.label_zeta = QLabel("Damping ratio")
        self.spinbox_zeta = QDoubleSpinBox()
        self.spinbox_zeta.setRange(0, 1)
        self.spinbox_zeta.setSingleStep(0.1)

        self.label_omega = QLabel("Natural frequency")
        self.spinbox_omega = QDoubleSpinBox()
        self.spinbox_omega.setRange(0, 1000)
        self.spinbox_omega.setSingleStep(1)

        self.label_xmin = QLabel("xmin")
        self.spinbox_xmin = QDoubleSpinBox()
        self.spinbox_xmin.setRange(-100, 0)
        self.label_xmax = QLabel("xmax")
        self.spinbox_xmax = QDoubleSpinBox()
        self.spinbox_xmax.setRange(0, 100)
        self.label_ymin = QLabel("ymin")
        self.spinbox_ymin = QDoubleSpinBox()
        self.spinbox_ymin.setRange(-100, 0)
        self.label_ymax = QLabel("ymax")
        self.spinbox_ymax = QDoubleSpinBox()
        self.spinbox_ymax.setRange(0, 100)

        self.grid_u = QGridLayout()
        self.grid_u.addWidget(self.radio_default, 0, 0)
        self.grid_u.addWidget(self.label_zeta, 1, 0)
        self.grid_u.addWidget(self.spinbox_zeta, 1, 1)
        self.grid_u.addWidget(self.label_omega, 2, 0)
        self.grid_u.addWidget(self.spinbox_omega, 2, 1)

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setFrameShadow(QFrame.Sunken)

        self.grid_d = QGridLayout()
        self.grid_d.addWidget(self.label_xmin, 0, 0)
        self.grid_d.addWidget(self.spinbox_xmin, 0, 1)
        self.grid_d.addWidget(self.label_xmax, 0, 2)
        self.grid_d.addWidget(self.spinbox_xmax, 0, 3)
        self.grid_d.addWidget(self.label_ymin, 1, 0)
        self.grid_d.addWidget(self.spinbox_ymin, 1, 1)
        self.grid_d.addWidget(self.label_ymax, 1, 2)
        self.grid_d.addWidget(self.spinbox_ymax, 1, 3)

        self.buttonBox = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        
        self.layout = QVBoxLayout()
        self.layout.addLayout(self.grid_u)
        self.layout.addWidget(sep)
        self.layout.addLayout(self.grid_d)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


    def populateWidgets(self):
        self.spinbox_zeta.setValue(self.settings.get_rlocus_zeta())
        self.spinbox_omega.setValue(self.settings.get_rlocus_omega())
        self.spinbox_xmin.setValue(self.settings.get_rlocus_xmin())
        self.spinbox_xmax.setValue(self.settings.get_rlocus_xmax())
        self.spinbox_ymin.setValue(self.settings.get_rlocus_ymin())
        self.spinbox_ymax.setValue(self.settings.get_rlocus_ymax())
        

    def disableWidgets(self):
        for w in self.widgets:
            w.setEnabled(False)


    def enableWidgets(self):
        for w in self.widgets:
            w.setEnabled(True)


    def onRadioDefaultToggle(self):        
        if self.radio_default.isChecked():
            self.settings.set_rlocus_default(True)
            self.disableWidgets()
        else:
            self.settings.set_rlocus_default(False)
            self.enableWidgets()


    def onAccpted(self):
        self.settings.set_rlocus_zeta(self.spinbox_zeta.value())
        self.settings.set_rlocus_omega(self.spinbox_omega.value())
        self.settings.set_rlocus_xmin(self.spinbox_xmin.value())
        self.settings.set_rlocus_xmax(self.spinbox_xmax.value())
        self.settings.set_rlocus_ymin(self.spinbox_ymin.value())
        self.settings.set_rlocus_ymax(self.spinbox_ymax.value())


class ConfigResponseBode(QDialog):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.setupUi()
        
        self.widgets = [
            self.label_freq_min, self.spinbox_freq_min,
            self.label_freq_max, self.spinbox_freq_max
        ]

        # Run at launch
        self.populateWidgets()
        if self.settings.is_bode_default():
            self.disableWidgets()
            self.radio_default.setChecked(True)

        # Slots
        self.radio_default.toggled.connect(self.onRadioDefaultToggle)
        self.accepted.connect(self.onAccpted)


    def setupUi(self):
        self.setWindowTitle("Bode")

        self.radio_default = QCheckBox("Default values")

        self.label_freq_min = QLabel("Minimum Frequency")
        self.spinbox_freq_min = QDoubleSpinBoxLog()
        self.spinbox_freq_min.setMinimum(1e-2)
        self.spinbox_freq_min.setMaximum(1e5)

        self.label_freq_max = QLabel("Maximum Frequency")
        self.spinbox_freq_max = QDoubleSpinBoxLog()
        self.spinbox_freq_max.setMinimum(1e-1)
        self.spinbox_freq_max.setMaximum(1e6)

        self.grid = QGridLayout()
        self.grid.addWidget(self.radio_default, 0, 0)
        self.grid.addWidget(self.label_freq_min, 1, 0)
        self.grid.addWidget(self.spinbox_freq_min, 1, 1)
        self.grid.addWidget(self.label_freq_max, 2, 0)
        self.grid.addWidget(self.spinbox_freq_max, 2, 1)

        self.buttonBox = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        
        self.layout = QVBoxLayout()
        self.layout.addLayout(self.grid)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


    def populateWidgets(self):
        self.spinbox_freq_min.setValue(self.settings.get_bode_freq_min())
        self.spinbox_freq_max.setValue(self.settings.get_bode_freq_max())


    def disableWidgets(self):
        for w in self.widgets:
            w.setEnabled(False)


    def enableWidgets(self):
        for w in self.widgets:
            w.setEnabled(True)


    def onRadioDefaultToggle(self):        
        if self.radio_default.isChecked():
            self.settings.set_bode_default(True)
            self.disableWidgets()
        else:
            self.settings.set_bode_default(False)
            self.enableWidgets()

    
    def onAccpted(self):
        self.settings.set_bode_freq_min(self.spinbox_freq_min.value())
        self.settings.set_bode_freq_max(self.spinbox_freq_max.value())
            

class ConfigResponseNyquist(QDialog):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.setupUi()
        self.widgets = [
            self.label_xmin, self.spinbox_xmin,
            self.label_xmax, self.spinbox_xmax,
            self.label_ymin, self.spinbox_ymin,
            self.label_ymax, self.spinbox_ymax
        ]
        
        # Run at launch
        self.populateWidgets()
        if self.settings.is_nyquist_default():
            self.disableWidgets()
            self.radio_default.setChecked(True)

        # Slots
        self.radio_default.toggled.connect(self.onRadioDefaultToggle)
        self.accepted.connect(self.onAccpted)


    def setupUi(self):
        self.setWindowTitle("Root locus")

        self.radio_default = QCheckBox("Default values")

        self.label_xmin = QLabel("xmin")
        self.spinbox_xmin = QDoubleSpinBox()
        self.spinbox_xmin.setRange(-100, 0)
        self.label_xmax = QLabel("xmax")
        self.spinbox_xmax = QDoubleSpinBox()
        self.spinbox_xmax.setRange(0, 100)
        self.label_ymin = QLabel("ymin")
        self.spinbox_ymin = QDoubleSpinBox()
        self.spinbox_ymin.setRange(-100, 0)
        self.label_ymax = QLabel("ymax")
        self.spinbox_ymax = QDoubleSpinBox()
        self.spinbox_ymax.setRange(0, 100)

        self.grid = QGridLayout()
        self.grid.addWidget(self.radio_default, 0, 0, 1, 4)
        self.grid.addWidget(self.label_xmin, 1, 0)
        self.grid.addWidget(self.spinbox_xmin, 1, 1)
        self.grid.addWidget(self.label_xmax, 1, 2)
        self.grid.addWidget(self.spinbox_xmax, 1, 3)
        self.grid.addWidget(self.label_ymin, 2, 0)
        self.grid.addWidget(self.spinbox_ymin, 2, 1)
        self.grid.addWidget(self.label_ymax, 2, 2)
        self.grid.addWidget(self.spinbox_ymax, 2, 3)

        self.buttonBox = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        
        self.layout = QVBoxLayout()
        self.layout.addLayout(self.grid)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


    def populateWidgets(self):
        self.spinbox_xmin.setValue(self.settings.get_nyquist_xmin())
        self.spinbox_xmax.setValue(self.settings.get_nyquist_xmax())
        self.spinbox_ymin.setValue(self.settings.get_nyquist_ymin())
        self.spinbox_ymax.setValue(self.settings.get_nyquist_ymax())
        

    def disableWidgets(self):
        for w in self.widgets:
            w.setEnabled(False)


    def enableWidgets(self):
        for w in self.widgets:
            w.setEnabled(True)


    def onRadioDefaultToggle(self):        
        if self.radio_default.isChecked():
            self.settings.set_nyquist_default(True)
            self.disableWidgets()
        else:
            self.settings.set_nyquist_default(False)
            self.enableWidgets()


    def onAccpted(self):
        self.settings.set_nyquist_xmin(self.spinbox_xmin.value())
        self.settings.set_nyquist_xmax(self.spinbox_xmax.value())
        self.settings.set_nyquist_ymin(self.spinbox_ymin.value())
        self.settings.set_nyquist_ymax(self.spinbox_ymax.value())


class QDoubleSpinBoxLog(QDoubleSpinBox):
    """QDoubleSpinBox but in logarithmic scale"""
    def stepBy(self, steps):
        if steps == 1:
            if self.value() == 0:
                self.setValue(self.minimum())
            else:
                self.setValue(self.value()*10)
        elif steps == -1:
            self.setValue(self.value()/10)
        else:
            QDoubleSpinBox.stepBy(steps)