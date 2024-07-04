import tkinter as tk
from tkinter import filedialog
import winsound
from datetime import datetime, timedelta

class SchoolBellApp:
    def __init__(self, master):
        self.master = master
        master.title("Maktab Qong'irog'i")

        self.schedule_entries = []
        self.create_schedule_entry()

        self.add_button = tk.Button(master, text="Qo'ng'iroq qo'shish", command=self.create_schedule_entry)
        self.add_button.pack()

        self.start_button = tk.Button(master, text="Boshlash", command=self.start_schedule)
        self.start_button.pack()

        self.quit_button = tk.Button(master, text="Tugatish", command=master.quit)
        self.quit_button.pack()

    def create_schedule_entry(self):
        new_entry = tk.Frame(self.master)
        new_entry.pack()

        time_label = tk.Label(new_entry, text="Vaqt (ЧЧ:ММ):")
        time_label.grid(row=0, column=0)

        time_entry = tk.Entry(new_entry)
        time_entry.grid(row=0, column=1)

        browse_button = tk.Button(new_entry, text="Tanlash", command=lambda entry=new_entry: self.browse_file(entry))
        browse_button.grid(row=0, column=2)

        new_entry.audio_file_path = tk.StringVar()
        tk.Label(new_entry, textvariable=new_entry.audio_file_path).grid(row=0, column=3)

        self.schedule_entries.append(new_entry)

    def browse_file(self, entry):
        file_path = filedialog.askopenfilename()
        entry.audio_file_path.set(file_path)

    def start_schedule(self):
        for entry in self.schedule_entries:
            call_time_str = entry.winfo_children()[1].get()
            audio_file_path = entry.audio_file_path.get()

            if call_time_str and audio_file_path:
                try:
                    call_time = datetime.strptime(call_time_str, "%H:%M")
                    now = datetime.now()

                    scheduled_time = datetime(now.year, now.month, now.day, call_time.hour, call_time.minute)
                    if scheduled_time < now:
                        scheduled_time += timedelta(days=1)

                    delay = (scheduled_time - now).total_seconds()

                    self.master.after(int(delay * 1000), self.make_school_call, audio_file_path)
                except ValueError:
                    print("Notogri format iltimos qayta urinib koring")
            else:
                print("vaqt va fayl kiriting")

    def make_school_call(self, audio_file_path):
        winsound.PlaySound(audio_file_path, winsound.SND_FILENAME)

def run_app():
    root = tk.Tk()
    app = SchoolBellApp(root)
    root.mainloop()

if __name__ == "__main__":
    run_app()