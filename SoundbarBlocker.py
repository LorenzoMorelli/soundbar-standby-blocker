import sounddevice as sd
import numpy as np
import time
from threading import Thread, Event

from tkinter import Tk, Button
from tkinter import messagebox



######## SoundbarBlocker mechanism ########
class SoundbarBlockerThread(Thread):
    # Set the desired frequency (in Hertz)
    frequency = 1
    sample_rate = 44100

    
    def __init__(self, event, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.event = event

    def run(self):
        print("Started.")
        last_emit = time.time()
        self.emit_sound()

        while True:
            # emit every 10 minutes
            if time.time() - last_emit > 600:
                self.emit_sound()
                last_emit = time.time()
            # check if must stop
            if self.event.is_set():
                break
            # repeat checks every second
            time.sleep(1)
        print("Stopped.")

    def emit_sound(self):
        duration = 1  # Duration of the sound (in seconds)
        num_frames = int(duration*self.sample_rate)

        t = np.arange(num_frames) / self.sample_rate
        max_amp = 2**31-1 # maximum value of signed int32
        signal = max_amp*np.sin(2 * np.pi * self.frequency * t)
        signal = signal.astype(np.int32)
        sd.play(signal, samplerate=self.sample_rate)
        sd.wait()
        print("Sound emited at: " + time.strftime("%H:%M:%S"))


def start_clicked():
    global thread, event

    event = Event()
    thread = SoundbarBlockerThread(event)
    thread.start()
    # Terminate the process
    messagebox.showinfo('Started', 'Started')


def stop_clicked():
    global event

    # Terminate the process
    event.set()  # sends a SIGTERM
    messagebox.showinfo('Stopped', 'Stopped')



# ######## GUI ########

window = Tk()

window.title("Soundbar Blocker")
window.geometry('350x200')

event = Event()
thread = SoundbarBlockerThread(event)

btn_start = Button(window,text='Start', command=start_clicked)
btn_start.grid(column=0,row=0)
btn_stop = Button(window,text='Stop', command=stop_clicked)
btn_stop.grid(column=1,row=0)

window.mainloop()
