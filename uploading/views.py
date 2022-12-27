
# Create your views here.
from django.shortcuts import render
import openpyxl
from uploading.models import fees_update
import pandas as pd
from django.utils import timezone
from datetime import date
from users.models import use, sch_reg, act, class_fee
from operator import add
from django.http import HttpResponseBadRequest
from django import forms
from django.template import RequestContext
import django_excel as excel
from itertools import islice
import os
from django.core.files.storage import FileSystemStorage
import numpy as np 
import itertools
import math



def index(request):
    if "GET" == request.method:
        return render(request, 'upload.html', {})
    else:
        excel_file = request.FILES["excel_file"]

        # you may put validations here to check extension or file size

        wb = openpyxl.load_workbook(excel_file)
        username = None
        usernamed = request.user.username 
        # getting a particular sheet by name out of many sheets
        ree = ['Creche','K.G1', 'K.G2','Class1', 'Class2', 'Class3', 'Class4', 'Class5', 'Class6', 'J.H.S1', 'J.H.S2', 'J.H.S3']
        #ree = ['Creche','K.G 1', 'K.G 2']
        dfs = pd.DataFrame(use.objects.all().values().filter(username = usernamed))
        if list(dfs) == []:
            dfs = pd.DataFrame(sch_reg.objects.all().values().filter(username = usernamed))
        code = list(dfs['school'])
        code = code[0]
        df_act = pd.DataFrame(act.objects.all().values())
        df_act = df_act[df_act['school_code'] == code]
        term = list(df_act['active_term']) 
        term = term[0]

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
            dfs = pd.DataFrame(use.objects.all().values().filter(username = usernamed))
            if list(dfs) == []:
                dfs = pd.DataFrame(sch_reg.objects.all().values().filter(username = usernamed))
            dfsr = pd.DataFrame(sch_reg.objects.all().values().filter(username = usernamed))
            ffr = list(dfsr['school'])
            ffs = list(dfsr['full_sch'])
            fullsch = ffs[0]
            schr = ffr[0]
            ff = list(dfs['school'])
            sch = ff[0]
            claz_df = pd.DataFrame(class_fee.objects.all().values().filter(school_code = sch).filter(classes =i))
            claz_df = list(claz_df['fee'])
            clazfee = claz_df[0]
            df['middlename'] = df['middlename'].fillna('None')
            df['mother_name'] = df['mother_name'].fillna('None')
            df['father_name'] = df['father_name'].fillna('None')
            df['mother_contact'] = df['mother_contact'].fillna('None')
            df['father_contact'] = df['father_contact'].fillna('None')
            df['datey'] = date.today()
            #df['school'] = sch
            df['school_name'] = fullsch
            df['school'] = schr
            df['level'] = i
            df['numbering'] = np.arange(len(df))
            df['number'] = df['numbering']
            df['fee'] = clazfee
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
#['stu_id', 'firstname', 'middlename', 'lastname', 'level', 'amount','amountpaid_term1', 'amountpaid_term2', 'amountpaid_term3','fee', 'balance', 'school', 'datey', 'school_full', 'mother_name', 'mother_contact', 'father_name', 'father_contact']
            else:
                dfp = dfp.copy()
                dfp = dfp.drop('id', axis=1)
            if len(dfp['stu_id']) == 0:
                leng = 1
            else:
                dfp['new'] = dfp["stu_id"].str.split("-", n = 1, expand = False)
                leng = list(dfp['new'])
                leng = [item[1] for item in leng]
                leng = [float(i) for i in leng]
                leng = max(leng)+1
                leng = math.trunc(leng)
           # leng = len(list(dfp['stu_id']))+ 1
            df['numbering'] = df['numbering']+leng
            my_list = list(df['numbering'])
            my_list = [str(x) for x in my_list]
            inn = i
            df['stu_id'] = [inn+schr+'-' +x  for x in my_list]
            df['amount'] = 0
            df['balance'] = df['fee'] - df['amount']
            df['level'] = i
            df['school_full'] = fullsch
#['stu_id', 'firstname', 'middlename', 'lastname', 'level', 'amount','amountpaid_term1', 'amountpaid_term2', 'amountpaid_term3','fee', 'balance', 'school', 'datey', 'school_full', 'mother_name', 'mother_contact', 'father_name', 'father_contact']
            com = ['stu_id', 'firstname', 'middlename', 'lastname', 'level', 'amount', 'fee', 'balance', 'school','school_name', 'datey', 'school_full', 'mother_name', 'mother_contact', 'father_name', 'father_contact']
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
                model.mother_name = row['mother_name']
                model.father_name = row['father_name']
                model.mother_contact = row['mother_contact']
                model.father_contact = row['father_contact']
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
            dfs = pd.DataFrame(use.objects.all().values().filter(username = usernamed))
            if list(dfs) == []:
                dfs = pd.DataFrame(sch_reg.objects.all().values().filter(username = usernamed))
            ff = list(dfs['school'])
            sch = ff[0]
            claz_df = pd.DataFrame(class_fee.objects.all().values().filter(school_code = sch).filter(classes =ii))
            claz_df = list(claz_df['fee'])
            clazfee = claz_df[0]
            df['middlename'] = df['middlename'].fillna('None')
            df['datey'] = date.today()
            df['school'] = schr
            df['level'] = ii
            df['fee'] = clazfee
    #['stu_id', 'firstname', 'middlename', 'lastname', 'level', 'amount', 'fee', 'balance', 'school', 'datey']
           # com = ['stu_id', 'firstname', 'middlename', 'lastname', 'level', 'amount', 'fee', 'balance', 'school', 'amount', 'datey']
           # df.columns = com
            #df = df[com]
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
                    'datey': pd.Series(dtype='str'),
                    'amountpaid_term1': pd.Series(dtype='float'),
                    'amountpaid_term2': pd.Series(dtype='float'),
                    'amountpaid_term3': pd.Series(dtype='float'),
                    })
            else:
                dfp = dfp.copy()
                dfp = dfp.drop('id', axis=1)
            dff = dfp.loc[dfp['stu_id'].isin(lis)]
            dff_list = list(dff['amountpaid_'+term]) #amountpaid-term1
            df_list = list(df['amount'])
            wix = list(df['stu_id'])
            df['newamount'] = list(map(add, dff_list, df_list))
            if term == 'term1':
                df['balance'] = df['fee'] - df['newamount']
            if term == 'term2':
                df['balance'] = 2*(df['fee']) - df['newamount'] - df['amountpaid_term1']
            if term == 'term3':
                df['balance'] = 3*(df['fee']) - df['newamount'] - df['amountpaid_term1'] - df['amountpaid_term2']
     #       df['balance'] = df['fee'] - df['newamount']
            df['middlename'] = df['middlename'].fillna('None')
            df['datey'] = date.today()
            df['school'] = schr   
            df['level'] = ii
            df['fee'] = clazfee
            if term == 'term1':
                df['amountpaid_term1'] = list(df['newamount'])
                df['amountpaid_term2'] = list(dff['amountpaid_term2'])
                df['amountpaid_term3'] = list(dff['amountpaid_term3'])
            if term == 'term2':               
                df['amountpaid_term1'] = list(dff['amountpaid_term1'])
                df['amountpaid_term2'] = list(df['newamount'])
                df['amountpaid_term3'] = list(dff['amountpaid_term3'])
            if term == 'term3':
                df['amountpaid_term1'] = list(dff['amountpaid_term1'])
                df['amountpaid_term2'] = list(df['amountpaid_term2'])
                df['amountpaid_term3'] = list(df['newamount'])
            list2 = list(df['stu_id'])
            newamn = list(df['newamount'])##
            bal = list(df['balance'])
            dat = list(df['datey'])
            am1 = list(df['amountpaid_term1'])
            am2 = list(df['amountpaid_term2'])
            am3 = list(df['amountpaid_term3'])
            fee = list(df['fee'])
            for a,b,c,d,e,f,g,h in zip(list2, newamn, bal, dat, am1, am2, am3, fee):
                fees_update.objects.filter(stu_id=a).update(amount=b, balance=c, datey=d, amountpaid_term1=e, amountpaid_term2=f, amountpaid_term3=g, fee=h)
            #for (a,b,c,d,e,f,g) in zip(list2, newamn, bal, dat, am1, am2, am3):
            
        return render(request, 'upload.html', {})

            # for i in list2:
            #     fees_update.objects.all().filter(school = schr).filter(stu_id = i).delete()
            # for index, row in df.iterrows():
            #     model = fees_update()
            #     if term == 'term1':
            #         model.amountpaid_term1 = row['newamount']
            #         model.amountpaid_term2 = row['amountpaid_term2']
            #         model.amountpaid_term3 = row['amountpaid_term3']
            #     if term == 'term2':
            #         model.amountpaid_term2 = row['newamount']
            #         model.amountpaid_term1 = row['amountpaid_term1']
            #         model.amountpaid_term3 = row['amountpaid_term3']
            #     if term == 'term3':
            #         model.amountpaid_term3 = row['newamount']
            #         model.amountpaid_term1 = row['amountpaid_term2']
            #         model.amountpaid_term3 = row['amountpaid_term3']                    
            #     model.stu_id = row['stu_id']
            #     model.firstname = row['firstname']
            #     model.middlename = row['middlename']
            #     model.lastname = row['lastname']
            #     model.level = row['level']
            #     model.fee = row['fee']
            #     model.balance = row['balance']
            #     model.school = row['school']
            #     model.datey = row['datey']
            #     model.save()


def fetch(request):
    username = None
    usernamed = request.user.username 
    dfs = pd.DataFrame(sch_reg.objects.all().values().filter(username = usernamed ))
    ff = list(dfs['school'])
    sch = ff[0]
    df = pd.DataFrame(fees_update.objects.all().values().filter(school = sch))
    ree = ['Creche','K.G1', 'K.G2', 'Class1', 'Class2', 'Class3', 'Class4', 'Class5', 'Class6', 'J.H.S1', 'J.H.S2', 'J.H.S3']
    for z in ree:
        dft = pd.DataFrame(fees_update.objects.all().values().filter(school = sch).filter(level = z))
        prom_id = list(df['stu_id'])
        level_id = list(df['level'])
        position = ree.index(level_id[0])
        pos1 = ree[position]
        if pos1 == ree[-1]:
            pos2 = ree[0]
        else:
            pos2 = ree[position+1]
        prom_id = [i.replace(pos1, pos2) for i in prom_id ]
        level_id =[i.replace(pos1, pos2) for i in level_id ]
        for a,b in zip(prom_id, level_id):
            fees_update.objects.filter(school =sch).update(stu_id = a, amount=0, balance=0, datey=date.today(), amountpaid_term1=0, amountpaid_term2=0, amountpaid_term3=0, fee=0, level = b)
    return render(request, 'fetch.html')
#['stu_id', 'firstname', 'middlename', 'lastname', 'level', 'amount','amountpaid_term1', 'amountpaid_term2', 'amountpaid_term3','fee', 'balance', 'school', 'datey']
