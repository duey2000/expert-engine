#******VERSION AFTER WORKING WITH ALEX*******
#******DO NOT CHANGE*********************

import psycopg2
import PySimpleGUI as sg
# import re
import sys

class Login:
    def __init__(self,f_name='',l_name='',email_address='',department='',user_name='',user_id='',password=''):
        self.f_name = f_name
        self.l_name = l_name
        self.email_address = email_address
        self.department = department
        self.department_name = ''
        self.user_name = user_name
        self.user_id = user_id
        self.password = password
        self.email_chars = '@.'
        self.special = '[]!@?#$%-&*=_'
        self.password = password
        self.user_check_flag = False
        self.email_check_flag = False

    def Register_Input_Screen(self):
        try:
            conn = psycopg2.connect(
            database = 'facilities_service_request',
            user = 'postgres',
            password = 'Eagle3614',
            host = 'localhost',
            port = '5432'
            )
            conn.autocommit = True
            cur = conn.cursor()
            if conn is not None:
                print("[+] Connection established!")
                try:
                    cur.execute(f"""SELECT user_id FROM users
                                    ORDER BY user_id DESC
                                    FETCH FIRST ROW ONLY;""")
                    self.user_id = cur.fetchone()
                    self.user_id = self.user_id[0]+1
                except (Exception,conn.DatabaseError) as error:
                    #Login.Error()
                    pass
        except (Exception,conn.DatabaseError) as error:
            #Login.Error()
            print('[-] Query unsuccessful!')
        finally:
            cur.close()
            conn.close()
            print("[+] Connection closed.")

        layout1 = [[sg.Text("Please fill out the information below.")],
                    [sg.Text("First name", size=(25,1)), sg.InputText(size=(30,1), key='FIRST_NAME')],
                    [sg.Text("Last name", size=(25,1)), sg.InputText(size=(30,1), key='LAST_NAME')],
                    [sg.Text("Email address", size=(25,1)), sg.InputText(size=(30,1), key='EMAIL')],
                    [sg.Text("Choose your department",size=(25,1)), sg.Combo(["Engineering",
                                                                                "Executive",
                                                                                "Housekeeping",
                                                                                "Human Resources",
                                                                                "Information Technology",
                                                                                "Marketing",
                                                                                "Outbound Sales"], key='DEPARTMENT',size=(30,1))],
                    [sg.Text("Choose your User name", size = (25,1)), sg.InputText(size=(30,1),key='USER_NAME')],
                    [sg.Text(key = 'OUTPUT1',font = 'Times 12 bold',text_color='Blue',size=(60,))],
                    [sg.Button("Submit",size=(10, 1), key='SUBMIT', pad=((5, 0), (5, 2))), sg.Button("Cancel",size=(10, 1), key='CANCEL', pad=((5,0),(5,2)))]]
        register_window1 = sg.Window("Register Your Account",layout1)

        while True: 
            event,values = register_window1.read() 
            if event == 'CANCEL' or event == sg.WIN_CLOSED:
                break
                
                # Login.Login_Screen(self)
            else:
                self.f_name = str(values['FIRST_NAME']).lower().strip()
                self.l_name = str(values['LAST_NAME']).lower().strip()
                self.email_address = str(values['EMAIL']).strip()
                self.user_name = str(values['USER_NAME'])
                self.user_input_full_name = f"{self.f_name} {self.l_name}"
                if self.f_name == '' or self.l_name =='' or self.email_address == '' or self.department_name == '' or self.user_name == '':                        
                        register_window1['OUTPUT1'].update("All fields must be completed.")
                if self.email_check_flag == False:
                    e_list = []                  
                    for e in self.email_address:
                        e_list.extend(e)
                    for e2 in self.email_chars:
                        if e2 not in e_list:
                            register_window1['OUTPUT1'].update("Please enter a valid email address.")
                            event,values = register_window1.read()
                        else:
                            register_window1['OUTPUT1'].update(" ")
                            event,values = register_window1.read()
                            self.email_check_flag = True
                if self.email_check_flag == True:    
                    if self.user_check_flag == False:
                        try:
                            conn = psycopg2.connect(
                            database = 'facilities_service_request',
                            user = 'postgres',
                            password = 'Eagle3614',
                            host = 'localhost',
                            port = '5432'
                            )
                            conn.autocommit = True     
                            if conn is not None:
                                print("[+] Connection established!")
                                cur = conn.cursor()
                                try:             
                                    cur.execute(f"""SELECT first_name, last_name, email_address, user_name FROM users
                                                    WHERE 
                                                    first_name = '{self.f_name}' AND
                                                    last_name = '{self.l_name}' OR
                                                    email_address = '{self.email_address}' OR
                                                    user_name = '{self.user_name}';""")
                                    usr = (cur.fetchall())
                                    for u in usr:      
                                        user_input = tuple(usr)
                                        user_input2 =[]
                                        for u2 in user_input:
                                            user_input2.extend(u2)
                                        if self.f_name==user_input2[0] and self.l_name==user_input2[1]:
                                            print("same name")                                   
                                            register_window1['OUTPUT1'].update("This name is already associated with another account.")
                                            event,values = register_window1.read()
                                        else:                                                    
                                            if self.email_address == user_input2[2]:
                                                print("same email")
                                                register_window1['OUTPUT1'].update("This email address is already associated with another account.")
                                                event,values = register_window1.read()
                                            else:
                                                if self.user_name == user_input2[3]:
                                                    print("same username")
                                                    register_window1['OUTPUT1'].update("This user name is already associated with another account.")
                                                    event,values = register_window1.read() 
                                                else:
                                                    self.user_check_flag = True
                                                    break        
                                except (Exception,conn.DatabaseError) as error:
                                    #Login.Error()
                                    pass
                        except (Exception,conn.DatabaseError) as error:
                            #Login.Error
                            pass
                        finally:
                            cur.close()
                            conn.close()
                            print("[+] Connection closed.")                                
                    else:
                        print("Moving On")
                        # Login.Password_Set(self)
                        break  
                else:
                    if values['DEPARTMENT'] == "Engineering":
                        self.department = 10
                        self.department_name = 'Engineering'
                    elif values['DEPARTMENT'] == "Executive":
                        self.department = 20
                        self.department_name = 'Executive'
                    elif values['DEPARTMENT'] == "Housekeeping":
                        self.department = 30
                        self.department_name = 'Housekeeping'
                    elif values['DEPARTMENT'] == "Human Resources":
                        self.department = 40
                        self.department_name = 'Human Resources'
                    elif values['DEPARTMENT'] == "Information Technology":
                        self.department = 50
                        self.department_name = 'Information Technology'
                    elif values['DEPARTMENT'] == "Marketing":
                        self.department = 60
                        self.department_name = 'Marketing'
                    elif values['DEPARTMENT'] == "Outbound Sales":
                        self.department = 70
                        self.department_name = 'Outbound Sales'

run = Login()
run.Register_Input_Screen()