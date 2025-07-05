# import pymongo

# con = pymongo.MongoClient("localhost", 27017)
# # database name
# db = con['TADA']
# employee_table = db['EmployeeTable']


# for i in employee_table.find():
#     whats_app_mobile_number = str(i['whats_app_mobile_number'])
#     employee_code = i['employee_code']
#     if whats_app_mobile_number!= 'nan':
#         employee_table.update_one({'employee_code':employee_code}, {"$set":{"whats_app_mobile_number": str(int(float(whats_app_mobile_number)))}})

import pandas as pd



#check for employee code and month and year

def returnStatus(emp_code, month, year):
    #check for employee code
    df = pd.read_excel('status.xlsx')
    filtered_rows = df[df['emp_code'] == int(emp_code)]
    date = list(filtered_rows['Month'])[0]
    if month== date.month and year ==date.year:
        print(list(filtered_rows['Status'])[0])
    else:
        print("nono")


returnStatus('70002417', 7, 2023)

