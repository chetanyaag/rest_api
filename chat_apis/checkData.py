from .Employee import *
import pymongo

con = pymongo.MongoClient("localhost", 27017)
# database name
db = con['TADA']
employee_table = db['EmployeeTable']



def checkData(data):
    # CHECK EMPLOYEE CODE
    # CHECK MONTH
    month = Month(data)
    status = month.monthJsonObject()

    if status:
        checkDuplicate(data, status)
        addAdditionalData(data)
        return True
    else:
        return False



def checkDuplicate(data, monthData):

    employee_code = data['employee_code']

    employee = employee_table.find_one({"employee_code":str(employee_code)})

    # CHECK THE MONTH
    update_flag = False
    if employee:
        for mon in employee['monthDeductionList']:
            if monthData['month'] == mon['month'] and monthData['dateOfRec'] == mon['dateOfRec'] and monthData['paymentDate'] == mon['paymentDate']:
                update_flag = True
                break

        if update_flag:
            pa = 10
        else:
            em = employee['monthDeductionList'].copy()
            em.append(monthData)
            employee_table.update_one({"employee_code":str(employee_code)},{"$set":{"monthDeductionList":em}})
    else:
        employee_new = Employee(data)
        (employee_new.employeeJsonObject())
        employee_table.insert_one(employee_new.employeeJsonObject())

def addAdditionalData(data):
    employee_code = data['employee_code']

    employee = employee_table.find_one({"employee_code":str(employee_code)})

    status = data.get('status')
    if employee:
        if status in ['ACTIVE', 'DEACTIVE']:
            if employee['status'] != status:
                employee_table.update_one({"employee_code":str(employee_code)},{"$set":{"status":status}})
        whats_app_mobile_number = data.get('whats_app_mobile_number')
        if str(whats_app_mobile_number).isnumeric():
            if str(whats_app_mobile_number) != str(employee['whats_app_mobile_number'])  and len(str(whats_app_mobile_number))==10:
                # print(whats_app_mobile_number)
                (employee_table.update_one({"employee_code":str(employee_code)},{"$set":{"whats_app_mobile_number":int(whats_app_mobile_number)}}))

    


            

