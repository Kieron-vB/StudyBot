import tkinter as tk
import time


class StudyTimer(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry('350x200')
        self.master.title('Study Timer')
        self.master.configure()

        # Add a frame to hold the widgets
        self.frame = tk.Frame(self.master)
        self.frame.pack(expand=True)

        # Add the widgets to the frame
        self.study_label = tk.Label(self.frame, text='Study timer: 00:00', font=('Montserrat', 20))
        self.study_label.pack()
        self.break_label = tk.Label(self.frame, text='Break timer: 00:00', font=('Montserrat', 20))
        self.break_label.pack()
        self.start_button = tk.Button(self.frame, text='Start', command=self.start_stop_study, font=('Montserrat', 10))
        self.start_button.pack()
        self.master.bind('<Return>', self.start_stop_study)
        self.study_running = False


    def start_stop_study(self, event=None):
        if not self.study_running:
            self.study_start_time = time.time()
            self.study_running = True
            self.start_button.config(text='Stop')
            self.update_study_timer()
        else:
            self.study_elapsed_time += time.time() - self.study_start_time
            self.study_running = False
            self.start_button.config(text='Start')
            self.break_()
        print('Study running:', self.study_running)

    def update_study_timer(self):
        if self.study_running:
            self.study_elapsed_time = time.time() - self.study_start_time
            self.study_time = self.study_elapsed_time  # update study time without breaks
            study_time = time.strftime('%M:%S', time.gmtime(self.study_time))
            self.study_label.config(text=f'Study timer: {study_time}')
            self.master.after(100, self.update_study_timer)

    def break_(self):
        self.break_start_time = time.time()
        self.break_running = True
        self.start_button.config(state='disabled')
        break_length = self.study_time // 5
        self.break_label.config(text=f'Break timer: {int(break_length)}:00')
        self.update_break_timer()

    def update_break_timer(self):
        if self.break_running:
            elapsed_time = time.time() - self.break_start_time
            remaining_time = int((self.study_time // 5) - elapsed_time)
            if remaining_time >= 0:
                break_time = time.strftime('%M:%S', time.gmtime(remaining_time))
                self.break_label.config(text=f'Break timer: {break_time}')
                self.master.after(100, self.update_break_timer)
            else:
                self.break_label.config(text='Break timer: Time is up!')
                self.break_running = False
                self.study_elapsed_time = 0
                self.study_time = 0
                self.study_label.config(text='Study timer: 00:00')
                self.start_button.config(state='normal')

root = tk.Tk()
root.geometry('400x300')
app = StudyTimer(root)
app.pack()
root.mainloop()
