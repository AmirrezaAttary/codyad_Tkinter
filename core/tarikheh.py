import sqlite3
from customtkinter import *
from tkinter import CENTER, END, E

font_enry = ("B Nazanin", 18)
font_bt = ("Vazir", 20)

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def create_header(frame, font_enry_):
    headers = ["مالک دستگاه", "نام دستگاه", "مدل دستگاه", "کدملی", "موبایل"]
    for i, header in enumerate(headers[::-1], start=5):
        entry = CTkLabel(
            frame,
            text=header,
            font=font_enry_,
            fg_color="#d9d9d9",         # رنگ پس‌زمینه شبیه CTkEntry غیرفعال
            text_color="black",         # رنگ متن
            corner_radius=5,            # گوشه‌های گرد
            width=136,
            height=28,
            anchor=CENTER               # وسط‌چین کردن متن
        )
        entry.grid(row=0, column=i, padx=2, pady=2, sticky=E)

def create_data_row(frame, font_enry_, font_bt, row_data, row_index, show_callback, delete_callback):
    from customtkinter import CTkLabel, CTkButton, CTkFont
    from tkinter import E, CENTER

    # داده‌ها برای ستون‌ها به ترتیب: مالک، نام دستگاه، مدل، کدملی، موبایل
    values = [
        f"0{row_data[8]}",  # موبایل
        f"0{row_data[9]}",  # کدملی
        row_data[5],        # مدل
        row_data[3],        # نام دستگاه
        row_data[7],        # مالک دستگاه
    ]

    for i, value in enumerate(values, start=5):
        label = CTkLabel(
            frame,
            text=value,
            font=font_enry_,
            fg_color="#d9d9d9",     # همان رنگ پس‌زمینه برای هماهنگی
            text_color="black",
            corner_radius=5,
            width=136,
            height=28,
            anchor=CENTER
        )
        label.grid(row=0, column=i, padx=2, pady=2, sticky=E)

    # دکمه‌ها
    btn_show = CTkButton(
        frame,
        width=50,
        font=CTkFont(family="Vazir", size=20, weight='bold'),
        text='نمایش',
        command=lambda: show_callback(row_data[0])
    )
    btn_show.grid(row=0, column=4, padx=2, sticky=E)

    btn_del = CTkButton(
        frame,
        width=50,
        font=CTkFont(family="Vazir", size=20, weight='bold'),
        text='حذف',
        fg_color='red',
        command=lambda: delete_callback(row_data[0])
    )
    btn_del.grid(row=0, column=3, padx=2, sticky=E)



def display_results(search_text, column, main_frame, show_callback, delete_callback):
    clear_frame(main_frame)

    header_frame = CTkFrame(main_frame, fg_color='skyblue', corner_radius=5)
    header_frame.pack(pady=5, fill='x')
    create_header(header_frame)

    with sqlite3.connect('db.db') as con:
        c = con.cursor()
        c.execute(f"SELECT * FROM paziresh WHERE {column} = ? AND status = 0", (search_text,))
        rows = c.fetchall()

        for i, row_data in enumerate(rows):
            row_frame = CTkFrame(main_frame, fg_color='skyblue', corner_radius=5)
            row_frame.pack(pady=5, fill='x')
            create_data_row(row_frame, row_data, i, show_callback, delete_callback)


