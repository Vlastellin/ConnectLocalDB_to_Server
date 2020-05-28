import pyodbc
import requests
import json
import time
from tkinter import *  
from tkinter import messagebox 
from tkinter import filedialog
import os
from tkinter import ttk
import os.path
import pickle


class Desctop(object):
    def __init__(self):
        self.is_first= not( os.path.exists('settings.pickle'))
        self.path_access=''
        self.path_exel=''
        self.tab_read=''
        self.tab_write=''
        self.run=False
        self.time = 0
        self.url = 'http://176.58.60.36/kokoro/connect_to_server/'
        self.GUI()
        
    def start(self):
        self.connect()
        self.window.mainloop()
        
    def GUI(self):
        self.window = Tk()
        self.window.title("Связь с сервером")  
        self.window.geometry('650x300')  
        self.tab_control = ttk.Notebook(self.window)  
        self.tab1 = ttk.Frame(self.tab_control) 
        self.tab_control.add(self.tab1, text='Настройка') 
        self.t1_b1 = Button(self.tab1, text='Выбрать базу данных', command=self.t1_b1_clicked)  
        self.t1_b1.grid(column=0, row=1,padx=10, pady=10, sticky="w" ) 
        self.t1_lbl3 = Label(self.tab1, text='')  
        self.t1_lbl3.grid(column=0, row=2, padx=10, pady=10, sticky="w")
        self.t1_lbl1 = Label(self.tab1, text='Имя таблицы для записи:')  
        self.t1_lbl1.grid(column=0, row=3, padx=10, pady=10, sticky="w")
        self.t1_txt1 = Entry(self.tab1,width=30)  
        self.t1_txt1.grid(column=1, row=3, padx=10, pady=10, sticky="w")
        self.t1_lbl2 = Label(self.tab1, text='Имя таблицы для чтения:')  
        self.t1_lbl2.grid(column=0, row=4, padx=10, pady=10, sticky="w")
        self.t1_txt2 = Entry(self.tab1,width=30)  
        self.t1_txt2.grid(column=1, row=4, padx=10, pady=10, sticky="w")
        self.t1_b3 = Button(self.tab1, text='Запустить',background="#99FF99", command=self.t1_b3_clicked)  
        self.t1_b3.grid(column=0, row=5,padx=10, pady=10, sticky="w" ) 
        self.t1_b4 = Button(self.tab1, text='Остановить',background="#FF6666", command=self.t1_b4_clicked)  
        self.t1_b4.grid(column=1, row=5,padx=10, pady=10, sticky="e" ) 
        self.t1_lbl5 = Label(self.tab1, text='')  
        self.t1_lbl5.grid(column=0, row=6, padx=10, pady=10, sticky="w")
        self.t1_b5 = Button(self.tab1, text='Настройки по умолчанию', command=self.t1_b6_clicked)  
        self.t1_b5.grid(column=1, row=1,padx=10, pady=10, sticky="w" )
        self.t1_b6 = Button(self.tab1, text='Сохранить настройки', command=self.t1_b5_clicked)  
        self.t1_b6.grid(column=1, row=2,padx=10, pady=10, sticky="w" )
        self.tab_control.pack(expand=1, fill='both') 
    
    def t1_b6_clicked(self):
        if not self.is_first:
            with open('settings.pickle', 'rb') as f:
                t= pickle.load(f)
                self.path_access=t[0]
                self.tab_read=t[1]
                self.tab_write=t[2]
                self.t1_lbl3.configure(text=self.path_access ) 
                self.t1_txt1.delete(0, last=END)
                self.t1_txt1.insert(0, self.tab_read)
                self.t1_txt2.delete(0, last=END)
                self.t1_txt2.insert(0, self.tab_write)
                messagebox.showinfo("Данные заполненны", "Выбор настроек по умолчанию успешно выполнен.")
        else:
            messagebox.showerror("Ошибка!", "Файл с сохраненными настройками не найден! ")
            
    def t1_b5_clicked(self):
        if self.check_data():
                with open('settings.pickle', 'wb') as f:
                    pickle.dump([self.path_access, self.tab_read, self.tab_write], f)
                    messagebox.showinfo("Данные сохранены", "Сохранение настроек по умолчанию успешно выполнено.")  
                    self.is_first= False

    def check_data(self):
        if self.path_access=='':
            messagebox.showerror("Ошибка!", "Не выбран  файл access ")
            return 0
        s = self.t1_txt1.get()
        self.tab_read= s
        if len(s)==0:
            messagebox.showerror("Ошибка!", "Не введено имя таблицы для чтения")
            return  0
        s = self.t1_txt2.get()
        self.tab_write= s
        if len(s)==0:
            messagebox.showerror("Ошибка!", "Не введено имя таблицы для записи")
            return  0
        return 1
    
    def t1_b3_clicked(self):
        if self.check_data():            
            messagebox.showinfo("Файлы выбраны", "Запуск соединения с сервером...")
            self.time=0
            self.run = True
    
    def t1_b1_clicked(self):
        self.path_access =  str(filedialog.askopenfilename())
        self.t1_lbl3.configure(text=self.path_access ) 
    
    def t1_b4_clicked(self):
        messagebox.showinfo("Остановка соединения с сервером ", "Остановка соединения с сервером успешно выполнена")
        self.run = False
        self.t1_lbl5.configure(text="")
    def for_test_data(self):
        self.t1_b6_clicked()
        conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' +self.path_access+' ;')
        cursor = conn.cursor()
        request_data = {}
        cursor.execute('select * from '+self.tab_read)
        for i,row in enumerate(cursor.fetchall()):
                request_data["row"+str(i+1)]=row
        with open('test.pickle', 'wb') as f:
                    pickle.dump(request_data, f)
        
                
    def connect(self): 
        if self.run:
            conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' +self.path_access+' ;')
            cursor = conn.cursor()
            #post request
            request_data = {}
            cursor.execute('select * from '+self.tab_read)
            for i,row in enumerate(cursor.fetchall()):
                request_data["row"+str(i+1)]=str(row)
            r =requests.post(self.url, json =request_data)
            print(r)
            #get request
    #         cursor.execute("DELETE FROM Tab2")
    #         request_answer = requests.get(url)
    #         print(request_answer.encoding )
    #         print(request_answer.text)
    #         request_data = request_answer.text.replace('\n','') 
    #         print(json.loads(request_data))


    #         for i in range(len(request_data)):
    #             row = request_data['row'+str(i+1)]
    #             cursor.execute("INSERT INTO "+tab_write+" VALUES ('" + row +" ');")
    #             conn.commit()
    #         cursor.close()
            self.time+=5
            self.t1_lbl5.configure(text="Время соединения с сервером - "+str(self.time )+" секунд")
        self.window.after(5000, self.connect)

        
def main():
    app = Desctop()
    app.for_test_data()
    app.start()
    
    
main()

































# is_first= not( os.path.exists('settings.pickle'))
# path_access=''
# path_exel=''
# tab_read=''
# tab_write=''
# run=False
# time = 0
# url = 'http://176.58.60.36/kokoro/connect_to_server/'
# if not is_first:
#     with open('settings.pickle', 'rb') as f:
#         t= pickle.load(f)
#     path_access=t[0]
#     path_exel=t[1]

        
# def t2_b1_clicked():
#     global path_access
#     path_access =  filedialog.askopenfilename()
#     t2_lbl3.configure(text=str(path_access )) 
    
# def t2_b2_clicked():
#     global path_exel
#     path_exel =  filedialog.askopenfilename()
#     t2_lbl4.configure(text=str(path_exel )) 
    
# def t2_b3_clicked():

#     if path_access=='':
#         messagebox.showerror("Ошибка!", "Не выбран  файл access ")
#         return 1
#     s = t2_txt.get()
#     global tab_read
#     tab_read= s
#     if len(s)==0:
#         messagebox.showerror("Ошибка!", "Не введено имя таблицы для чтения")
#         return  1
#     s = t2_txt_2.get()
#     global tab_write
#     tab_write= s
#     if len(s)==0:
#         messagebox.showerror("Ошибка!", "Не введено имя таблицы для записи")
#         return  1
#     with open('settings.pickle', 'wb') as f:
#         pickle.dump([path_access,path_exel], f)   
#     messagebox.showinfo("Файлы выбраны", "Запуск соединения с сервером...")
#     global time
#     time=0
#     global run
#     run = True
    

# def t2_b4_clicked():
     
#     messagebox.showinfo("Остановка соединения с сервером ", "Остановка соединения с сервером успешно выполнена")
#     global run
#     run = False
#     t2_lbl5.configure(text="")

    
# def connect():
#     print("after")
#     global run, url, path_access, tab_read, tab_write 
#     if run:
#         conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' +path_access+' ;')
#         cursor = conn.cursor()
#         #post request
#         request_data = {}
#         cursor.execute('select * from '+tab_read)
#         for i,row in enumerate(cursor.fetchall()):
#             request_data["row"+str(i+1)]=str(row)
#         requests.post(url, json =request_data)

#         #get request
# #         cursor.execute("DELETE FROM Tab2")
# #         request_answer = requests.get(url)
# #         print(request_answer.encoding )
# #         print(request_answer.text)
# #         request_data = request_answer.text.replace('\n','') 
# #         print(json.loads(request_data))

        
# #         for i in range(len(request_data)):
# #             row = request_data['row'+str(i+1)]
# #             cursor.execute("INSERT INTO "+tab_write+" VALUES ('" + row +" ');")
# #             conn.commit()
# #         cursor.close()
#         global time
#         time+=15
#         t2_lbl5.configure(text="Время соединения с сервером - "+str(time )+" секунд")
#     print("after_fin")
#     global window
#     window.after(5000, connect)


# window = Tk()
# window.after(5000, connect)
# window.title("Связь с сервером")  
# window.geometry('650x300')  

# tab_control = ttk.Notebook(window)  
# tab2 = ttk.Frame(tab_control) 
  

# tab_control.add(tab2, text='Настройка') 
# # lbl1 = Label(tab1, text='Настройки заданы по умолчанию               ')  
 
# # btn = Button(tab1, text='Запустить', command=clicked_down)  
# # btn.grid(column=1, row=0,padx=10, pady=10, sticky="w" ) 
# # btn = Button(tab1, text='Остановить', command=clicked_up)  
# # btn.grid(column=1, row=0,padx=10, pady=10, sticky="w" ) 

# #tab2

# t2_b1 = Button(tab2, text='Выбрать базу данных', command=t2_b1_clicked)  
# t2_b1.grid(column=0, row=1,padx=10, pady=10, sticky="w" ) 
# t2_lbl3 = Label(tab2, text='')  
# t2_lbl3.grid(column=0, row=2, padx=10, pady=10, sticky="w")
# t2_lbl1 = Label(tab2, text='Имя таблицы для записи:')  
# t2_lbl1.grid(column=0, row=3, padx=10, pady=10, sticky="w")
# t2_txt = Entry(tab2,width=30)  
# t2_txt.grid(column=1, row=3, padx=10, pady=10, sticky="w")

# t2_lbl2 = Label(tab2, text='Имя таблицы для чтения:')  
# t2_lbl2.grid(column=0, row=4, padx=10, pady=10, sticky="w")
# t2_txt_2 = Entry(tab2,width=30)  
# t2_txt_2.grid(column=1, row=4, padx=10, pady=10, sticky="w")
# # t2_b2 = Button(tab2, text='Выберите файл exel', command=t2_b2_clicked)  
# # t2_b2.grid(column=0, row=5,padx=10, pady=10, sticky="w" ) 
# # t2_lbl4 = Label(tab2, text='')  
# # t2_lbl4.grid(column=0, row=6, padx=10, pady=10, sticky="w")

# t2_b3 = Button(tab2, text='Запустить',background="#99FF99", command=t2_b3_clicked)  
# t2_b3.grid(column=0, row=5,padx=10, pady=10, sticky="w" ) 

# t2_b4 = Button(tab2, text='Остановить',background="#FF6666", command=t2_b4_clicked)  
# t2_b4.grid(column=1, row=5,padx=10, pady=10, sticky="e" ) 
# t2_lbl5 = Label(tab2, text='')  
# t2_lbl5.grid(column=0, row=6, padx=10, pady=10, sticky="w")
# tab_control.pack(expand=1, fill='both') 
# window.mainloop()




