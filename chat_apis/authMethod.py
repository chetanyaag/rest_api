import pymongo
from datetime import datetime as dt
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


date_time = "%m/%d/%Y, %H:%M:%S"

con = pymongo.MongoClient("localhost", 27017)
db = con['TADA']


tokenTable = db['tokenTable']
# date_time_obj = dt.strptime(tokenText, date_time)

employees = db['EmployeeTable']



def checkToken(username):
    token = tokenTable.find_one({"username": username})
    if token:
        return token.get("token")
    else:
        tokenText = createToken(username)
        return tokenText

def createToken(username):
    tokenTime = dt.now()
    tokenText = tokenTime.strftime(date_time) 
    token = tokenTable.find_one({"username": username})
    if token:
        tokenTable.update_one({"username":username}, {"$set":{"token":tokenText, "tokenCreated":tokenTime}})
        return tokenText
    else:
         tokenObject = {"username":username, "token":tokenText, "tokenCreated":tokenTime}
         tokenTable.insert_one(tokenObject)
         return tokenText

def checkTokenValid(token):
    tokenObject = tokenTable.find_one({"token":token})
    if tokenObject:
        return True
    else:
        return False

def createExcel():
    dictonaryTo = []

    for employee in employees.find():
        for monthData in employee['monthDeductionList']:
            jsonTo = {}
            jsonTo['employee_code'] = employee['employee_code']
            jsonTo['employee_name'] = employee['employee_name']
            jsonTo['state'] = employee['state']
            jsonTo['location'] = employee['location']
            jsonTo['grade'] = employee['grade']
            jsonTo['month'] = monthData['month']
            jsonTo['date_of_reciving'] = monthData['dateOfRec']
            jsonTo['date_of_payment'] = monthData['paymentDate']
            jsonTo['claim_amount'] = monthData['claimAmount']
            jsonTo['grand_total'] = monthData['grandTotal']
            jsonTo['deduction'] = monthData['deduction']
            jsonTo['reason_of_deductions'] = monthData['reasonOfDeduction']
            jsonTo['email_id'] = employee['email_id']
            jsonTo['whats_app_mobile_number'] = employee['whats_app_mobile_number']
            jsonTo['status'] = employee['status']
            dictonaryTo.append(jsonTo)

    details = {
        'employee_code' : [],
        'employee_name' : [],
        'state' : [],
        'location' : [],
        'grade' : [],
        'month' : [],
        'date_of_reciving' : [],
        'date_of_payment' : [],
        'claim_amount' : [],
        'grand_total' : [],
        'deduction' : [],
        'reason_of_deductions' : [],
        'email_id' : [],
        'whats_app_mobile_number' : [],
        'status':[],
    }
    # creating a Dataframe object 
    df = pd.DataFrame(details)

    df = df.append(dictonaryTo, ignore_index=True, sort=False)

    # df.reset_index(drop=True, inplace=True)
    df.drop_duplicates().to_excel("excelToSend.xlsx", index=False) 

def sendMailWithAttachment():
    fromaddr = "EReimbursement@creambell.com"
    toaddr = "ghanshyam.garg@creambell.com"
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "WhatsApp TADA Database"
    body = "Sharing the current data in DATABASE"
    msg.attach(MIMEText(body, 'plain'))
    filename = "excelToSend.xlsx"
    attachment = open(filename, "rb")
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, "rqsecizxnzebaqsj")
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()

