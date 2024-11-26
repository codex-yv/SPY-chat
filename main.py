from tkinter import*
import customtkinter as ctk
from tkinter import messagebox
from tkinter import simpledialog
import pyautogui
import socket
import threading
win=Tk()
sidee=0
client_name_list=[]
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        


def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            label =Label(frame, text='', relief="raised",bd=2)
            label2=Label(frame,text='Client',bg='#e8f8f5',font=('Cascadia Code',10,'bold'))
            label.config(text=message.strip(),bg='white')
            label.pack(pady=(10,0),ipadx=10,anchor='w',ipady=5)
            label2.pack(anchor='w')
            frame.update_idletasks()
            main_canvas.config(scrollregion=main_canvas.bbox("all"))
            pyautogui.scroll(-2000000)
        except:
            messagebox.showerror("Recieve Error","Error receiving message!")
            break

def send_messages(client_socket):
    try:
        message = entry_area.get('1.0',END).strip()
        client_socket.send(message.encode('utf-8'))
        entry_area.delete('1.0',END)
        pyautogui.scroll(-2000000)
        
    except OSError:
        entry_area.configure(state=DISABLED)
            
            
def start_client():
    try:
        global client
        client.connect(('192.168.1.2', 5555))

        print("Connected to the server. You can start chatting!")

        threading.Thread(target=receive_messages, args=(client,)).start()

    except ConnectionRefusedError:
        status_icon.configure(fg_color='#e74c3c') 
        status_text.config(text='Server:Offline')          
            
            
def on_mouse_wheel(event):
        main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
def inputs():
    global  client,client_name_list
    main_canvas.create_window((10, 10), window=frame, anchor="nw")
    inn=entry_area.get('1.0',END)
    
    label =Label(frame, text='', relief='raised',bd=2,fg='white',font=('Cascadia Code',10,'bold'))
    label2=Label(frame,text=client_name_list[0],bg='#e8f8f5',font=('Cascadia Code',10,'bold'))
    label.config(text=inn.strip(),bg='#8e44ad')
    threading.Thread(target=send_messages, args=(client,)).start()
  
    label.pack(pady=(10,0),ipadx=10,anchor='w',ipady=5)
    label2.pack(anchor='w')
    frame.update_idletasks()
    main_canvas.config(scrollregion=main_canvas.bbox("all"))



def inputs1(events):
    global client_name_list, client
    main_canvas.create_window((10, 10), window=frame, anchor="nw")
    inn=entry_area.get('1.0',END)

    label =Label(frame, text='', relief='raised',bd=2,fg='white',font=('Cascadia Code',10,'bold'))
    label2=Label(frame,text=client_name_list[0],bg='#e8f8f5',font=('Cascadia Code',10,'bold'))
    label.config(text=inn.strip(),bg='#8e44ad')
    threading.Thread(target=send_messages, args=(client,)).start()
    
    label.pack(pady=(10,0),ipadx=10,anchor='w',ipady=5)
    label2.pack(anchor='w')
    frame.update_idletasks()
    main_canvas.config(scrollregion=main_canvas.bbox("all"))

    

win.geometry("800x500")
win.config(bg='#85929e')
win.title("SPY CHAT copy")
icon_path='assets\\meetme.ico'
win.iconbitmap(icon_path)

status_frame=Frame(win,height=30,bg='#34495e')
status_frame.propagate(False)
status_frame.place(relx=0.0,rely=0.003,relwidth=1.0)

status_icon=ctk.CTkLabel(status_frame,text='',fg_color='#28b463',corner_radius=10,height=10,width=10)
status_icon.pack(side=LEFT,padx=20)

status_text=Label(status_frame,text="Server:Online",fg='white',bg='#34495e',font=('Cascadia Code',10,'bold'))
status_text.pack(side=LEFT)

start_client()

client_name=simpledialog.askstring('Client Name:','Enter your Name:')
if client_name:
    client_name_list.append(client_name)
else:
    client_name_list.append('Identity Hidden')

main_canvas=Canvas(win,bg='#e8f8f5',relief='sunken',bd=3)
main_canvas.pack(side=LEFT,fill=BOTH,expand=True,pady=(35,60))
v_scrollbar =Scrollbar(win, orient="vertical", command=main_canvas.yview)
v_scrollbar.pack(side=RIGHT, fill="y",pady=(35,60))

main_canvas.config(yscrollcommand=v_scrollbar.set)
frame = Frame(main_canvas,bg='#e8f8f5')

main_canvas.create_window((10, 10), window=frame ,anchor='w')
chat_frame=Frame(win,bg='white',height=50,width=800,relief='ridge',bd=2)
chat_frame.propagate(False)
chat_frame.place(relx=0.0,rely=0.889)
entry_area=ctk.CTkTextbox(chat_frame,border_color='#48c9b0',border_width=2)
entry_area.pack(side=LEFT,fill=BOTH,expand=True,pady=3,padx=4)
# entry_area.insert('1.0','',END)
button=ctk.CTkButton(chat_frame,text='Send',font=('Bahnschrift',15,'bold'),fg_color='#58d68d',text_color='white',command=inputs,width=100)
button.pack(side=RIGHT,ipadx=1,fill=Y,pady=2,padx=4)
win.bind("<Shift-Return>", lambda event: inputs1(event))
main_canvas.bind_all("<MouseWheel>", on_mouse_wheel)  # Windows and macOS

win.mainloop()