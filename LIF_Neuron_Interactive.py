import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import  Button, Slider
from matplotlib.widgets import TextBox

#==============================================================================#

def LIF(I, _I=0.005, gl=0.16, Cm=0.0049):

    ######### Constants
    El      =   -0.065                      # restint membrane potential [V]
    thresh  =   -0.050                      # spiking threshold [V]

    ######### Experimental Setup
    # TIME
    T       =   0.100                       # total simulation length [s]
    dt      =   0.00002                     # step size [s]
    time    =   np.arange(0, T+dt, dt)      # step values [s]
    # VOLTAGE
    V       =   np.empty(len(time))         # array for saving Voltage history
    V[0]    =   El                          # set initial to resting potential
    # CURRENT
    
    ######### Measurements
    spikes  =   0                           # counter for number of spikes
    spike_status = False
    ######### Simulation
    for i in range(1, len(time)):
        # use "I - V/R = C * dV/dT" to get this equation
        dV =  (I[i] - gl*(V[i-1]-El))/Cm
        V[i] = V[i-1] + dV*dt

        # in case we exceed threshold
        if V[i] > thresh:
            V[i-1] = 0.04   # set the last step to spike value
            V[i] = El       # current step is resting membrane potential
            spikes += 1     # count spike

    return V

# function that offsets the V values by a certain time interval
def inhibitedLIF(V, offset=500):
    V = np.roll(V, offset)
    V[:offset] = -0.065

    
    return V


def I_values(_I=0.005, time=None, start=1000, end=2000, start2=3000, end2=4000):
    I = np.zeros(len(time))
    I[start:end] = _I
    I[start2:end2] = _I
    return I

#==============================================================================#

def start_LIF_sim():
    # time parameters for plotting
    T       =   0.100                       # total simulation length [s]
    dt      =   0.00002                     # step size [s]
    time    =   np.arange(0, T+dt, dt)      # step values [s]

    # initial parameters
    I_init  =   0.005
    gl_init =   0.16
    Cm_init =   0.0049
    I_2_init =  0.005

    # update functions for lines
    I = I_values(_I=I_init, time=time)
    V = LIF(I, _I=I_init, gl=gl_init, Cm=Cm_init)
    # V_2 = inhibitedLIF(V, 500)
    # I_2 = I_values(_I=I_2_init, time=time)

    ######### Plotting
    axis_color = 'lightgoldenrodyellow'

    fig = plt.figure("Leaky Integrate-and-Fire Neuron", figsize=(14, 7))
    ax = fig.add_subplot(111)
    plt.title("Interactive Leaky Integrate-and-Fire Neuron Simulation")
    fig.subplots_adjust(left=0.1, bottom=0.32)

    # plot lines
    line = plt.plot(time, V, label="Neuron 1 MP")[0]
    # line2 = plt.plot(time, V_2, label="Neuron 2 MP")[0]
    line3 = plt.plot(time, I, label="Applied Current")[0]

    # add legend
    plt.legend(loc="upper right")

    # add axis labels
    plt.ylabel("Potential [V]/ Current [A]")
    plt.xlabel("Time [s]")

    # define sliders (position, color, inital value, parameter, etc...)
    I_slider_axis = plt.axes([0.1, 0.17, 0.65, 0.03], facecolor=axis_color)
    I_slider = Slider(I_slider_axis, '$I_{ext}$', 0, 0.05, valinit=I_init)

    gl_slider_axis = plt.axes([0.1, 0.12, 0.65, 0.03], facecolor=axis_color)
    gl_slider = Slider(gl_slider_axis, '$g_{L}$', 0.0, 0.3, valinit=gl_init)

    Cm_slider_axis = plt.axes([0.1, 0.07, 0.65, 0.03], facecolor=axis_color)
    Cm_slider = Slider(Cm_slider_axis, '$C_{m}$', 0.0, 0.01, valinit=Cm_init)

    # current start time and end time text boxes at the bottom left and right
    I_start_textbox = TextBox(plt.axes([0.1, 0.02, 0.05, 0.03]), 'I_start  ', initial='1000')
    I_end_textbox = TextBox(plt.axes([0.26, 0.02, 0.05, 0.03]), 'I_end  ', initial='2000')

    # start 2 and end 2 text boxes
    I_start_textbox_2 = TextBox(plt.axes([0.42, 0.02, 0.05, 0.03]), 'I_start2  ', initial='3000')
    I_end_textbox_2 = TextBox(plt.axes([0.58, 0.02, 0.05, 0.03]), 'I_end2  ', initial='4000')
    


    # update functions
    def update(val):
        # line2.set_ydata(inhibitedLIF(line.get_ydata(), int(500 + -1000*I_slider.val**10 )))
        start, end = int(I_start_textbox.text), int(I_end_textbox.text)
        start2, end2 = int(I_start_textbox_2.text), int(I_end_textbox_2.text)
        I_new = I_values(I_slider.val, time, start=start, end=end, start2=start2, end2=end2)
        line3.set_ydata(I_new)
        line.set_ydata(LIF(I_new, I_slider.val, gl_slider.val, Cm_slider.val))
        # line2.set_ydata(inhibitedLIF(line.get_ydata(), int(500 + -1000*I_slider.val**10 )))
       

    
   

    # update, if any slider is moved
    I_slider.on_changed(update)
    gl_slider.on_changed(update)
    Cm_slider.on_changed(update)

    # update, if any textbox is changed
    def update_textbox(val):
        I_start = int(I_start_textbox.text)
        I_end = int(I_end_textbox.text)
        I_start_2 = int(I_start_textbox_2.text)
        I_end_2 = int(I_end_textbox_2.text)
        I_new = I_values(I_slider.val, time, start=I_start, end=I_end, start2=I_start_2, end2=I_end_2)
        line3.set_ydata(I_new)
        line.set_ydata(LIF(I_new, I_slider.val, gl_slider.val, Cm_slider.val))
        # line2.set_ydata(inhibitedLIF(line.get_ydata(), int(500 + -1000*I_slider.val**10 )))
        fig.canvas.draw_idle()

    I_start_textbox.on_submit(update_textbox)
    I_end_textbox.on_submit(update_textbox)
    I_start_textbox_2.on_submit(update_textbox)
    I_end_textbox_2.on_submit(update_textbox)

    # Add a button for resetting the parameters
    reset_button_ax = plt.axes([0.8, 0.02, 0.1, 0.04])
    reset_button = Button(
        reset_button_ax, 'Reset', color=axis_color, hovercolor='0.975')

    # event of resert button being clicked
    def reset_button_was_clicked(event):
        I_slider.reset()
        gl_slider.reset()
        Cm_slider.reset()

    reset_button.on_clicked(reset_button_was_clicked)

    plt.show()


#==============================================================================#

if (__name__ == '__main__'):
    start_LIF_sim()
