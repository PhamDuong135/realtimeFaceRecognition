import tkinter as tk
import tkinter.filedialog as fd
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from PIL import Image, ImageTk
import random
import os
from time import strftime

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://facerecognition-b163c-default-rtdb.asia-southeast1.firebasedatabase.app/"
})

def submit_form():
    ref = db.reference('Students')
    data = {
        "name": name_entry.get(),
        "major": major_entry.get(),
        "starting_year": int(starting_year_entry.get()),
        "total_attendance": int(total_attendance_entry.get()),
        "standing": standing_entry.get(),
        "year": int(year_entry.get()),
        "last_attendance_time": last_attendance_time_entry.get()
    }
    ref.child(student_id_entry.get()).set(data)
    status_label.config(text='Data saved successfully!')
def select_photo():
    filetypes = (("JPEG files","*.jpg"),("PNG files","*.png"))
    filename = fd.askopenfilename(title="Select a file", filetypes=filetypes)
    if filename:
        img = Image.open(filename)
        img = img.resize((216, 216), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        photo_label.config(image=photo)
        photo_label.image = photo
        # random_number = str(random.randint(1, 100000))
        file_extension = os.path.splitext(filename)[1]
        # new_filename = student_id_entry.get() + file_extension
        new_filename = student_id_entry.get() + '.png'
        img.save(os.path.join("Images/" + new_filename),'PNG')
        global photo_url
        photo_url = new_filename
        status_label.config(text='Photo selected successfully!')

root = tk.Tk()
root.title('Student Information Form')

student_id_label = tk.Label(root, text='Student ID:')
student_id_label.grid(row=0, column=0, padx=5, pady=5)

student_id_entry = tk.Entry(root)
student_id_entry.grid(row=0, column=1, padx=5, pady=5)

name_label = tk.Label(root, text='Name:')
name_label.grid(row=1, column=0, padx=5, pady=5)

name_entry = tk.Entry(root)
name_entry.grid(row=1, column=1, padx=5, pady=5)

major_label = tk.Label(root, text='Major:')
major_label.grid(row=2, column=0, padx=5, pady=5)

major_entry = tk.Entry(root)
major_entry.grid(row=2, column=1, padx=5, pady=5)

starting_year_label = tk.Label(root, text='Starting Year:')
starting_year_label.grid(row=3, column=0, padx=5, pady=5)

starting_year_entry = tk.Entry(root)
starting_year_entry.grid(row=3, column=1, padx=5, pady=5)

total_attendance_label = tk.Label(root, text='Total Attendance:')
total_attendance_label.grid(row=4, column=0, padx=5, pady=5)

total_attendance_entry = tk.Entry(root)
total_attendance_entry.grid(row=4, column=1, padx=5, pady=5)

standing_label = tk.Label(root, text='Standing:')
standing_label.grid(row=5, column=0, padx=5, pady=5)

standing_entry = tk.Entry(root)
standing_entry.grid(row=5, column=1, padx=5, pady=5)

year_label = tk.Label(root, text='Year:')
year_label.grid(row=6, column=0, padx=5, pady=5)

year_entry = tk.Entry(root)
year_entry.grid(row=6, column=1, padx=5, pady=5)

last_attendance_time_label = tk.Label(root, text='Last Attendance Time:')
last_attendance_time_label.grid(row=7, column=0, padx=5, pady=5)
#lấy thông tin thời gian thực của last attendance
entry_var = tk.StringVar()
current_time = strftime('%Y-%m-%d %H:%M:%S')  # Định dạng thời gian theo mong muốn
entry_var.set(current_time)

last_attendance_time_entry = tk.Entry(root, textvariable=entry_var)
last_attendance_time_entry.grid(row=7, column=1, padx=5, pady=5)

photo_select_button = tk.Button(root, text='Select Photo', command=select_photo)
photo_select_button.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

photo_label = tk.Label(root)
photo_label.grid(row=9, column=0, columnspan=2, padx=5, pady=5)

submit_button = tk.Button(root, text='Submit', command=submit_form)
submit_button.grid(row=10, column=0, columnspan=2, padx=5, pady=5)

status_label = tk.Label(root, text='')
status_label.grid(row=11, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()