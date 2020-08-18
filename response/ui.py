import matplotlib.pyplot as plt
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import(
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox, QTabWidget,
    QLabel, QLineEdit, QPushButton, QRadioButton, QMessageBox, QDoubleSpinBox)
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT)
plt.style.use('bmh')

from response import plant
from response import tex
from response import config
from response import settings

class stackResponse(QWidget):
    def __init__(self, ):
        super().__init__()

        # UI
        self.setupUiEq()
        self.setupUiFig()
        self.setupUiControlOL()
        self.setupUiControlCL()
        self.setupUiControlPlotType()
        self.setupUi()

        # Slots
        self.btn_about.clicked.connect(self.onBtnAboutClick)
        self.btn_zpk.clicked.connect(self.onBtnZpkClick)
        self.btn_update.clicked.connect(self.onBtnUpdateClick)
        self.btn_custom.clicked.connect(self.onBtnCustomClick)
        self.btn_compensator.clicked.connect(self.onBtnCompensatorClick)
        self.groupbox_cl.clicked.connect(self.onGroupboxClClick)

        # Data
        self.settings = settings.Settings()
        self.equation = tex.TexTf()
        self.plant = plant.Plant(self.settings)
        
        # First run
        self.updateAll()


    def setupUi(self):
        hbox_control = QHBoxLayout()
        hbox_control.addWidget(self.groupbox_ol, 1)
        hbox_control.addWidget(self.groupbox_cl, 1)

        self.btn_about = QPushButton("About")
        hbox_toolbar = QHBoxLayout()
        hbox_toolbar.addWidget(self.plot_toolbar)
        hbox_toolbar.addWidget(self.btn_about)

        self.layout = QVBoxLayout()
        self.layout.addLayout(hbox_control)
        self.layout.addWidget(self.groupbox_plot_type)
        self.layout.addWidget(self.groupbox_plot, 4)
        self.layout.addLayout(hbox_toolbar)
        self.setLayout(self.layout)


    def setupUiControlOL(self):
        self.label_num = QLabel("Numerator")       
        self.line_num = QLineEdit()
        self.label_den = QLabel("Denominator")       
        self.line_den = QLineEdit()

        self.line_num.setText("1")
        self.line_den.setText("1 1")

        grid = QGridLayout()
        grid.addWidget(self.label_num, 0, 0)
        grid.addWidget(self.line_num, 0, 1)
        grid.addWidget(self.label_den, 1, 0)
        grid.addWidget(self.line_den, 1, 1)

        self.btn_zpk = QPushButton("ZPK to TF")
        self.btn_zpk.setAutoDefault(False)

        vbox = QVBoxLayout()
        vbox.addWidget(self.eq_canvas)
        vbox.addLayout(grid)
        vbox.addWidget(self.btn_zpk)
        
        self.groupbox_ol = QGroupBox("Plant model")
        self.groupbox_ol.setLayout(vbox)
        

    def setupUiControlCL(self):
        # Tab Gain
        label_gain = QLabel("Gain")
        self.spin_gain = QDoubleSpinBox()
        self.spin_gain.setValue(1)

        grid_gain = QGridLayout()
        grid_gain.addWidget(label_gain, 0, 0)
        grid_gain.addWidget(self.spin_gain, 0, 1)
        self.tab_gain = QWidget()
        self.tab_gain.setLayout(grid_gain)
        
        # Tab PID
        label_kp = QLabel("Kp")       
        self.spin_kp = QDoubleSpinBox()
        label_ki = QLabel("Ki")
        self.spin_ki = QDoubleSpinBox()
        label_kd = QLabel("Kd")
        self.spin_kd = QDoubleSpinBox()
        self.spin_kp.setValue(1)
        grid_pid = QGridLayout()
        grid_pid.addWidget(label_kp, 0, 0)
        grid_pid.addWidget(self.spin_kp, 0, 1)
        grid_pid.addWidget(label_ki, 1, 0)
        grid_pid.addWidget(self.spin_ki, 1, 1)
        grid_pid.addWidget(label_kd, 2, 0)
        grid_pid.addWidget(self.spin_kd, 2, 1)
        self.tab_pid = QWidget()
        self.tab_pid.setLayout(grid_pid)

        # Tab Lead-Lag
        self.tab_leadlag = QWidget()
        label_k = QLabel("Gain")       
        self.spin_k = QDoubleSpinBox()
        self.spin_k.setValue(1)
        label_ad = QLabel("Alpha-Lead")
        self.spin_ad = QDoubleSpinBox()
        label_td = QLabel("Tau-Lead")
        self.spin_td = QDoubleSpinBox()
        label_ag = QLabel("Alpha-Lag")
        self.spin_ag = QDoubleSpinBox()
        label_tg = QLabel("Tau-Lag")
        self.spin_tg = QDoubleSpinBox()
        grid_leadlag = QGridLayout()
        grid_leadlag.addWidget(label_k, 0, 0, 1, 2)
        grid_leadlag.addWidget(self.spin_k, 0, 2, 1, 2)
        grid_leadlag.addWidget(label_ad, 1, 0)
        grid_leadlag.addWidget(self.spin_ad, 1, 1)
        grid_leadlag.addWidget(label_td, 2, 0)
        grid_leadlag.addWidget(self.spin_td, 2, 1)
        grid_leadlag.addWidget(label_ag, 1, 2)
        grid_leadlag.addWidget(self.spin_ag, 1, 3)
        grid_leadlag.addWidget(label_tg, 2, 2)
        grid_leadlag.addWidget(self.spin_tg, 2, 3)
        self.tab_leadlag = QWidget()
        self.tab_leadlag.setLayout(grid_leadlag)

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.addTab(self.tab_gain, 'Gain')
        self.tabs.addTab(self.tab_pid, 'PID')
        self.tabs.addTab(self.tab_leadlag, 'Lead-Lag')
        # Button
        self.btn_compensator = QPushButton("Update compensator")
        self.btn_compensator.setAutoDefault(False)

        # Layout
        vbox = QVBoxLayout()
        vbox.addWidget(self.tabs)
        vbox.addWidget(self.btn_compensator)
        self.groupbox_cl = QGroupBox("Closed loop")
        self.groupbox_cl.setLayout(vbox)
        self.groupbox_cl.setCheckable(True)
        self.groupbox_cl.setChecked(False)

        # Set range for all spinboxes
        for widget in self.groupbox_cl.findChildren(QDoubleSpinBox):
            widget.setRange(0, 10000)
        


    def setupUiControlPlotType(self):
        self.rd_step = QRadioButton("Step")
        self.rd_rlocus = QRadioButton("Root locus")
        self.rd_bode = QRadioButton("Bode")
        self.rd_nyquist = QRadioButton("Nyquist")
        self.rd_step.setChecked(True)

        self.btn_update = QPushButton("Update plot")
        self.btn_custom = QPushButton("Customize plot")
        self.btn_custom.setAutoDefault(False)

        hbox_left = QHBoxLayout()
        hbox_left.addWidget(self.rd_step)
        hbox_left.addWidget(self.rd_rlocus)
        hbox_left.addWidget(self.rd_bode)
        hbox_left.addWidget(self.rd_nyquist)

        hbox_right = QHBoxLayout()
        hbox_right.addWidget(self.btn_update)
        hbox_right.addWidget(self.btn_custom)

        hbox = QHBoxLayout()
        hbox.addLayout(hbox_left, 2)
        hbox.addLayout(hbox_right, 1)

        self.groupbox_plot_type = QGroupBox("Plot type")
        self.groupbox_plot_type.setLayout(hbox)


    def setupUiEq(self):
        self.eq_fig, self.eq_ax = plt.subplots()
        self.eq_canvas = FigureCanvas(self.eq_fig)
        
        self.eq_canvas.setFixedHeight(70) # TODO : FIND A BETTER WAY TO SIZE
        self.eq_canvas.draw()


    def setupUiFig(self):
        self.plot_fig = plt.figure()
        self.plot_canvas = FigureCanvas(self.plot_fig)
        self.plot_toolbar = NavigationToolbar(self.plot_canvas, self)
        self.plot_canvas.draw()

        self.label_plot_info = QLabel()
        self.label_plot_info.setAlignment(
            QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        
        vbox = QVBoxLayout()
        vbox.addWidget(self.label_plot_info, 0)
        vbox.addWidget(self.plot_canvas, 10)
        
        self.groupbox_plot = QGroupBox("Plot")
        self.groupbox_plot.setLayout(vbox)


    def updateFigure(self):
        self.plot_fig = self.plant.plot(self.plot_fig)
        self.plot_canvas.draw_idle()


    def updateEq(self):
        left, width = .25, .5
        bottom, height = .25, .5
        right = left + width
        top = bottom + height

        self.eq_ax.cla()
        self.eq_ax.axis('off')
        self.eq_ax.text(
            0.5*(left+right), 0.5*(bottom+top),
            self.equation.get_title(),
            fontsize=24,
            ha ='center', va = 'center')
        self.eq_canvas.draw_idle()

    
    def onBtnAboutClick(self):
        text = '''
        A PyQt interface for plotting common graphs in control theory.

        This project is still a work in progress.
        Check for newer versions at : https://github.com/ouzmargof
        '''
        msgbox = QMessageBox(QMessageBox.NoIcon, 'About', text)
        msgbox.exec_()


    def onBtnZpkClick(self):
        dialog = config.ConfigZpk()
        res = dialog.exec_()
        if res:
            try:
                zeros, poles, gain = dialog.value()
                zeros = [self.extract(zero) for zero in zeros]
                poles = [self.extract(pole) for pole in poles]
                gain = self.extract(gain)
                num, den = self.plant.c_zpk2tf(zeros, poles, gain)
                
                num_str = self.cleanZpkPolynomial(str(num.tolist()))
                den_str = self.cleanZpkPolynomial(str(den.tolist()))
                
                self.line_num.setText(num_str)
                self.line_den.setText(den_str)
            except TypeError:
                pass
            

    def onBtnCustomClick(self):
        functions = {
            'step': config.ConfigResponseStep,
            'rlocus': config.ConfigResponseRlocus,
            'bode': config.ConfigResponseBode,
            'nyquist': config.ConfigResponseNyquist
        }
        res = functions[self.plant.get_plot_type()](self.settings).exec_()
        if res:
            self.updateAll()


    def onBtnUpdateClick(self):
        self.updateAll()


    def onGroupboxClClick(self):
        if self.groupbox_cl.isChecked():
            self.plant.set_loop_closed()
        else:
            self.plant.set_loop_open()


    def onBtnCompensatorClick(self):
        if self.tabs.currentIndex() == 0:
            k = self.spin_gain.value()
            self.plant.set_comp('gain', k=k)
        elif self.tabs.currentIndex() == 1:
            kp = self.spin_kp.value()
            ki = self.spin_ki.value()
            kd = self.spin_kd.value()
            self.plant.set_comp('pid', kp=kp, ki=ki, kd=kd)
        elif self.tabs.currentIndex() == 2:
            k = self.spin_k.value()
            ad = self.spin_ad.value()
            td = self.spin_td.value()
            ag = self.spin_ag.value()
            tg = self.spin_tg.value()
            self.plant.set_comp('leadlag', k=k, ad=ad, td=td, ag=ag, tg=tg)
        

    def updateAll(self):
        res = self.validateBeforeUpdate()
        if (res):
            QMessageBox.critical(self, 'Error', res)
        else:
            self.updateData()
            self.updateLoop()
            self.updatePlotType()
            self.updateFigure()
            self.updateEq()
            self.updateInfo()
            self.updateListener()


    def updateLoop(self):
        self.plant.set_tf()


    def updatePlotType(self):
        if self.rd_step.isChecked():
            self.plant.set_plot_type('step')
        elif self.rd_rlocus.isChecked():
            self.plant.set_plot_type('rlocus')
        elif self.rd_bode.isChecked():
            self.plant.set_plot_type('bode')
        elif self.rd_nyquist.isChecked():
            self.plant.set_plot_type('nyquist')


    def updateData(self):
        try:
            num = [self.extract(t) for t in self.line_num.text().split()]
            den = [self.extract(t) for t in self.line_den.text().split()]
            self.plant.set_plant(num=num, den=den)
            self.equation.update(num=num, den=den)
        except ValueError:
            pass


    def updateInfo(self):
        self.label_plot_info.setText(self.plant.info())


    def updateListener(self):
        if self.plant.get_plot_type() == 'rlocus':
            self.cid = self.plot_canvas.mpl_connect(
                'button_release_event', self.updateInfoDynamic)
        else:
            try:
                self.plot_canvas.mpl_disconnect(self.cid)
            except AttributeError:
                pass


    def updateInfoDynamic(self, event):
        if self.plant.get_plot_type() == 'rlocus':
            self.label_plot_info.setText(self.plant.info_dynamic(event))


    def extract(self, value):
        try:
            return int(value)
        except ValueError:
            try:
                return float(value)
            except ValueError:
                try:
                    return complex(value)
                except ValueError:
                    return
    
    
    def cleanZpkPolynomial(self, poly_in):
        #remove redundant characters
        poly_out = poly_in
        poly_out = poly_out.replace('[', '')
        poly_out = poly_out.replace(']', '')
        poly_out = poly_out.replace(',', '')
        poly_out = poly_out.replace('.0', '')
        return poly_out
    

    def validateBeforeUpdate(self):
        num = self.line_num.text().split()
        den = self.line_den.text().split()

        for cn, dn in zip(num, den):
            if cn.islower() or cn.isupper() or dn.islower() or dn.isupper():
                return 'Coefficients cannot contain letters'

        if len(num) > len(den):
            return 'Transfer function must be proper'
        
        return


class NavigationToolbar(NavigationToolbar2QT):
    """Customize Matplotlib Toolbar"""
    toolitems = [t for t in NavigationToolbar2QT.toolitems if
                t[0] in ('Home', 'Pan', 'Zoom', 'Save')]
    def set_message(self, msg):
        """Disable coordinates"""
        pass