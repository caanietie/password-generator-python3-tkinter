import random
import tkinter
import sqlite3
from os import path
from tkinter import font
from tkinter import messagebox, simpledialog


def copy_password():
    psug = pass_sugg.get()
    if psug:
        root.clipboard_clear()
        root.clipboard_append(psug)
        messagebox.showinfo(
            title='PassGen', message='Copied to clipboard'
        )


def gen_password():
    condStr = ''
    if space.get():
        condStr += ' '
    if number.get():
        condStr += '0123456789'
    if symbol.get():
        condStr += '!@#$%^&_-+=|;:.'
    if lowercase.get():
        condStr += 'abcdefghijklmnopqrstuvwxyz'
    if uppercase.get():
        condStr += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    if duplicate.get():
        # No duplicates exclusion if expected
        # password length > possible option
        if pass_len.get() > len(condStr):
            pass_len.set(len(condStr))
            messagebox.showwarning(
                title='Password Generator',
                message=f'Only {len(condStr)} unique characters are possible'
            )
        pass_sugg.set(''.join(random.sample(condStr, pass_len.get())))
    else:
        pass_sugg.set(''.join([
            condStr[int(random.random()*len(condStr))]
            for i in range(pass_len.get())
        ]))
    asterisk.set('＊'*pass_len.get())


def save_password():
    if pass_sugg.get():
        pass_id = simpledialog.askstring(
            'Password Generator', 'Enter identifier for password'
        )
        if pass_id:
            stmt = 'INSERT INTO password_generator(identifier, password) VALUES(?, ?)'
            db_pth = path.abspath(
                path.dirname(__file__) + '/data/password_generator.db'
            )
            db_con = sqlite3.connect(db_pth)
            db_con.execute(stmt, [pass_id, pass_sugg.get()])
            db_con.commit()
            messagebox.showinfo('Password Generator', 'Password saved!')
        elif pass_id == "":
            messagebox.showwarning(
                'Password Generator', 'Password identifier cannot be blank!'
            )


def header(tk_obj):
    hdr = tkinter.Frame(tk_obj, borderwidth=10)
    tkinter.Label(
        hdr, text="Password Generator", foreground='royalblue',
        font=font.Font(size=20, weight='bold')
    ).pack()
    return hdr


def eye_btn(allowed):
    pth = '/assets/eye-'+['blocked', 'allowed'][allowed]+'.png'
    return tkinter.PhotoImage(
        format='png', width=20, height=20,
        file=path.dirname(__file__)+pth
    )


def switch_eye():
    _sugg = frame.nametowidget('suggestion')
    _display = _sugg.nametowidget('display')
    _eye = _sugg.nametowidget('eye')
    allowed.set(not allowed.get())
    _btn, _disp = [[eye_blocked_btn, pass_sugg],
                   [eye_allowed_btn, asterisk]][allowed.get()]
    _eye.configure(image=_btn)
    _display.configure(textvariable=_disp)


def suggestion(tk_obj):
    sug = tkinter.Frame(tk_obj, borderwidth=15, name='suggestion')
    tkinter.Label(
        sug, bg='white', width=45, anchor='w', borderwidth=5, name='display',
        textvariable=pass_sugg, font=font.Font(family='Times', size=13)
    ).pack(side='left')
    tkinter.Button(
        sug, image=copy_btn, command=copy_password,
        width=25, height=25
    ).pack(side='right')
    tkinter.Button(
        sug, image=eye_blocked_btn, command=switch_eye,
        width=25, height=25, name='eye'
    ).pack(side='right')
    tkinter.Button(
        sug, image=floppy_disk_btn, command=save_password,
        width=25, height=25
    ).pack(side='right')
    return sug


def password_strength(tk_obj):
    pstr = tkinter.Frame(tk_obj, borderwidth=2, bg='white')
    # Maximum width should be 440
    tkinter.Frame(pstr, width=440, height=3, bg='royalblue').pack()
    return pstr


def password_length(tk_obj):
    plen = tkinter.Frame(tk_obj, borderwidth=10)
    tkinter.Label(
        plen, text='Password Length', width=36, anchor='w',
        font=font.Font(size=12, weight='bold')
    ).pack(side='left')
    tkinter.Label(
        plen, textvariable=pass_len, width=4, anchor='e',
        font=font.Font(size=12, weight='bold')
    ).pack(side='right')
    return plen


def password_slider(tk_obj):
    psld = tkinter.Frame(tk_obj, borderwidth=10)
    tkinter.Scale(
        psld, length=440, orient="horizontal", sliderlength=20,
        showvalue=False, variable=pass_len
    ).pack()
    return psld


def check_button(tk_obj, text, var):
    cbtn = tkinter.Frame(tk_obj)
    tkinter.Checkbutton(
        cbtn, onvalue=True, offvalue=False, variable=var
    ).pack(side='left')
    tkinter.Label(
        cbtn, text=text, width=17, anchor='w',
        font=font.Font(size=13)
    ).pack(side='right')
    return cbtn


def password_setting_row(tk_obj, col1_txt, var1, col2_txt, var2):
    psrow = tkinter.Frame(tk_obj)
    check_button(psrow, col1_txt, var1).pack(side='left')
    check_button(psrow, col2_txt, var2).pack(side='right')
    return psrow


def password_settings(tk_obj):
    pset = tkinter.Frame(tk_obj, borderwidth=10)
    tkinter.Label(
        pset, text='Password Setting', anchor='w', width=40,
        font=font.Font(size=12, weight='bold')
    ).pack()
    password_setting_row(
        pset, 'Lowercase', lowercase, 'Uppercase', uppercase
    ).pack(anchor='w')
    password_setting_row(
        pset, 'Numbers', number, 'Symbols', symbol
    ).pack(anchor='w')
    password_setting_row(
        pset, 'Exclude duplicate', duplicate, 'Include Space', space
    ).pack(anchor='w')
    return pset


def generate_password(tk_obj):
    pgen = tkinter.Frame(tk_obj, borderwidth=10)
    tkinter.Button(
        pgen, text='GENERATE PASSWORD', width=30, bg='royalblue',
        fg='white', font=font.Font(size=12), command=gen_password,
        activebackground='royalblue', activeforeground='white'
    ).pack()
    return pgen


fp = path.abspath(path.dirname(__file__)+'/assets/pass_gen.png')

root = tkinter.Tk(className='PassGen')
root.resizable(width=False, height=False)
root.iconphoto(True, tkinter.PhotoImage(file=fp))
root.title("Password Generator")

pass_sugg = tkinter.StringVar()
pass_len = tkinter.IntVar()
pass_len.initialize(8)

asterisk = tkinter.StringVar()

floppy_disk_btn = tkinter.PhotoImage(
    format='png', width=20, height=20,
    file=path.dirname(__file__)+'/assets/floppy-disk.png'
)

allowed = tkinter.BooleanVar()
allowed.initialize(False)
eye_allowed_btn = eye_btn(True)
eye_blocked_btn = eye_btn(False)

copy_btn = tkinter.PhotoImage(
    format='png', width=20, height=20,
    file=path.dirname(__file__)+'/assets/copy.png'
)

lowercase = tkinter.BooleanVar()
lowercase.initialize(True)

uppercase = tkinter.BooleanVar()
uppercase.initialize(True)

number = tkinter.BooleanVar()
number.initialize(True)

symbol = tkinter.BooleanVar()

duplicate = tkinter.BooleanVar()

space = tkinter.BooleanVar()

strength_length = tkinter.StringVar()
strength_color = tkinter.StringVar()

frame = tkinter.Frame(root, borderwidth=1, relief="raised")
header(frame).pack()
suggestion(frame).pack()
password_strength(frame).pack()
password_length(frame).pack()
password_slider(frame).pack()
password_settings(frame).pack()
generate_password(frame).pack()
frame.pack(padx=10, pady=10, fill='both')
root.mainloop()
