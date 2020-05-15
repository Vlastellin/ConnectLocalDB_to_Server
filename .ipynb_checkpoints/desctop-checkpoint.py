
from tkinter import *  
from tkinter import messagebox 
from tkinter import filedialog
import os
import tkinter as tk
from tkinter import ttk
import os.path
import pickle
import time

is_first= not( os.path.exists('settings.pickle'))
path_access=''
path_exel=''
run=False
if not is_first:
    with open('settings.pickle', 'rb') as f:
        t= pickle.load(f)
    path_access=t[0]
    path_exel=t[1]

def clicked_down():
    if is_first:
        messagebox.showerror("Ошибка!","Выберите файл access и exel во вкладке Настройки ")
        return 1
    global run
    run= True
    while run:
        print('run')
        time.sleep(5000)
        
def clicked_up():
    global run
    run= False
        
def t2_b1_clicked():
    global path_access
    path_access =  filedialog.askopenfilename()
    t2_lbl3.configure(text=str(path_access )) 
    
def t2_b2_clicked():
    global path_exel
    path_exel =  filedialog.askopenfilename()
    t2_lbl4.configure(text=str(path_exel )) 
    
def t2_b3_clicked():
    global path_exel
    global path_access
    if path_exel=='':
        messagebox.showerror("Ошибка!", "Не выбран  файл exel ")
        return 1
    if path_access=='':
        messagebox.showerror("Ошибка!", "Не выбран  файл access ")
        return 1
    with open('settings.pickle', 'wb') as f:
        pickle.dump([path_access,path_exel], f)   
    messagebox.showinfo("Операция выполнена", "Новые настройки сохранены")
    


window = Tk()  
window.title("Связь с сервером")  
window.geometry('650x600')  
tab_control = ttk.Notebook(window)  
tab2 = ttk.Frame(tab_control) 
tab1 = ttk.Frame(tab_control)  
  
tab_control.add(tab1, text='Главная')  
tab_control.add(tab2, text='Настройка') 
 

lbl1 = Label(tab1, text='Настройки заданы по умолчанию               ')  
 
btn = Button(tab1, text='Запустить', command=clicked_down)  
btn.grid(column=1, row=0,padx=10, pady=10, sticky="w" ) 
btn = Button(tab1, text='Остановить', command=clicked_up)  
btn.grid(column=1, row=0,padx=10, pady=10, sticky="w" ) 

#tab2

t2_b1 = Button(tab2, text='Выбрать базу данных', command=t2_b1_clicked)  
t2_b1.grid(column=0, row=2,padx=10, pady=10, sticky="w" ) 
t2_lbl3 = Label(tab2, text='')  
t2_lbl3.grid(column=0, row=3, padx=10, pady=10, sticky="w")

t2_b2 = Button(tab2, text='Выберите файл exel', command=t2_b2_clicked)  
t2_b2.grid(column=0, row=5,padx=10, pady=10, sticky="w" ) 
t2_lbl4 = Label(tab2, text='')  
t2_lbl4.grid(column=0, row=6, padx=10, pady=10, sticky="w")

t2_b3 = Button(tab2, text='Сохранить настройки', command=t2_b3_clicked)  
t2_b3.grid(column=0, row=7,padx=10, pady=10, sticky="w" ) 


window.mainloop()