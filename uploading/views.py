
# Create your views here.
from django.shortcuts import render
import openpyxl
from .models import fees_update
import pandas as pd
from django.utils import timezone
from datetime import date
from users.models import use
from operator import add
def index(request):
    if "GET" == request.method:
        return render(request, 'upload.html', {})
    else:
        excel_file = request.FILES["excel_file"]

        # you may put validations here to check extension or file size

        wb = openpyxl.load_workbook(excel_file)

        # getting a particular sheet by name out of many sheets
        worksheet = wb["Sheet1"]
        print(worksheet)
        excel_data = list()
        # iterating over the rows and
        # getting value from each cell in row
        for row in worksheet.iter_rows():
            row_data = list()
            for cell in row:
                row_data.append(str(cell.value))
            excel_data.append(row_data)
# ['stu_id', 'firstname', 'middlename', 'lastname', 'level', 'amount','datey']   
        username = None
        username = request.user.username 
        dfs = pd.DataFrame(use.objects.all().values())
        dfs = dfs[dfs['username'] == username]
        ff = list(dfs['school'])
        sch = ff[0]
        data_df = pd.read_excel(wb, engine='openpyxl')
        data_df['middlename'] = data_df['middlename'].fillna('None')
        data_df['datey'] = date.today()
        data_df['school'] = sch
        liss = list(data_df['stu_id'])
        lis = list(set(liss)) #list of excel stu_id
        df = pd.DataFrame(fees_update.objects.all().values().filter(school = sch))
        
        if list(df) == []:
            df = pd.DataFrame({'stu_id': pd.Series(dtype='str'),
                   'firstname': pd.Series(dtype='str'),
                   'lastname': pd.Series(dtype='str'),
                   'level': pd.Series(dtype='str'),
                   'amount': pd.Series(dtype='float'),
                   'fee': pd.Series(dtype='float'),
                   'balance': pd.Series(dtype='float'),
                   'school': pd.Series(dtype='str'),
                   'datey': pd.Series(dtype='str')})
        else:
            df = df.copy()
            df = df.drop('id', axis=1)

        dff = df.loc[df['stu_id'].isin(lis)]
        list2 = list(dff['stu_id'])
        list2 = list(set(list2))#students from db in excel list 
        dv = data_df[~data_df['stu_id'].isin(list2)] #list taken out from the excel data \\ new stu
        dd = df[~df['stu_id'].isin(list2)]
        #dk = data_df[data_df.stu_id != list2]
        dff['amount'] = list(map(add, list(dff['amount']), list(data_df['amount'])))
        #dff['amount'] = dff['amount'] + data_df['amount']
        #di = dv.append(dff) #here going
        di = pd.concat([dv, dff])
        di['balance'] = di['fee'] - di['amount']
     #   dp = di.append(dd)
        dp = pd.concat([di, dd])
        
        #dp['balance'] = dp['fee'] - dp['amount']
        new_data = dp.copy()
        new_data = new_data.dropna()
        new_data = new_data.sort_values(by='datey')
 #       new_data = new_data.sort_values(by='datey',ascending=False)
        fees_update.objects.all().filter(school = sch).delete()

        for index, row in new_data.iterrows():
            model = fees_update()
            model.stu_id = row['stu_id']
            model.firstname = row['firstname']
            model.middlename = row['middlename']
            model.lastname = row['lastname']
            model.level = row['level']
            model.amount = row['amount']
            model.fee = row['fee']
            model.balance = row['balance']
            model.school = row['school']
            model.datey = row['datey']
            model.save()

        ## add your the excel, dclear rows in db, upload df to db

        return render(request, 'upload.html', {"excel_data":excel_data})



#create(Empcode=dbframe.Empcode,firstName=dbframe.firstName, middleName=dbframe.middleName,
 #                                           lastName=dbframe.lastName, email=dbframe.email, phoneNo=dbframe.phoneNo, address=dbframe.address,
  #                                          gender=dbframe.gender, DOB=dbfram