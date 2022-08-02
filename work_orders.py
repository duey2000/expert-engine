import PySimpleGUI as sg
import datetime
from datetime import datetime
import time
from time import strftime,localtime
import sys
import psycopg2

sg.set_options(font='Times 12')
sg.theme('DarkBlue3')

class Work_Order():
    def __init__(self,floor='',service='',details='',time_stamp='',date_stamp=''):
        self.floor = floor
        self.service = service
        self.details = details
        self.time_stamp = time_stamp
        self.date_stamp = date_stamp
        self.start_date = ''
        self.end_date = ''
        self.report = ''

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
            if event == 'CANCEL' or event == sg.WIN_CLOSED:
                break
            elif event == 'SUBMIT':
                self.floor = str(values['FLOOR'])
                self.service = str(values['SERVICE1'])
                self.details = str(values['DETAILS'])
                self.time_stamp = datetime.now().strftime("%H:%M")
                self.date_stamp = strftime("%d %b %Y",localtime())
                work_order_window.close()
                Work_Order.Communicate_Work_Order(self)
                Work_Order.Work_Order_Submitted(self)

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
                Work_Order.Work_Order_Submission(self)
                break
            elif event == 'NO':
                sys.exit()

    def Communicate_Work_Order(self):
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
            print("[+] Connection established!")
            cur.execute(f"""INSERT INTO work_order(floor,service,details,date_submitted,time_submitted)
                            VALUES('{self.floor}','{self.service}','{self.details}','{self.date_stamp}','{self.time_stamp}');""")                            
            conn.commit()
        except (Exception,conn.DatabaseError) as error:
            #Login.Error()
            pass
        finally:
            conn.close()
            print("[+] Connection closed.")


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
                break
            if event == 'OKAY':
                if values['DATE1'] =='' or values['DATE2']=='':
                    sg.popup("You must enter a start and an end date.")
                elif values['SERVICE1'] == '':
                    sg.popup("You must select a service to query.")
                elif values['DATE1'] !='' and values['DATE2']!='' and values['SERVICE1']:
                    self.start_date = values['DATE1']
                    self.end_date= values['DATE2']
                    self.service= values['SERVICE1']
                    #sg.popup(f"Start date: {self.start_date}\nEnd date: {self.end_date}\nService type: {self.service}")
                    print(f"""SELECT * FROM work_order
                                WHERE (date_submitted between '{self.start_date}' AND
                                '{self.end_date}') AND
                                service = '{self.service}';""")
                    retrieve_window.close()
                    Work_Order.Communicate_Report_Request(self)
    
    def Communicate_Report_Request(self):
        reporting_info = []
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
                cur.execute(f"""SELECT * FROM work_order
                                WHERE (date_submitted BETWEEN '{self.start_date}' AND '{self.end_date}') AND
                                service = '{self.service}';""")                            
                self.report = (cur.fetchall())
                reporting_info = list(self.report)
                print(reporting_info)

                print(self.report)
        except (Exception,conn.DatabaseError) as error:
            #Login.Error()
            pass
        finally:
            conn.close()
            print("[+] Connection closed.")
        print(reporting_info)


                
                
                    
                






        
                           
        

run = Work_Order()
run.Retrieve_Work_Orders()

# test = Work_Order()
# test.Retrieve_Work_Orders()


