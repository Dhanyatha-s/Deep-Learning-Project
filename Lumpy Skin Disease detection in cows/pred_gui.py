from tkinter import *
import tkinter as tk
import os
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
import shutil
from PIL import Image, ImageTk
from tensorflow.keras.models import load_model
import cv2
import numpy as np
import smtplib
top = Tk()
top.geometry('600x400')
top.configure(background='blue')
top.title("Dr. Lampy Disease")

def Load_image():
    def openphoto():
        def analysis():
            model_name=var.get()
            class_names = ["Healthy","Lampy"] # fill the rest
            if model_name=="CNN":
                model = load_model('model_cnn.h5')
                model.compile(loss='categorical_crossentropy',
                          optimizer='adam',
                          metrics=['accuracy'])
            elif model_name=="VGG16":
                model = load_model('vgg16_model.h5')
                model.compile(loss='categorical_crossentropy',
                          optimizer='adam',
                          metrics=['accuracy'])
            else:
                model = load_model('inceptionv3_model.h5')
                model.compile(loss='categorical_crossentropy',
                          optimizer='adam',
                          metrics=['accuracy'])
            
            img = cv2.imread(fileName)
            img = cv2.resize(img,(224,224))
            img = np.reshape(img,[1,224,224,3])
            result =np.argmax(model.predict(img),axis=-1)
            #classes = np.argmax(model.predict(img), axis = -1)
            result=result[0]
            names=""
            if result==0:
                names=class_names[0]

            elif result==1:
                names=class_names[1]
                import mysql.connector
                # Establish a connection to the database
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="vdoctor"
                )
                # Create a cursor object
                cursor = conn.cursor()

                # Execute the query to select distinct values from the "area" column
                cursor.execute("SELECT DISTINCT area FROM doctors")

                # Fetch all the results and store them in a variable
                results = cursor.fetchall()
                area=[]
                # Print the unique values of the "area" column
                for r in results:
                    area.append(r[0])
                # Close the cursor and connection to the database
                cursor.close()
                conn.close()
            
            option.destroy()
            Lab.configure(text="Prediction with "+str(model_name)+":"+str(names))
            def button_clicked():
                area = option_variable.get()
                import mysql.connector
                # Establish a connection to the database
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="vdoctor")
                # Create a cursor object
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM doctors WHERE area = %s", (area,))
                results = cursor.fetchall()
                message='You can Contact fallowing doctors\n'
                for result in results:
                    message=message+"Doctor:"+result[1]+"\tContact:"+result[2]+"\n"
                email = email_entry.get()
                usermail="yashu.m.k7@gmail.com"
                s = smtplib.SMTP('smtp.gmail.com', 587)
                s.starttls()
                s.login("yashu.m.k7@gmail.com","gpsfckmdfhgakvqq")
                s.sendmail(usermail,email,message)
                s.quit()
                messagebox.showinfo("Success", "Email sent successfully!")
                
                
            if result==1:
                options=area
                option_variable = tk.StringVar()
                button2.destroy()
                # Set the default value for the option menu to the first option in the list
                option_variable.set("Select Area")
                # Create the option menu
                option_menu = tk.OptionMenu(top1, option_variable, *options)
                option_menu.grid(row=3, column=0)
                email_label = tk.Label(top1, text="Enter Email:")
                email_label.grid(row=4, column=0)
                email_entry = tk.Entry(top1)
                email_entry.grid(row=5, column=0)
                button = tk.Button(top1, text="Submit", command=button_clicked)
                button.grid(row=6, column=0)
            
            
        fileName = askopenfilename(initialdir='./', title='Select image for analysis ',
                               filetypes=[('image files', '*')])
        dst = "./dataset"
        shutil.copy(fileName, dst)
        load = Image.open(fileName)
        render = ImageTk.PhotoImage(load)
        img = tk.Label(image=render, height="250", width="500")
        img.image = render
        img.place(x=0, y=0)
        img.grid(column=0, row=1, padx=10, pady = 10)
        button1.destroy()
        var = StringVar(top1)
        var.set("Select Model") # initial value

        option = OptionMenu(top1, var, "CNN", "VGG16") # Declaring the OptionMenu (Drop-Down list) widget
        option.config(bg = "violet")
        option.config(fg = "black")
        option.config(font=('algerian',10,'bold'))
        option.config(width=12)
        option.grid(column=0, row=2, padx=10, pady = 10)
        button2 = tk.Button(text="Analyse Image", command=analysis)
        button2.grid(column=0, row=3, padx=10, pady = 10)
        Lab=Label(top1,text="")
        Lab.grid(row=2,column=0,padx=10, pady = 10)
    top.destroy()
    top1 = Tk()
    top1.geometry('600x600')
    #top1.configure(background='blue')
    top1.title("Dr. Lampy Disease")
    button1 = tk.Button(top1,text="Get Photo", command = openphoto)
    button1.place(x=200, y=300)
    top1.mainloop()    
def fun1():  
    messagebox.showinfo("Selection", "Resnet50 Selected")
    
    Load_image()
  
b1 = Button(top, text="Lets Start", command=Load_image  ,fg="red"  ,bg="yellow"  ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))    
b1.place(x=200, y=300)
top.mainloop()  
