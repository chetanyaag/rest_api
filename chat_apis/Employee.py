from datetime import datetime as dt
import pymongo


con = pymongo.MongoClient("localhost", 27017)
# database name
db = con['TADA']
# collection for chat_users
# chat_user_table = db['chat_users']
employee_table = db['EmployeeTable']







dateTimeFormat = "%m/%d/%Y"


class Month:

    def __init__(self, month):
        self.mont = month.get('month')                                #done
        self.dateOfRec = month.get('date_of_reciving')                #done
        self.claimAmount = month.get('claim_amount')                  #done
        self.grandTotal = month.get('grand_total')                    #done
        self.deduction = month.get('deduction')                       #done
        self.reasonOfDeduction = month.get('reason_of_deduction')     #done
        self.dateOfPayment = month.get('date_of_payment')             #done
        self.nature = month.get('nature')                             #done

    def checkMonth(self):
        try:
            # CHECK IF EMPTY 
            if self.mont =="" or self.dateOfPayment =="" or self.dateOfRec=="":
                return False

            # TODO Add month
            monthDate = dt.strptime(self.mont, dateTimeFormat)
            monthDate = dt.strptime(self.dateOfRec, dateTimeFormat)
            monthDate = dt.strptime(self.dateOfPayment, dateTimeFormat)
            return True
        except Exception as e:
            return False


    def checkOther(self):
        if self.claimAmount =="" or self.grandTotal =="" or self.deduction=="":
            return False
        
        try:
            int(float(self.claimAmount))
            int(float(self.claimAmount))
            int(float(self.claimAmount))
            return True
        except:
            return False






    def monthJsonObject(self):

        if self.checkMonth() == False:
            return {}
        if self.checkOther() == False:
            return {}

        return {
            "month":self.mont, 
            "dateOfRec":self.dateOfRec, 
            "claimAmount":self.claimAmount,
             "grandTotal":self.grandTotal,
            "deduction":self.deduction, 
            "reasonOfDeduction":self.reasonOfDeduction, 
            "paymentDate":self.dateOfPayment
            # "nature":self.nature
            }






class Employee:


    def __init__(self, employee_data):
        self.em_code = str(employee_data.get('employee_code'))
        self.name = employee_data.get('employee_name')
        self.email = employee_data.get('email_id')
        self.state = employee_data.get('state')
        self.location = employee_data.get('location')
        self.grade = employee_data.get('grade')
        self.whatsappNo = employee_data.get('whats_app_mobile_number')
        self.status = employee_data.get('status')

        self.monthDeductionList = [Month(employee_data).monthJsonObject()]

    
    def employeeJsonObject(self):

        return {
            "employee_code":self.em_code, "employee_name":self.name, "email_id":self.email, "state":self.state, "location":self.location,
            "grade":self.grade, "whats_app_mobile_number":self.whatsappNo, "status":self.status, "monthDeductionList":self.monthDeductionList
        }

    def addToDataBase(self):
        # CHECK IF ALREADY EXITS BY EMPLOYEE CODE
        employee = employee_table.find_one({"employee_code":self.em_code}) 
        if employee:
            # CHECK Duplicase AND UPDATE DATA
            monthList = employee.get('monthDeductionList')
            noDuplicate = True
            for index in range(len(month_list)):
                if self.month == monthList[index]['month'] and self.reasonOfDeduction== monthList[index]['reasonOfDeduction'] and self.dateOfPayment== monthList[index]['paymentDate']:
                    duplicate = False
                    break
            if noDuplicate:
                monthList.append(self.monthJsonObject())
        else:
            # ADD A NEW EMPLOYEE   
            employee_table.insert_one(self.employeeJsonObject())
