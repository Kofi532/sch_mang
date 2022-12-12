from django.shortcuts import render
from .models import use
import pandas as pd
from .forms import PostForm
from datetime import date
from uploading.models import fees_update
from django.http import HttpResponse
import xlwt
import numpy as np
import xlsxwriter
from xlwt import Workbook, Worksheet, easyxf

# Create your views here.
def adduser(request):
    username = None
    usernamed = request.user.username
    df = pd.DataFrame(use.objects.all().values())
    df = df.drop('id', axis=1)
    form = PostForm(request.POST or None)
    df = df[df['username'] == usernamed]
    ff = list(df['school'])
    sch = ff[0] 
    active = use.objects.all().values().filter(school = sch) 
    if request.method == 'POST'and form.is_valid():
        username = form.cleaned_data["username"]          
        dfn = pd.DataFrame({'username': pd.Series(dtype='str'),
                'school': pd.Series(dtype='str'),
                'date': pd.Series(dtype='object')})
        df = df[df['username'] == usernamed]
        ff = list(df['school'])
        sch = ff[0] 
        dfn['school'] = sch
        new_row = {'username':username , 'school':sch, 'date':date.today()}
        df2 = dfn.append(new_row, ignore_index=True)


        for index, row in df2.iterrows():
            model = use()
            model.username = row['username']
            model.school = row['school']
            model.date= row['date']
            model.save()

    else:
        form = PostForm()
    return render(request, 'adduser.html', {"form": form, "active": active})

def display(request):
    username = None
    usernamed = request.user.username
    df = pd.DataFrame(use.objects.all().values())
    df = df[df['username'] == usernamed]
    ff = list(df['school'])
    sch = ff[0] 
    disp = fees_update.objects.all().values().filter(school = sch)
    schname = fees_update.objects.all().values().filter(school = sch)[:1].get()
    return render(request, 'data.html', {"disp": disp, "schname": schname})


def download(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="users.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users Data') # this will make a sheet named Users Data

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['stu_id', 'firstname' ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style) # at 0 row 0 column 

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = fees_update.objects.all().values_list('stu_id', 'firstname')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)

    return response




def download2(request):
    username = None
    usernamed = request.user.username
    df = pd.DataFrame(use.objects.all().values())
    df = df[df['username'] == usernamed]
    ff = list(df['school'])
    sch = ff[0] 
    response = HttpResponse(content_type='application/ms-excel')
    today = str(date.today())
    name = 'attachment;'+' filename = '+ today +'.xls'
    response['Content-Disposition'] = name

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Class 1') # this will make a sheet named Users Data


    # Create cell styles for both read-only and editable cells
    editable = xlwt.easyxf("protection: cell_locked false;")
    read_only = xlwt.easyxf("")  # "cell_locked true" is default
    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True


    columns = ['stu_id', 'firstname' , 'middlename', 'lastname', 'fee', 'balance', 'amount' ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style) # at 0 row 0 column 
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = fees_update.objects.all().filter(school = sch).filter(level = 'Class 1').values_list('stu_id', 'firstname' , 'middlename', 'lastname', 'fee', 'balance', 'amount' )
    for row in rows:
        row_num += 1
        for col_num in range(len(rows)):
            ws.write(row_num, col_num, row[col_num],  read_only)
    
    df = pd.DataFrame(fees_update.objects.all().values().filter(school = sch).filter(level = 'Class 1'))
    df['amount'] = 0
    listt = list(df['amount'])
    for x in range(len(listt)):
        col_num = 6
        ws.write(x+1, col_num, listt[x], editable)



        # Protect worksheet - all cells will be read-only by default
    ws.protect = True  # defaults to False
    ws.password = "kofi"

    wb.save(response)

    return response


