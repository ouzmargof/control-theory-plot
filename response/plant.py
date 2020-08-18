import numpy as np
import matplotlib.pyplot as plt

from scipy import signal
from scipy.signal import zpk2tf
import control

class Plant:
    def __init__(self, settings):
        self.num = [1]
        self.den = [1, 1]
        self.tf = 1
        self.tf_plant = 1
        self.tf_comp = 1
        self.loop_type = 'ol'
        self.plot_type = 'step'
        self.settings = settings


    def set_plot_type(self, value):
        self.plot_type = value


    def get_plot_type(self):
        return self.plot_type


    def set_loop_open(self):
        self.loop_type = 'ol'


    def set_loop_closed(self):
        self.loop_type = 'cl'


    def set_plant(self, **kwargs):
        self.num = kwargs['num']
        self.den = kwargs['den']
        self.tf_plant = control.tf(self.num, self.den)


    def set_comp(self, c_type, **kwargs):
        if c_type == 'gain':
            k = kwargs['k']
            self.tf_comp = k
        elif c_type == 'pid':
            kp = kwargs['kp']
            ki = kwargs['ki']
            kd = kwargs['kd']
            p_action = kp
            i_action = ki*control.tf([1], [1, 0])
            d_action = kd*control.tf([1, 0], [1])
            self.tf_comp = p_action + i_action + d_action
        elif c_type == 'leadlag':
            k = kwargs['k']
            td = kwargs['td']
            ad = kwargs['ad']
            tg = kwargs['tg']
            ag = kwargs['ag']
            lead_action = control.tf([td, 1], [td*ad, 1])
            lag_action = control.tf([tg, 1], [tg*ag, 1])
            self.tf_comp = k * lead_action * lag_action
        

    def set_tf(self):
        if self.loop_type == 'ol':
            self.tf = self.tf_plant
        elif self.loop_type == 'cl':
            self.tf = control.feedback(self.tf_plant*self.tf_comp, 1)


    def c_zpk2tf(self, zeros, poles, gain):
        num, den = zpk2tf(zeros, poles, gain)
        return num, den
        

    def plot(self, fig):
        if self.plot_type == 'step':
            return self.plot_step(fig)
        elif self.plot_type == 'rlocus':
            return self.plot_rlocus(fig)
        elif self.plot_type == 'bode':
            return self.plot_bode(fig)
        elif self.plot_type == 'nyquist':
            return self.plot_nyquist(fig)
 

    def plot_step(self, fig):
        if self.settings.is_step_default():
            t, y = control.step_response(self.tf)
        else:
            tmax = self.settings.get_step_time_max()
            step = self.settings.get_step_step()
            t = np.arange(0, tmax, step)
            _, y = control.step_response(self.tf, t)

        fig.clf()
        ax = fig.add_subplot(1, 1, 1)
        ax.plot(t, y)

        ax.set_xlabel('Time')
        ax.set_ylabel('Amplitude (s)')
        return fig


    def plot_bode(self, fig):
        tf = self.tf if self.loop_type == 'ol' else self.tf_plant*self.tf_comp

        if self.settings.is_bode_default():
            mag, phase, omega = control.bode(tf, dB=True, Plot=False)
        else:
            fmin = self.settings.get_bode_freq_min()
            fmax = self.settings.get_bode_freq_max()
            mag, phase, omega = control.bode(tf, omega_limits=[fmin, fmax], dB=True, Plot=False)
        
        mag = 20*np.log10(mag)
        phase = phase*180.0/np.pi

        fig.clf()

        ax1 = fig.add_subplot(2, 1, 1)
        ax1.semilogx(omega,mag)
        ax1.grid(which="both")
        ax1.set_xlabel('Frequency (rad/s)')
        ax1.set_ylabel('Magnitude (dB)')

        ax2 = fig.add_subplot(2, 1, 2)
        ax2.semilogx(omega,phase)
        ax2.grid(which="both")
        ax2.set_xlabel('Frequency (rad/s)')
        ax2.set_ylabel('Phase (deg)')

        return fig

        
    def plot_rlocus(self, fig):
        tf = self.tf if self.loop_type == 'ol' else self.tf_plant*self.tf_comp
        
        fig.clf()
        ax = fig.add_subplot(1, 1, 1)

        klist = np.linspace(500.0, 0, num = 1000) 
        rlist, _ = control.root_locus(tf, kvect=klist, Plot=False)
        
        rlist = np.vstack(rlist)

        poles = np.array(control.pole(tf))
        ax.plot(np.real(poles), np.imag(poles), 'x')
        
        zeros = np.array(control.zero(tf))
        if zeros.size > 0:
            ax.plot(np.real(zeros), np.imag(zeros), 'o')

        ax.plot(np.real(rlist), np.imag(rlist))

        ax.axhline(0., linestyle=':', color='k', zorder=-20)
        ax.axvline(0., linestyle=':', color='k')

        ax.set_xlabel('Real axis')
        ax.set_ylabel('Imaginary axis')

        if not self.settings.is_rlocus_default():
            zeta = self.settings.get_rlocus_zeta()
            wn = self.settings.get_rlocus_omega()

            x0 = -np.arccos(zeta)*wn if wn else ax.get_xlim()[0]
            xt = np.arange(x0, 0, 0.01)
            ax.plot(xt, -np.arccos(zeta)*xt, '--', linewidth=0.5, color='black')
            ax.plot(xt, np.arccos(zeta)*xt, '--', linewidth=0.5, color='black')

            x = np.arange(0, wn+0.01, 0.01)
            y = np.sqrt(wn**2 - x**2)
            x = -np.concatenate([x,x[::-1]])
            y = np.concatenate([y,-y[::-1]])
            ax.plot(x, y, '--', linewidth=0.5, color='black')

            xmin = self.settings.get_rlocus_xmin()
            xmax = self.settings.get_rlocus_xmax()
            ymin = self.settings.get_rlocus_ymin()
            ymax = self.settings.get_rlocus_ymax()
            ax.set_xlim(xmin, xmax)
            ax.set_ylim(ymin, ymax)

        return fig


    def plot_nyquist(self, fig):
        tf = self.tf if self.loop_type == 'ol' else self.tf_plant*self.tf_comp

        w = np.logspace(-100, 100, 50000)
        x, y, _ = control.nyquist(tf, omega = w)
        
        fig.clf()
        ax = fig.add_subplot(1, 1, 1)
        ax.plot(x, y)
        ax.plot(x, -y, '--')
        ax.plot([-1], [0], color='r', marker='x', markersize=10)

        ax.set_xlabel('Real axis')
        ax.set_ylabel('Imaginary axis')

        if not self.settings.is_nyquist_default():
            xmin = self.settings.get_nyquist_xmin()
            xmax = self.settings.get_nyquist_xmax()
            ymin = self.settings.get_nyquist_ymin()
            ymax = self.settings.get_nyquist_ymax()
            ax.set_xlim(xmin, xmax)
            ax.set_ylim(ymin, ymax)
        
        return fig


    def info(self):
        functions = {
            'step': self.info_step,
            'rlocus': self.info_rlocus,
            'bode': self.info_bode,
            'nyquist': self.info_nyquist
        }
        return functions[self.plot_type]()


    def info_step(self):
        for p in control.pole(self.tf):
            if np.real(p) > 0:
                return 'Unstable system'
        
        if self.settings.is_step_default():
            t, y = control.step_response(self.tf)
        else:
            tmax = self.settings.get_step_time_max()
            step = self.settings.get_step_step()
            t = np.arange(0, tmax, step)
            _, y = control.step_response(self.tf, t)

        yf = y[-1]
        
        os = 100 * (abs(y.max()-yf)/yf)

        tp = t[np.where(y == y.max())][0]

        ts = 0
        # Temporary fix for TF = 1
        try:
            for i in range(-1, -len(t)+1, -1):
                if y[i-1] > 1.02*yf or y[i-1] < 0.98*yf:
                    ts = t[i]
                    break
        except UnboundLocalError:
            pass

        tr_max = t[np.where(y > 0.9*yf)][0]
        tr_min = t[np.where(y > 0.1*yf)][0]
        tr =  tr_max - tr_min

        res = 'OS : {:.2f}% | Tp : {:.2f}s | Ts : {:.2f}s | Tr : {:.2f}s '.format(os, tp, ts, tr)
        
        return res

    
    def info_bode(self):
        tf = self.tf if self.loop_type == 'ol' else self.tf_plant*self.tf_comp

        try:
            gm, pm, wg, wp = control.margin(tf)
            gm = 20*np.log10(gm)

            if np.isinf(gm):
                g_txt = gm
            else:
                g_txt = '{:.2f} dB (at {:.2f} rad/s)'.format(gm, wg)
            
            if np.isinf(pm):
                p_txt = pm
            else:
                p_txt = '{:.2f} deg (at {:.2f} rad/s)'.format(pm, wp)
            
            res = 'GM : {} | PM : {} '.format(g_txt, p_txt)

            return res
        except:
            # Temporary fix for numpy error 'Eigenvalues did not converge'
            return 'Error. Plot could not be updated.'


    def info_rlocus(self):
        return '(EXPERIMENTAL) Click on a valid point to display gain.'


    def info_nyquist(self):
        return self.info_bode()


    def info_dynamic(self, event):
        functions = {
            'rlocus': self.info_dynamic_rlocus
        }
        return functions[self.plot_type](event)

    
    def info_dynamic_rlocus(self, event):
        # Temporary solution until control.rlocus is well understood
        tf = self.tf if self.loop_type == 'ol' else self.tf_plant*self.tf_comp
        s = complex(event.xdata, event.ydata)
        K = -1. / tf.horner(s)
        if abs(K.imag) < 1:
            p_re = np.round(s.real, 2)
            p_im = abs(np.round(s.imag, 2))
            gain = np.round(K.real, 2)[0][0]
            
            sign = '+' if s.imag > 0 else '-'
            return 'Gain = {} | Pole = {}{}j{}'.format(gain, p_re, sign, p_im)
        else:
            return '(EXPERIMENTAL) Click on a valid point to display gain.'