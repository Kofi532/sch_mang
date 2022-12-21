
# Create your views here.
from django.shortcuts import render
import openpyxl
from uploading.models import fees_update
import pandas as pd
from django.utils import timezone
from datetime import date
from users.models import use, sch_reg
from operator import add
from django.http import HttpResponseBadRequest
from django import forms
from django.template import RequestContext
import django_excel as excel
from itertools import islice
import os
from django.core.files.storage import FileSystemStorage
import numpy as np 



def indexv(request):
    if "GET" == request.method:
        return render(request, 'upload.html', {})
    else:
        form = UploadFileForm(request.POST, request.FILES)
        excel_file = request.FILES["excel_file"]

        # you may put validations here to check extension or file size

        wb = openpyxl.load_workbook(excel_file)

        # getting a particular sheet by name out of many sheets
        worksheet = wb["Sheet1"]
        print(worksheet)
        excel_data = list()
        # iterating over the rows andFF
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


def index(request):
    if "GET" == request.method:
        return render(request, 'upload.html', {})
    else:
        excel_file = request.FILES["excel_file"]

        # you may put validations here to check extension or file size

        wb = openpyxl.load_workbook(excel_file)

        # getting a particular sheet by name out of many sheets
        ree = ['Creche','K.G1', 'K.G2','Class1', 'Class2', 'Class3', 'Class4', 'Class5', 'Class6', 'J.H.S1', 'J.H.S2', 'J.H.S3']
        #ree = ['Creche','K.G 1', 'K.G 2']
        for i in ree:
           #"Class 1NewAdm"
            
            worksheet = wb[i+'NewAdm']
            data = worksheet.values
            cols = next(data)[1:]
            data = list(data)
            idx = [r[0] for r in data]
            data = (islice(r, 1, None) for r in data)
            df = pd.DataFrame(data, index=idx, columns=cols)
            username = None
            username = request.user.username 
            dfs = pd.DataFrame(use.objects.all().values())
            dfsr = pd.DataFrame(sch_reg.objects.all().values())
            dfsr = dfsr[dfsr['username'] == username]
            ffr = list(dfsr['school_code'])
            ffs = list(dfsr['full_sch'])
            fullsch = ffs[0]
            schr = ffr[0]
            dfs = dfs[dfs['username'] == username]
            ff = list(dfs['school'])
            sch = ff[0]
            df['middlename'] = df['middlename'].fillna('None')
            df['datey'] = date.today()
            #df['school'] = sch
            df['school_name'] = fullsch
            df['school'] = schr
            df['level'] = i
            df['numbering'] = np.arange(len(df))
            df['number'] = df['numbering']
            dfp = pd.DataFrame(fees_update.objects.all().values().filter(school = schr).filter(level = i))
            if list(dfp) == []:
                dfp = pd.DataFrame({'stu_id': pd.Series(dtype='str'),
                    'firstname': pd.Series(dtype='str'),
                    'lastname': pd.Series(dtype='str'),
                    'level': pd.Series(dtype='str'),
                    'amount': pd.Series(dtype='float'),
                    'fee': pd.Series(dtype='float'),
                    'balance': pd.Series(dtype='float'),
                    'school': pd.Series(dtype='str'),
                    'school_name': pd.Series(dtype='str'),
                    'datey': pd.Series(dtype='str')})
            else:
                dfp = dfp.copy()
                dfp = dfp.drop('id', axis=1)
            leng = len(list(dfp['stu_id']))+ 1
            df['numbering'] = df['numbering']+leng
            my_list = list(df['numbering'])
            my_list = [str(x) for x in my_list]
            inn = i
            df['stu_id'] = [inn+schr+'-' +x  for x in my_list]
            df['amount'] = 0
            df['balance'] = df['fee'] - df['amount']
            df['level'] = i
    #['stu_id', 'firstname', 'middlename', 'lastname', 'level', 'amount', 'fee', 'balance', 'school', 'datey']
            com = ['stu_id', 'firstname', 'middlename', 'lastname', 'level', 'amount', 'fee', 'balance', 'school','school_name', 'datey']
            df = df[com]
            df = df.dropna()
            for index, row in df.iterrows():
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
                model.school_full = row['school_name']
                model.datey = row['datey']
                model.save()
#        return render(request, 'upload.html', {})
    
        ree = ['Creche','K.G1', 'K.G2', 'Class1', 'Class2', 'Class3', 'Class4', 'Class5', 'Class6', 'J.H.S1', 'J.H.S2', 'J.H.S3']
        #ree = ['Creche','K.G 1', 'K.G 2']
        for ii in ree:
            worksheet = wb[ii]
            data = worksheet.values
            cols = next(data)[1:]
            data = list(data)
            idx = [r[0] for r in data]
            data = (islice(r, 1, None) for r in data)
            df = pd.DataFrame(data, index=idx, columns=cols)
            username = None
            username = request.user.username 
            dfs = pd.DataFrame(use.objects.all().values())
            dfs = dfs[dfs['username'] == username]
            ff = list(dfs['school'])
            sch = ff[0]
            df['middlename'] = df['middlename'].fillna('None')
            df['datey'] = date.today()
            df['school'] = schr
            df['level'] = ii
    #['stu_id', 'firstname', 'middlename', 'lastname', 'level', 'amount', 'fee', 'balance', 'school', 'datey']
            com = ['stu_id', 'firstname', 'middlename', 'lastname', 'level', 'amount', 'fee', 'balance', 'school', 'datey']
           # df.columns = com
            df = df[com]
            df = df.dropna()
            liss = list(df['stu_id'])
            lis = list(set(liss))
            dfp = pd.DataFrame(fees_update.objects.all().values().filter(school = schr))
            if list(dfp) == []:
                dfp = pd.DataFrame({'stu_id': pd.Series(dtype='str'),
                    'firstname': pd.Series(dtype='str'),
                    'lastname': pd.Series(dtype='str'),
                    'level': pd.Series(dtype='str'),
                    'amount': pd.Series(dtype='float'),
                    'fee': pd.Series(dtype='float'),
                    'balance': pd.Series(dtype='float'),
                    'school': pd.Series(dtype='str'),
                    'datey': pd.Series(dtype='str')})
            else:
                dfp = dfp.copy()
                dfp = dfp.drop('id', axis=1)
            dff = dfp.loc[dfp['stu_id'].isin(lis)]
            dff_list = list(dff['amount'])
            df_list = list(df['amount'])
            df['newamount'] = list(map(add, dff_list, df_list))
            df['balance'] = df['fee'] - df['newamount']
            df['middlename'] = df['middlename'].fillna('None')
            df['datey'] = date.today()
            df['school'] = schr   
            df['level'] = ii
            df['fee'] = 1000     
            list2 = list(df['stu_id'])
            for i in list2:
                fees_update.objects.all().filter(school = schr).filter(stu_id = i).delete()
            for index, row in df.iterrows():
                model = fees_update()
                model.stu_id = row['stu_id']
                model.firstname = row['firstname']
                model.middlename = row['middlename']
                model.lastname = row['lastname']
                model.level = row['level']
                model.amount = row['newamount']
                model.fee = row['fee']
                model.balance = row['balance']
                model.school = row['school']
                model.datey = row['datey']
                model.save()
            
        return render(request, 'upload.html', {})

