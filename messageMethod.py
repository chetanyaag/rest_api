import requests
import json
import pymongo
import pandas as pd
import smtplib
from email.message import EmailMessage
import random
from datetime import datetime as dt
# df = pd.read_excel('tada.xlsx')

date_time = "%m/%d/%Y"
con = pymongo.MongoClient("localhost", 27017)
# database name
db = con['TADA']
# collection for chat_users
chat_user_table = db['chat_users']
chat_user_table_GST = db['chat_gst']
employee_table = db['EmployeeTable']


def verifyGST(gstNumber):
    url = "https://gst-return-status.p.rapidapi.com/free/gstin/" + gstNumber
    payload={}
    headers = {
    'Content-Type': 'application/json',
    'X-RapidAPI-Key': '8877c4790amsh917cef965a36f91p1e31f2jsn85d5764e9f9c',
    'X-RapidAPI-Host': 'gst-return-status.p.rapidapi.com'
    }
    response = requests.request("GET", url, headers=headers, data=payload)

    data = response.json()
    boolForGST = data.get('data').get('hsnArr')
    bool_hsn = data.get('data').get('hsn')
    nba = data.get('data').get('nba')
    fillingFreq = data.get('data').get('fillingFreq')
    returns = data.get('data').get('returns')

    returnString = ""
    if bool(boolForGST) or bool(bool_hsn) or bool(nba) or bool(fillingFreq) or bool(returns):
        tradeName = (data.get('data').get('tradeName'))
        legalName = (data.get('data').get('lgnm'))
        dateOfRegistration = (data.get('data').get('rgdt'))
        constitutionOfBussiness = (data.get('data').get('ctb'))
        gstinUniStatus = (data.get('data').get('sts'))

        if tradeName:
            returnString = returnString + "Trade Name : " + tradeName + "\n"
        if legalName:
            returnString = returnString + "Legal Name : " + legalName + "\n"
        if dateOfRegistration:
            returnString = returnString + "Date Of Registration : " + dateOfRegistration + "\n"
        if constitutionOfBussiness:
            returnString = returnString + "Constitution Of Bussiness : " + constitutionOfBussiness + "\n"
        if gstinUniStatus:
            returnString = returnString + "GSTIN/UIN Status : " + gstinUniStatus + "\n"
        
        returnString = returnString + "GSTIN : " +  gstNumber + "\n"    
        returnString = returnString + "Status : " +  " verified"
    else:
        returnString = gstNumber + " is not  verified"

    return returnString

def otp_create():
    number = random.randint(1000, 9999)
    return number


def send_email(otp, email_send):
    # email_rec = "chetanyaagrawal@gmail.com"
    # email_rec = "Ghanshyam.garg@creambell.com "
    email_rec = email_send
    password = "rqsecizxnzebaqsj"
    email_sender = "EReimbursement@creambell.com"
    # email_sender
    subject = "[DFIL_TADA] Please Verify OTP: {otp}".format(otp=otp)
    body = """
    Hi,

    A request for the TADA is asked for your account, Please verify.

    OTP: {otp}
    
    DO NOT REPLY 

    Thanks,
    DFIL_TADA_STATUS


    """.format(otp = otp)

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_rec
    em['Subject'] = subject
    em.set_content(body)

    smtp = smtplib.SMTP('smtp.gmail.com:587')
    smtp.ehlo()
    smtp.starttls()
    smtp.login(email_sender, password)
    smtp.sendmail(email_sender, email_rec, em.as_string())




def getMonthYear(string):
    month = string[:2]
    year = string[-2:]
    return [month, year]
# CHECK THE EMPLOYE CODE IN THE FILE


def check_em_code_file(employe_code):

    employee = employee_table.find_one({"employee_code":str(employe_code)})

    if employee:
        otp = otp_create()
        send_email(otp, employee['email_id'])
        return otp
    else:
        return ""



def create_employe_data1(employee, month_obj):
    return_string = ""
    employe_name = str(employee['employee_name'])
    # reciving_date = dataframe.iloc[index]['DATE OF RECEIVING']
    
    reciving_date = str(month_obj['dateOfRec'])
    reciving = dt.strptime(reciving_date, date_time)
    reciving_date = reciving.strftime("%d/%m/%Y")

    paymentDate = str(month_obj['paymentDate'])
    reciving = dt.strptime(paymentDate, date_time)
    paymentDate = reciving.strftime("%d/%m/%Y")

    month = str(month_obj['month'])
    reciving = dt.strptime(month, date_time)
    month = reciving.strftime("%d/%m/%Y")

    claim_amount = str(month_obj['claimAmount'])
    grand_total = str(month_obj['grandTotal'])
    deduction = str(month_obj['deduction'])
    reason = str(month_obj['reasonOfDeduction'])
    return_string =return_string+ "--------------------------------------------------\n                   DETAILS                      \n--------------------------------------------------\n"

    # return_string = return_string + " Employee Name             :  " + employe_name  + "\n Date Of Receiving             :  " + str(reciving_date) + "\n Month                               : " + str(month)
    # return_string = return_string + " Employee Name             :  " + employe_name  + "\n Month                               : " + str(month)
    # return_string = return_string + "\n Date Of Receiving          :  " + reciving_date  + "\n Date Of Payment           :  " + str(paymentDate) 
    # return_string = return_string + "\n Claim amount                 :  " + str(claim_amount)+ "\n Amount Paid                   :  " + str(grand_total)+ "\n Deduction                        :  " + str(deduction)
    # return_string = return_string +"\n Reason Of Deductions  :  \n" + reason +"\n"
    return_string = return_string + " Name                 :  " + employe_name  + "\n Month                : " + str(month)
    return_string = return_string + "\n Receiving Date :  " + reciving_date  + "\n Payment Date  :  " + str(paymentDate) 
    return_string = return_string + "\n Claim amount  :  " + str(claim_amount)+ "\n Amount Paid    :  " + str(grand_total)+ "\n Deduction         :  " + str(deduction)
    return_string = return_string +"\n Reasons            :  \n" + reason +"\n"


    return return_string


# CHECK THE MONTH AND YEAR
def check_month_year(text):
    try:
        text = text.split('/')
        month = int(text[0])
        year = int(text[1])
        # string = month_dic[month]+"-" + str(year)[-2:]
        string = [str(month), str(year)[-2:]]
        return {'status':True, 'string':string}
    except Exception as e:
        return {'status':False, 'string':'' }


def returnStatus(emp_code, month, year):
    #check for employee code
    try:
        df = pd.read_excel('status.xlsx')
        filtered_rows = df[df['emp_code'] == int(emp_code)]
        print(filtered_rows)
        date = list(filtered_rows['Month'])[0]
        if (int(month)== int(date.month)) and (int(year) ==int(date.year)):
            return list(filtered_rows['Status'])[0]
        else:
            return "Data is not available "
    except Exception as e:
        print(e)
        return "Data is not available "



def check_employee_code_return_data(employe_code, month):

    employee = employee_table.find_one({"employee_code": str(employe_code)})
    
    if employee:
        # check month
        returnData = ""
        for mn in employee['monthDeductionList']:
            # Get Month 
            month_list = getMonthYear(mn['month'])

            # if mn['month']== month:
            if int(month_list[0])==int(month[0]) and int(month_list[1]) == int(month[1]):
                returnData = returnData + "\n" +  create_employe_data1(employee, mn )
        if returnData:
            return returnData
        else:
            print("line 209")
            return returnStatus(employee['employee_code'], month[0], month[1])


    # return "Data is not available "



def send_message(number, message):
    # url = "https://graph.facebook.com/v14.0/103634132488392/messages"
    # url = "https://graph.facebook.com/v14.0/101557519384729/messages"   #//chatbot1
    
    url = url = "https://graph.facebook.com/v15.0/108172375434231/messages"  #//DFIL
    # CHATBOT1
    # headers = {"Authorization":"Bearer EAAFmaRWPBNMBAL6I8VIIAw8tYbjOPXfJR7FcpiykHHTYa1LnaZBHlbf64ZAW1kC9GEAA0yJ1i9gDysNdqZC6AVQABL2gEi8x0ImrkvSNP6O43MZBV9zwLEJzJAZAbA6V5ji6wNmyGjkwgC6tBiht43ZASllI8mgWvax5ZB9gwpT2XZA8ewDXkB1ZBCbWN1V0xvw9CB6SpynzXxQZDZD"}
   #DFIL
    headers = {"Authorization":"Bearer EAAJewjaI2kMBAE6b9KyHhTvqRWPM29pZCDq2AShjWuyl4UWKwOWE3IuJZBSQgRIYGeDBS66En93hNfjduPUg73ta3NOCZCWXQ3WLtr1TZBeWZCaH8vB0NUQSBtDE0XmZCVFtAM05EXLqLkSc404cnALZAjOw7kG9Ne4Tc9ZBOVYyx8N6DZAGnvZBpw"}
    headers['Content-Type'] = "application/json"
    # data = { "messaging_product": "whatsapp", "to": number,"type": "template", "template": { "name": "hello_world", "language": { "code": "en_US" } } }
    data = {
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": number,
  "type": "text",
  "text": { 
    "preview_url": False,
    "body": message
  }
    }

    res = requests.post(url, headers=headers, data=json.dumps(data, indent=4))


def conversation(number , message_text):
    # find the user in table
    chat_user  = chat_user_table.find_one({'user_number':number})
    chat_state = "0"

    if ("gst" in message_text) or ("GST" in message_text) :
        gstNumber = (message_text.split(" "))[1]
        return verifyGST(gstNumber)




    if chat_user:
        chat_state = chat_user.get('chat_state')
    else:
        chat_user_table.insert_one({"user_number":number, 'chat_state':"0"})
    

        #Cancel the chat or restart
    if message_text in ['cancel', '/cancel', 'stop','restart', 'Cancel', 'Stop', 'Restart']:
        chat_user_table.update_one({"user_number":number}, {"$set":{'chat_state':"0", "em_code":""}})
        return "Bye! I hope we can talk again some day."


    # process the message
    # START CHAT
    if chat_state == "0":
        if message_text in ['hi', 'hello', 'Hi', 'Hello'] :

            # CHECK IF NUMBER ALREADY EXITS IN TABLE

            employee = employee_table.find_one({"whats_app_mobile_number": str(number[2:])})

            if employee:
                return_text = "Hi "+ employee['employee_name'] + "\nPlease enter the number of the month and year in mm/yy Format.\nExample: 03/17"
                chat_user_table.update_one({'user_number': number}, {"$set":{"employee_code": employee['employee_code'], "chat_state" : "2"}})
            else:
                # return_text = "hi, I am TADA BOT, I will hold a conservation with you.\n You can stop conversion by sending stop. \n what is your employee code?"
                return_text = "Hi  I am DFIL TADA STATUS Teller. \n This number is not in my database. Do you want me to update Your number?\n If yes than Enter your Employee Code"
                chat_user_table.update_one({'user_number':number}, {"$set":{"chat_state":"1"}})
            
            
            return return_text
        else:
            return_text = "For starting the conversation send hi "
            return return_text

    # CHECK FOR THE EMPLOYEE
    elif chat_state == "1":
        if message_text.isnumeric():
            employee_status = check_em_code_file(message_text)
            if employee_status:
                chat_user_table.update_one({'user_number': number}, {"$set":{"employee_code": message_text,"otp": employee_status,"chat_state" : "1.5"}})
                return_text = "An otp is send on your email address.\n Please enter it"
                return return_text
            else:
                return "Invalid Employee Code"

        else:
            return_text = "Employee Code Must Be a Number"
            return return_text

    elif chat_state == "1.5":
        if message_text.isnumeric():
            otp = chat_user.get('otp')
            if str(otp) == str(message_text):
                chat_user_table.update_one({'user_number': number}, {"$set":{"chat_state" : "2"}})
                return_text = "Enter  month and year in mm/yy Format.\nExample: 03/17"
                return return_text
            else:
                return "Invalid otp"

        else:
            return_text = "Invalid otp"
            return return_text





    # CHECK THE DATE AND RETURN DATA
    elif chat_state =="2":
        month_status = check_month_year(message_text)
        if month_status['status']:
            employe_data = check_employee_code_return_data(chat_user['employee_code'], month_status['string'])
            return employe_data
        else:
            return "Incorrect Format"


    return "working on it"


def send_messageChatBot(number, message):
    # url = "https://graph.facebook.com/v14.0/103634132488392/messages"
    url = "https://graph.facebook.com/v14.0/101557519384729/messages"   #//chatbot1
    
    # url = url = "https://graph.facebook.com/v15.0/108172375434231/messages"  #//DFIL
    # CHATBOT1
    headers = {"Authorization":"Bearer EAAFmaRWPBNMBAL6I8VIIAw8tYbjOPXfJR7FcpiykHHTYa1LnaZBHlbf64ZAW1kC9GEAA0yJ1i9gDysNdqZC6AVQABL2gEi8x0ImrkvSNP6O43MZBV9zwLEJzJAZAbA6V5ji6wNmyGjkwgC6tBiht43ZASllI8mgWvax5ZB9gwpT2XZA8ewDXkB1ZBCbWN1V0xvw9CB6SpynzXxQZDZD"}
   #DFIL
    # headers = {"Authorization":"Bearer EAAJewjaI2kMBAE6b9KyHhTvqRWPM29pZCDq2AShjWuyl4UWKwOWE3IuJZBSQgRIYGeDBS66En93hNfjduPUg73ta3NOCZCWXQ3WLtr1TZBeWZCaH8vB0NUQSBtDE0XmZCVFtAM05EXLqLkSc404cnALZAjOw7kG9Ne4Tc9ZBOVYyx8N6DZAGnvZBpw"}
    headers['Content-Type'] = "application/json"
    # data = { "messaging_product": "whatsapp", "to": number,"type": "template", "template": { "name": "hello_world", "language": { "code": "en_US" } } }
    data = {
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": number,
  "type": "text",
  "text": { 
    "preview_url": False,
    "body": message
  }
    }

    res = requests.post(url, headers=headers, data=json.dumps(data, indent=4))


def conversationTwo(number , message_text):
    # find the user in table
    chat_user  = chat_user_table_GST.find_one({'user_number':number})
    chat_state = "0"

    if chat_user:
        chat_state = chat_user.get('chat_state')
    else:
        chat_user_table_GST.insert_one({"user_number":number, 'chat_state':"0"})
    

    #Cancel the chat or restart
    if message_text in ['cancel', '/cancel', 'stop','restart', 'Cancel', 'Stop', 'Restart']:
        chat_user_table_GST.update_one({"user_number":number}, {"$set":{'chat_state':"0"}})
        return "Bye! I hope we can talk again some day."


    # process the message
    # START CHAT
    if chat_state == "0":
        if message_text in ['hi', 'hello', 'Hi', 'Hello'] :
            return_text = "ENTER GST NUMBER"
            chat_user_table_GST.update_one({'user_number':number}, {"$set":{"chat_state":"1"}})
                        
            return return_text


    # CHECK FOR THE EMPLOYEE
    elif chat_state == "1":
        return_text = verifyGST(message_text)
        return return_text


