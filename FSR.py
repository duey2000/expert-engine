import PySimpleGUI as sg
import sys
import psycopg2
import pandas as pd
import os
import re
import datetime
from time import strftime,localtime
from csv import writer

#Sets the format for the user interface or 'GUI'
sg.set_options(font='Times 12')
sg.theme('DarkBlue3')

class Login:
    def __init__(self,f_name='',l_name='',email_address='',department='',user_name='',user_id='',password='',floor='',service='',details='',time_stamp='',date_stamp=''):
        self.f_name = f_name
        self.l_name = l_name
        self.email_address = email_address
        self.department = department
        self.user_name = user_name
        self.user_id = user_id
        self.password = password
        self.email_chars = '@.'
        self.special = '[]!@?#$%-&*=_'
        self.regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'        
        self.floor = floor
        self.service = service
        self.details = details
        self.time_stamp = time_stamp
        self.date_stamp = date_stamp
        self.start_date = ''
        self.end_date = ''
        self.report = ''

#An error message that is displayed if there is a communication issue between Python and the PostgreSQL database
    def Error(self):
        layout_error = [[sg.Text("There was an error connecting to the database. Please try again or contact the system administrator.",font='Times 16',size=(30,3))],
                        [sg.Button("Okay",size=(10,1),key='OKAY',)]]
        error_window = sg.Window("Error",layout_error,element_justification='center')
        event,values = error_window.read()
        if event == 'OKAY' or event == sg.WIN_CLOSED:
            error_window.close()

#The main login screen when the app is opened
    def Login_Screen(self): 
#Open the login window
        layout1 = [[sg.Text("Welcome to the Physicians Mutual Facilities Service Request app.",size=(50,1))],
                   [sg.Text("Log in", size=(10,1))],
                   [sg.Text("User Name", size=(10,1)), sg.InputText(size=(25,1),key='USER_NAME')],
                   [sg.Text("Aren't registered? Click here.", font='Times 12 underline', tooltip=("Register a new account"), enable_events=True, click_submits=True, size=(35, 1), key='REGISTER')],
                   [sg.Text("Password", size=(10, 1)), sg.InputText(size=(25, 1), password_char='*',key='PASSWORD')],
                   [sg.Submit(size=(10,1),key='SUBMIT',pad=((5,0),(5,2))), sg.Exit(size=(10,1), pad=((5,0),(5,2)), key='EXIT')]]
        login_window = sg.Window("Login",layout1)
        while True:
            event,values = login_window.read()
            #If the user wants to leave the program
            if event == 'EXIT' or event== sg.WIN_CLOSED:
                login_window.close()
                sys.exit()
            #If the user enters their user name and password and hits the submit button
            if event == 'SUBMIT':
                self.user_name = values['USER_NAME']
                self.password = values['PASSWORD']
                try:
                    conn = psycopg2.connect(
                    database = 'facilities_service_request',
                    user = 'postgres',
                    password = 'Eagle3614',
                    host = 'localhost',
                    port = '5432'
                    )
                    if conn is not None:
                        #Successful connection to Database
                        cur = conn.cursor()                        
                        #Attempting to match the user_name to a user_name in DB
                        try:
                            cur.execute(f"SELECT user_name,password FROM users WHERE user_name = '{self.user_name}';")
                            usr = cur.fetchall()
                            for u in usr:
                                print(u)

                            #If the username and password provided by user both are found in the database and match correctly, pop up welcome window will appear then move to the next window
                            if u == (self.user_name,self.password):
                                cur.execute(f"SELECT first_name,last_name,email_address FROM users WHERE user_name = '{self.user_name}';")
                                usr_information = (cur.fetchall())
                                usr_info_list = list(usr_information)
                                usr_info_list2 = []
                                for u in usr_info_list:
                                    usr_info_list2.extend(u)
                                    #Pop up window welcomes the user by name
                                    layout_welcome= [[sg.Text(f"Welcome {usr_info_list2[0].title()} {usr_info_list2[1].title()}",font='Times 16',justification='center', size=(20,2))]]
                                    welcome_window = sg.Window("Welcome",layout_welcome,auto_close=True,auto_close_duration=2)
                                    login_window.close()
                                    event,values = welcome_window.read()
                                    welcome_window.close()  
                                    break                                   
                                cur.close()
                                conn.close()
                            #If the information is not found in the database or the password and ID are not correctly matched then the user is returned to the login screen
                            else:
                                Login.Try_Again(self)
                                event,values = welcome_window.read()
                        #If there is an issue with the query or if the connection has an error then an error window will pop up                                
                        except (Exception,conn.DatabaseError) as error:                           
                            Login.Try_Again(self)
                        cur.close()
                        conn.close()
                    else:
                        pass
                except (Exception,psycopg2.DatabaseError) as error:   
                    print(error) 
                    conn.close()
                Login.Verify_Login(self)
#User selects register a new account
            if event == 'REGISTER':
                login_window.close()
                Login.Register_Screen(self)

#Successful login 
    def Verify_Login(self):
        #application is connecting to the server to verify user ID and password
        try:
            conn = psycopg2.connect(
            database = 'facilities_service_request',
            user = 'postgres',
            password = 'Eagle3614',
            host = 'localhost',
            port = '5432'
            )
            if conn is not None:
                #Successful connection to Database
                cur = conn.cursor()        
                #Attempting to match the user_name to a user_name in DB
                try:
                    cur.execute(f"SELECT user_name,password FROM users WHERE user_name = '{self.user_name}';")
                    usr = cur.fetchall()
                    for u in usr:
                        print(u)
                    #If the username and password provided by user both are found in the database and match correctly, pop up welcome window will appear then move to the next window
                    if u == (self.user_name,self.password):
                        cur.execute(f"SELECT first_name,last_name,email_address FROM users WHERE user_name = '{self.user_name}';")
                        usr_information = (cur.fetchall())
                        usr_info_list = list(usr_information)
                        usr_info_list2 = []
                        for u in usr_info_list:
                            usr_info_list2.extend(u)
                            Login.Map(self)                       
                        cur.close()
                        conn.close()
                    #If the information is not found in the database or the password and ID are not correctly matched then the user is returned to the login screen
                    else:
                        layout_invalid_user= [[sg.Text("You have entered an invalid User ID and/or Password. Please try again.",justification='center', size=(55,2))],
                                                [sg.Button("Try again",size=(10,1),pad=(180,0),key='TRY_AGAIN')]]
                        invalid_user_window = sg.Window("Invalid Login",layout_invalid_user,auto_close=True,auto_close_duration=3)
                        event,values = invalid_user_window.read()
                        if event == 'TRY_AGAIN' or event == sg.WIN_CLOSED:
                            invalid_user_window.close()
                            Login.Login_Screen(self)
                        invalid_user_window.close()
                        Login.Login_Screen(self)

                #If there is an issue with the query or if the connection has an error then an error window will pop up                                
                except (Exception,conn.DatabaseError) as error:                           
                    pass
                cur.close()
                conn.close()
            else:
                pass
        except (Exception,psycopg2.DatabaseError) as error:   
            print(error) 
            conn.close()

#Registering a new account
    def Register_Screen(self):
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
            elif event == 'SUBMIT':
                if values['FIRST_NAME'] == '' or values['LAST_NAME'] == '':
                    register_window1['OUTPUT1'].update("You must enter a first and last name.")
                    continue
                elif values['EMAIL'] == '':
                    register_window1['OUTPUT1'].update("Please enter your email address.")
                    continue
                elif values ['DEPARTMENT'] == '':
                    register_window1['OUTPUT1'].update("Please select your department.")
                    continue
                elif values['USER_NAME']== '':
                    register_window1['OUTPUT1'].update("Please enter a username.")
                    continue
                else:
                    if values['EMAIL'] !='':
                        if(re.search(self.regex,values['EMAIL'])) == None:   
                            register_window1['OUTPUT1'].update("Please enter a valid email address.")
                            continue
                        else:                       
                            self.f_name = str(values['FIRST_NAME']).lower().strip()
                            self.l_name = str(values['LAST_NAME']).lower().strip()
                            self.email_address = str(values['EMAIL']).strip()
                            self.user_name = str(values['USER_NAME'])
                            if values['DEPARTMENT'] == "Engineering":
                                self.department = 10
                            elif values['DEPARTMENT'] == "Executive":
                                self.department = 20
                            elif values['DEPARTMENT'] == "Housekeeping":
                                self.department = 30
                            elif values['DEPARTMENT'] == "Human Resources":
                                self.department = 40
                            elif values['DEPARTMENT'] == "Information Technology":
                                self.department = 50
                            elif values['DEPARTMENT'] == "Marketing":
                                self.department = 60
                            elif values['DEPARTMENT'] == "Outbound Sales":
                                self.department = 70
                            print(f"Name: {self.f_name} {self.l_name}\nEmail: {self.email_address}\nDepartment: {self.department}\nUser Name: {self.user_name}\n")
                            register_window1.close()
                            Login.Password_Set(self)

#Setting a password for a new account
    def Password_Set(self):
            set_password_layout = [[sg.Text("Please choose a new password.",size=(40,1))],
                                    [sg.Text("Your new passord must have the following attributes:",size=(40,1))],
                                    [sg.Text("-Between 6 and 12 characters long.",size=(40,1))],
                                    [sg.Text("-Contains at least one uppercase and one lowercase letter",size=(40,1))],
                                    [sg.Text("Enter your new password:",size=(25,1)), sg.InputText(size=(30,1),password_char='*',key='PASSWORD')],
                                    [sg.Text("Enter your new password again:",size=(25,1)), sg.InputText(size=(30,1),password_char='*',key='PASSWORD2')],
                                    [sg.Text(key = 'OUTPUT2',font = 'Times 12 bold',text_color='Blue',size=(60,))],
                                    [sg.Button("Submit",size=(10,1), key='SUBMIT'),sg.Button("Cancel",size=(10,1),key=("CANCEL"))]]
            set_pass_window = sg.Window('Create your password',set_password_layout)
            while True:
                event,values = set_pass_window.read()  
                if event == 'CANCEL' or event == sg.WIN_CLOSED:
                    break
                elif event == 'SUBMIT':
                    if values['PASSWORD'] == '' or values['PASSWORD2'] == '':
                        set_pass_window['OUTPUT2'].update("Password cannot be blank.")
                        continue
                    if values['PASSWORD'] != values['PASSWORD2']:
                        set_pass_window['OUTPUT2'].update("The passwords you've entered do not match. Please try again.")
                        event,values = set_pass_window.read()        
                        continue
                    elif len(values['PASSWORD']) < 6 or len(values['PASSWORD']) > 12:
                        set_pass_window['OUTPUT2'].update("Your password must be between 6 and 12 characters. Please try again.")
                        event,values = set_pass_window.read()  
                        continue                                       
                    elif values['PASSWORD'].upper() == values['PASSWORD']:
                        set_pass_window['OUTPUT2'].update("Your password must contain at least one lowercase letter. Please try again.")
                        event,values = set_pass_window.read()   
                        continue                         
                    elif values['PASSWORD'].lower() == values['PASSWORD']:
                        set_pass_window['OUTPUT2'].update("Your password must contain at least one uppercase letter. Please try again.")
                        event,values = set_pass_window.read()
                        continue
                    else:
                        self.password = values['PASSWORD']
                        set_pass_window.close()
                        Login.Verify_Screen(self)

#Generates a new user ID number based on the highest user ID number that already exists in the database
    def Fetch_User_ID(self):
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
            Login.Communicate_New_User_To_Table(self)

#Checks to see if the account information entered matches any already existing account (email, first+last name, email)
    def Existing_User_Check(self):
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
                    cur.execute(f"""SELECT first_name, last_name FROM users
                                WHERE first_name = '{self.f_name}' 
                                AND last_name = '{self.l_name}';""")
                    user_check_name = cur.fetchone()
                    self.user_input_full_name = str(self.user_input_full_name).strip('([])')
                    self.user_input_full_name = re.findall(r'\w+',self.user_input_full_name)
                    self.user_check_name = str(self.user_check_name).strip('([])')
                    self.user_check_name = re.findall(r'\w+',user_check_name)
                    if self.user_check_name == self.user_input_full_name:
                        self.user_check_flag = True
                except (Exception,conn.DatabaseError) as error:
                    #Login.Error()
                    pass
        except (Exception,conn.DatabaseError) as error:
            pass
        finally:
            cur.close()
            conn.close()
#This checks for a user with this existing email address
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
                try:
                    cur.execute(f"""SELECT email_address FROM users
                                WHERE email_address = '{self.email_address}';""")
                    user_check_email = cur.fetchone()
                    user_check_email = self.user_check_email[0]               
                    if user_check_email == self.email_address:
                        self.user_check_flag2 = True
                except (Exception,conn.DatabaseError) as error:
                    #Login.Error()
                    pass
        except (Exception,conn.DatabaseError) as error:
            pass
        finally:
            cur.close()
            conn.close()
#This checks if an account exists with the username that the user is trying to register
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
                    try:
                        cur.execute(f"""SELECT user_name FROM users
                                    WHERE user_name = '{self.user_name}';""")
                        user_check_username = cur.fetchone()
                        user_check_username = user_check_username[0]               
                        if user_check_username == self.user_name:
                            user_check_flag3 = True
                    except (Exception,conn.DatabaseError) as error:
                        #Login.Error()
                        pass
            except (Exception,conn.DatabaseError) as error:
                pass
            finally:
                cur.close()
                conn.close()

#Allows the user an opportunity to verify their information that they entered is correct
    def Verify_Screen(self):
        self.f_name = self.f_name.title().strip()
        self.l_name = self.l_name.title().strip()
        self.email_address = self.email_address.strip()
        self.user_name = self.user_name.strip()
        if self.department == 10:
            self.department_name = "Engineering"
        elif self.department == 20:
            self.department_name = "Executive"
        elif self.department == 30:
            self.department_name = "Housekeeping"
        elif self.department == 40:
            self.department_name = "Human Resources"
        elif self.department == 50:
            self.department_name = "Information Technology"
        elif self.department == 60:
            self.department_name = "Marketing"
        elif self.department == 70:
            self.department_name = "Outbound Sales"
        layout2_submit = [[sg.Text(f"Name: {self.f_name} {self.l_name}")],
                          [sg.Text(f"Email Address: {self.email_address}")],
                          [sg.Text(f"Department: {self.department_name}")],
                          [sg.Text(f"User name: {self.user_name}")],
                          [sg.Text("Is this information correct?")],
                          [sg.Button("Yes",size=(10, 1), key='YES', pad=((5, 0), (5, 2))), sg.Button("No",size=(10, 1), key='NO', pad=((5, 0), (5, 2))), sg.Cancel(size=(10, 1), key='CANCEL', pad=((5,0),(5,2)))]]
        submit_new_user_window = sg.Window("Register Your Account",layout2_submit) 
        while True:
            event,values = submit_new_user_window.read()
            if event == 'CANCEL' or sg.WIN_CLOSED:
                submit_new_user_window.close()
                Login.Login_Screen()
            if event == 'NO':
                submit_new_user_window.close()
                Login.Register_Screen(self)
            if event == 'YES':
                submit_new_user_window.close()
                Login.Fetch_User_ID(self)

#Communicates the new user information to the users table in the database
    def Communicate_New_User_To_Table(self):
        self.f_name = self.f_name.lower().strip()
        self.l_name = self.l_name.lower().strip()
        self.job_class = 3
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
            cur.execute(f"""INSERT INTO users(first_name,last_name,email_address,department_id,user_name,password,user_id,job_class)
                            VALUES('{self.f_name}','{self.l_name}','{self.email_address}','{self.department}','{self.user_name}','{self.password}','{self.user_id}','{self.job_class}');""")                            
            conn.commit()
        except (Exception,conn.DatabaseError) as error:
            pass
        finally:
            conn.close()
            print(f"'{self.f_name}','{self.l_name}','{self.email_address}','{self.department}','{self.user_name}','{self.password}','{self.user_id}','{self.job_class}'")
            sg.Popup("Your new account has been registered.")
            Login.Map(self)

#Based on the user's job_class, this function either takes the user directly to the 'create work order' screen' or it takes them to a menu screen
    def Map(self):

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
                try:
                    cur.execute(f"""SELECT job_class FROM users
                                WHERE user_name = '{self.user_name}';""")
                    class_check = cur.fetchone()
                    if 1 in class_check:
                        self.job_class = 1
                    elif 2 in class_check:
                        self.job_class = 2
                    elif 3 in class_check:
                        self.job_class = 3
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
        if self.job_class == 3:
            Login.Work_Order_Submission(self)
        if self.job_class == 1 or self.job_class == 2:
            Login.Select_Map(self)

#This is the menu screen for those in the facilities manager job class
    def Select_Map(self):
        maplayout = [[sg.Text("Please choose an option: ",font='Times 16',size=(25,1))],
                     [sg.Button("Create a service request",key='REQUEST',size=(25,2)),sg.Button("Generate reports",key='GENERATE',size=(25,2)),sg.Button("Exit",key='EXIT',size=(25,2))]]
        
        map_window = sg.Window("Choose an option",maplayout)
        while True:
            event,values = map_window.read()
            if event == 'EXIT' or event == sg.WIN_CLOSED:
                sys.exit()
            if  event =='REQUEST':
                map_window.close()
                Login.Work_Order_Submission(self)
            if event == 'GENERATE':
                map_window.close()
                Login.Retrieve_Work_Orders(self)

#User creates a work order on this screen
    def Work_Order_Submission(self):
        work_order_layout = [[sg.Text("Request Service",size=(25,1))],
                             [sg.Text("Select floor",size=(25,1)), sg.Combo(["Basement",
                                                                             "1st Floor",
                                                                             "2nd Floor",
                                                                             "3rd Floor",
                                                                             "4th Floor",
                                                                             "5th Floor",
                                                                             "6th Floor"],key='FLOOR',size=(25,1))],
                             [sg.Text("Select service",size=(25,1)), sg.Combo(["Restroom Services",
                                                                               "Trash/Recycling", 
                                                                               "Heating/Cooling",
                                                                               "Lightbulb replacement"], key='SERVICE1',size=(25,1))],
                             [sg.Text("Enter details what service is being requested (i.e. specific location):",size=(50,1))],
                             [sg.InputText(size=(57,1),key='DETAILS')],                                                  
                             [sg.Submit(size=(10, 1), key='SUBMIT', pad=((5, 0), (5, 2))), sg.Cancel(size=(10, 1), key='CANCEL', pad=((5,0),(5,2)))]]
        work_order_window = sg.Window("Request Service",work_order_layout)
        while True:
            event,values = work_order_window.read()
            if event == sg.WIN_CLOSED:
                sys.exit()
            if event == 'CANCEL':
                if self.job_class == 1 or self.job_class == 2:
                    work_order_window.close()
                    Login.Select_Map(self)
                else:
                    sys.exit()

            elif event == 'SUBMIT':
                self.floor = str(values['FLOOR'])
                self.service = str(values['SERVICE1'])
                self.details = str(values['DETAILS'])
                self.time_stamp = datetime.datetime.now().strftime("%H:%M:%S")
                self.date_stamp = strftime("%Y-%m-%d",localtime())
                work_order_window.close()
                Login.Communicate_Work_Order(self)

#This screen verifies that the report has been submitted and asks the user what they would like to do next
    def Work_Order_Submitted(self):
        work_info = f"Floor: {self.floor}\nServices Request: {self.service}\nDetails: {self.details}"
        work_order_report_layout = [[sg.Text(f"Floor: {self.floor}")],
                                    [sg.Text(f"Service: {self.service}")],
                                    [sg.Text(f"Details: {self.details}")],
                                    [sg.Text(f"Time reported: {self.time_stamp}")],
                                    [sg.Text(f"Date reported: {self.date_stamp}")],
                                    [sg.Text(f"Your work order has been sent. Thank you.")],
                                    [sg.Text("Submit another work order?")],
                                    [sg.Button("Yes",key='YES'),sg.Button("No",key='NO')]]

        work_order_report_window = sg.Window("Service Report",work_order_report_layout)
        while True:
            event,values = work_order_report_window.read()
            if event == sg.WIN_CLOSED:
                break
            elif event == 'YES':
                print(work_info)
                work_order_report_window.close()
                Login.Work_Order_Submission(self)
            elif event == 'NO':
                if self.job_class == 1 or self.job_class == 2:
                    work_order_report_window.close()
                    Login.Select_Map(self)
                else:
                  sys.exit()

#This function communicates the work order to the database
    def Communicate_Work_Order(self):
        
        filename1=os.path.join(os.path.dirname(__file__),'work_order.csv')
        new_line = f"\n{self.floor},{self.service},{self.details},{self.date_stamp},{self.time_stamp},Null,Null"
        f = open(filename1,mode='a')
        f.write(new_line)
        f.close()
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
            cur.execute(f"""INSERT INTO work_order(floor,service,details,date_submitted,time_submitted)
                            VALUES('{self.floor}','{self.service}','{self.details}','{self.date_stamp}','{self.time_stamp}');""")                            
            conn.commit()
        except (Exception,conn.DatabaseError) as error:
            pass
        finally:
            conn.close()
            Login.Work_Order_Submitted(self)

#For users with the option, this is the screen to generate a report of work orders based on input criteria
    def Retrieve_Work_Orders(self):
        retrieve_layout = [[sg.Text("Retrieve Work Orders")],
                           [sg.Text("Select date range",size=(25,1)),sg.Text("Day-Month-Year")],
                           [sg.CalendarButton("Start date",format=('%Y-%m-%d'),target='DATE1', size=(25,1)),sg.In(background_color='#64778d',text_color='white',key='DATE1',enable_events=True,size=(15,1))],
                           [sg.CalendarButton("End date",format=('%Y-%m-%d'),target= 'DATE2',size=(25,1)),sg.In(background_color='#64778d',text_color='white',key='DATE2',enable_events=True,size=(15,1))],
                           [sg.Text("Select service",size=(25,1))], 
                           [sg.Combo(["Restroom Services",
                                      "Trash/Recycling", 
                                      "Heating/Cooling",
                                      "Lightbulb replacement"], key='SERVICE1',size=(25,1))],
                           [sg.Button("Okay",key='OKAY'),sg.Button("Cancel",key='CANCEL')]]
        retrieve_window = sg.Window("Work order report",retrieve_layout)
        while True:
            event,values = retrieve_window.read()
            if event == sg.WINDOW_CLOSED:
                break
            if event == 'CANCEL':
                Login.Select_Map(self)
            if event == 'OKAY':
                if values['DATE1'] =='' or values['DATE2']=='':
                    sg.popup("You must enter a start and an end date.")
                elif values['SERVICE1'] == '':
                    sg.popup("You must select a service to query.")
                elif values['DATE1'] !='' and values['DATE2']!='' and values['SERVICE1']:
                    self.start_date = values['DATE1']
                    self.end_date= values['DATE2']
                    self.service= values['SERVICE1']
                    retrieve_window.close()
                    Login.Communicate_Report_Request(self)

#This function retrieves the information for the report, and copies it to a text file and opens it on the screen for the user
    def Communicate_Report_Request(self):
        filename1=os.path.join(os.path.dirname(__file__),'work_order.csv')
        df = pd.read_csv(filename1)
        data_query = df[(df['date_submitted'].between(f"{self.start_date}",f"{self.end_date}")) & (df['service']==f"{self.service}")]
        print(data_query)
        filename2 = os.path.join(os.path.dirname(__file__),'report.txt')
        f = open(file='report.txt',mode='w')
        current_date_time = datetime.datetime.now()
        f.write(f"Facilities Service Report\t{current_date_time}\n{data_query}")
        f.close
        f = open('report.txt')
        filepath = r'"C:\Users\Owner\Documents\Python Files\report.txt"'
        os.startfile(filepath)
        Login.Retrieve_Work_Orders(self)

#Launch the application
launch = Login()
launch.Login_Screen()