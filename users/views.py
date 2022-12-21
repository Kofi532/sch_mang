from django.shortcuts import render
from .models import use, sch_reg
import pandas as pd
from .forms import PostForm, RegForm
from datetime import date
from uploading.models import fees_update
from django.http import HttpResponse
import xlwt
import numpy as np
import xlsxwriter
from xlwt import Workbook, Worksheet, easyxf
import io
from django.http import FileResponse
import string
# Create your views here.



def adduser(request):
    username = None
    usernamed = request.user.username
    df = pd.DataFrame(sch_reg.objects.all().values())
    if usernamed in list(df['username']):
        #df = pd.DataFrame(use.objects.all().values())
        df = pd.DataFrame(sch_reg.objects.all().values())
        df = df.drop('id', axis=1)
        form = PostForm(request.POST or None)
        df = df[df['username'] == usernamed]
        ffs = list(df['full_sch'])
        schf = ffs[0]
        ff = list(df['school_code'])
        sch = ff[0]
        ffc = list(df['contact_details'])
        schc = ffc[0] 
        active = use.objects.all().values().filter(school = sch) 
        if request.method == 'POST'and form.is_valid():
            username = form.cleaned_data["username"]          
            dfn = pd.DataFrame({'username': pd.Series(dtype='str'),
                    'school': pd.Series(dtype='str'),
                    'full_sch': pd.Series(dtype='str'),
                    'contact_details': pd.Series(dtype='str'),
                    'date': pd.Series(dtype='object')})
            df = df[df['username'] == usernamed]
            ff = list(df['school_code'])
            sch = ff[0] 
            dfn['school'] = sch
            dfn['full_sch'] = schf
            dfn['contact_details'] = schc
            new_row = {'username':username , 'school':sch, 'full_sch':schf, 'contact_details':schc, 'date':date.today()}
            df2 = dfn.append(new_row, ignore_index=True)


            for index, row in df2.iterrows():
                model = use()
                model.username = row['username']
                model.school = row['school']
                model.full_sch = row['full_sch']
                model.date= row['date']
                model.save()

        else:
            form = PostForm()
        df = pd.DataFrame(sch_reg.objects.all().values())
        return render(request, 'adduser.html', {"form": form, "active": active})
    else:
        return render(request, 'unauth.html', {})

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
    response = HttpResponse(content_type='application/vnd.ms-excel')
    today = str(date.today())
    name = 'attachment;'+' filename = '+ today +'.xls'
    response['Content-Disposition'] = name

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Class 1') 
    ws1 = wb.add_sheet('NewAdm-Class1')
    ws2c = wb.add_sheet('Class 2')
    ws2a = wb.add_sheet('NewAdm-Class2')

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
        ws.col(col_num).width = 7000
        ws2c.write(row_num, col_num, columns[col_num], font_style) # at 0 row 0 column 
        ws2c.col(col_num).width = 7000
    # Sheet body, remaining rows

    columns = ['firstname' , 'middlename', 'lastname', 'fee' ]
    for col_num in range(len(columns)):
        ws1.write(row_num, col_num, columns[col_num], font_style) # at 0 row 0 column 
        ws1.col(col_num).width = 7000
        ws2a.write(row_num, col_num, columns[col_num], font_style) # at 0 row 0 column 
        ws2a.col(col_num).width = 7000


    rows = fees_update.objects.all().filter(school = sch).filter(level = 'Class 1').values_list('stu_id', 'firstname' , 'middlename', 'lastname', 'fee', 'balance' )
    c1 = pd.DataFrame(fees_update.objects.values().all().filter(school = sch).filter(level = 'Class 1').values_list('stu_id', 'firstname' , 'middlename', 'lastname', 'fee', 'balance' ))
    shape = c1.shape
    shape = shape[1]
    for row in rows:
        row_num += 1
        for col_num in range(shape):##check this one
            ws.write(row_num, col_num, row[col_num],  read_only)
            ws.col(col_num).width = 7000
    
    row_num = 0
    rows = fees_update.objects.all().filter(school = sch).filter(level = 'Class 2').values_list('stu_id', 'firstname' , 'middlename', 'lastname', 'fee', 'balance' )
    c1 = pd.DataFrame(fees_update.objects.values().all().filter(school = sch).filter(level = 'Class 2').values_list('stu_id', 'firstname' , 'middlename', 'lastname', 'fee', 'balance' ))
    shape = c1.shape
    shape = shape[1]
    for row in rows:
        row_num += 1
        for col_num in range(shape):##check this one
            ws2c.write(row_num, col_num, row[col_num],  read_only)
            ws2c.col(col_num).width = 7000


    df = pd.DataFrame(fees_update.objects.all().values().filter(school = sch).filter(level = 'Class 1').values_list('stu_id', 'firstname' , 'middlename', 'lastname', 'fee', 'balance' )) ##add payment editable
    df['amount'] = 0
    shape = df.shape
    shape = shape[1]
    listt = list(df['amount'])
    for x in range(len(listt)):
        col_num = shape-1
        ws.write(x+1, col_num, listt[x], editable)

    df = pd.DataFrame(fees_update.objects.all().values().filter(school = sch).filter(level = 'Class 2').values_list('stu_id', 'firstname' , 'middlename', 'lastname', 'fee', 'balance' )) ##add payment editable
    df['amount'] = 0
    shape = df.shape
    shape = shape[1]
    listt = list(df['amount'])
    for x in range(len(listt)):
        col_num = shape-1
        ws2c.write(x+1, col_num, listt[x], editable)     
    
    for k in range(30): ##add new person editable
        for r in range(30):
            ws2a.write(k+1, r, '', editable) 
            ws1.write(k+1, r, '', editable) 


    ws.protect = True
    ws1.protect = True
    ws2c.protect = True
    ws2a.protect = True
    ws.password = "kofi"


    wb.save(response)

    return response


def download4(request):
    username = None
    usernamed = request.user.username
    df = pd.DataFrame(use.objects.all().values())
    df = df[df['username'] == usernamed]
    ff = list(df['school'])
    sch = ff[0] 
    response = HttpResponse(content_type='application/vnd.ms-excel')
    today = str(date.today())
    name = 'attachment;'+' filename = '+ today +'.xls'
    response['Content-Disposition'] = name

    wb = xlwt.Workbook(encoding='utf-8')
   # ree = ['Creche','K.G 1', 'K.G 2','Class 1', 'Class 2', 'Class 3', 'Class 4', 'Class 5', 'Class 6', 'J.H.S 1', 'J.H.S 2', 'J.H.S 3']
    ree = ['Class 1']
    for t in ree:
        ws = wb.add_sheet(t) 
        ws1 = wb.add_sheet(t+'NewAdm')

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
            ws.col(col_num).width = 7000
        # Sheet body, remaining rows

        columns = ['firstname' , 'middlename', 'lastname', 'fee' ]
        for col_num in range(len(columns)):
            ws1.write(row_num, col_num, columns[col_num], font_style) # at 0 row 0 column 
            ws1.col(col_num).width = 7000


        rows = fees_update.objects.all().filter(school = sch).filter(level = t).values_list('stu_id', 'firstname' , 'middlename', 'lastname', 'fee', 'balance' )
        c1 = pd.DataFrame(fees_update.objects.values().all().filter(school = sch).filter(level = t).values_list('stu_id', 'firstname' , 'middlename', 'lastname', 'fee', 'balance' ))
        shape = c1.shape
        shape = shape[1]
        for row in rows:
            row_num += 1
            for col_num in range(shape):##check this one
                ws.write(row_num, col_num, row[col_num],  read_only)
                ws.col(col_num).width = 7000
        


        df = pd.DataFrame(fees_update.objects.all().values().filter(school = sch).filter(level = t).values_list('stu_id', 'firstname' , 'middlename', 'lastname', 'fee', 'balance' )) ##add payment editable
        df['amount'] = 0
        shape = df.shape
        shape = shape[1]
        listt = list(df['amount'])
        for x in range(len(listt)):
            col_num = shape-1
            ws.write(x+1, col_num, listt[x], editable)

        for k in range(30): ##add new person editable
            for r in range(30):
                ws1.write(k+1, r, '', editable) 


      #  ws.protect = True
      #  ws1.protect = True
      #  ws.password = "kofi"


    wb.save(response)

    return response

def download8(request):
    buffer = io.BytesIO()
    workbook = xlsxwriter.Workbook(buffer)
    username = None
    usernamed = request.user.username
    df = pd.DataFrame(use.objects.all().values())
    df = df[df['username'] == usernamed]
    ff = list(df['school'])
    sch = ff[0] 
    today = str(date.today())
    # Create some cell formats with protection properties.
    unlocked = workbook.add_format({'locked': False})
    locked   = workbook.add_format({'locked': True})


    f1= workbook.add_format()
    ree = ['Creche','K.G1', 'K.G2','Class1', 'Class2', 'Class3', 'Class4', 'Class5', 'Class6', 'J.H.S1', 'J.H.S2', 'J.H.S3']
  #  ree = ['Class 1']
    for t in ree:
        worksheet = workbook.add_worksheet(t)
        ws1 = workbook.add_worksheet(t+'NewAdm')
        worksheet.protect()
        ws1.protect()
        row_num = 0
        columns = ['number', 'stu_id', 'firstname' , 'middlename', 'lastname', 'fee', 'balance','total  paid', 'amount' ]
        for col_num in range(len(columns)):
            f1.set_bold(True)
            worksheet.write(row_num, col_num, columns[col_num], f1) 
            worksheet.set_column(row_num, col_num, 20)

        rows = fees_update.objects.all().filter(school = sch).filter(level = t).values_list('stu_id', 'firstname' , 'middlename', 'lastname', 'fee','balance', 'amount' )
        c1 = pd.DataFrame(fees_update.objects.values().all().filter(school = sch).filter(level = t).values_list('stu_id', 'firstname' , 'middlename', 'lastname', 'fee', 'balance', 'amount' ))
        shape = c1.shape
        shape = shape[1]
        for row in rows:
            row_num += 1
            for col_num in range(shape):##check this one
                worksheet.write(row_num, col_num+1, row[col_num])
                worksheet.write(row_num, shape +1, 0, unlocked)




        columns = ['number', 'firstname' , 'middlename', 'lastname', 'fee' ]
        row_num = 0
        for col_num in range(len(columns)):
            ws1.write(row_num, col_num, columns[col_num], f1)  # at 0 row 0 column 
            ws1.set_column(row_num, col_num, 20)

        for k in range(30): ##add new person editable
            for r in range(100):
                ws1.write(k+1, r, '', unlocked) 


    workbook.close()
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename='upload.xlsx')



def download3(request):
    buffer = io.BytesIO()
    workbook = xlsxwriter.Workbook(buffer)
    username = None
    usernamed = request.user.username
    dfr = pd.DataFrame(sch_reg.objects.all().values())
    dfr = dfr[dfr['username'] == usernamed]
    if list(dfr['date']) == []:
        dfr = pd.DataFrame(use.objects.all().values())
        dfr = dfr[dfr['username'] == usernamed]
    ffr = list(dfr['full_sch'])
    ffrc = list(dfr['contact_details'])
    schr = ffr[0]
    tel = ffrc[0]
    df = pd.DataFrame(use.objects.all().values())
    df = df[df['username'] == usernamed]
    ff = list(df['school'])
    sch = ff[0] 
    today = str(date.today())
    # Create some cell formats with protection properties.
    unlocked = workbook.add_format({'locked': False})
    locked   = workbook.add_format({'locked': True})
    merge_format = workbook.add_format({
    'bold': 1,
    'border': 0,
    'align': 'center',
    'valign': 'vcenter'})

    merge_format1 = workbook.add_format({
    #'bold': 1,
    'border': 0,
    'align': 'center',
    'valign': 'vcenter'})

    f1= workbook.add_format()
    ree = ['Creche','K.G1', 'K.G2','Class1', 'Class2', 'Class3', 'Class4', 'Class5', 'Class6', 'J.H.S1', 'J.H.S2', 'J.H.S3']
  #  ree = ['Class 1']
    for t in ree:
        worksheet = workbook.add_worksheet(t)
        wsr = workbook.add_worksheet(t+'Receipt')
        ws1 = workbook.add_worksheet(t+'NewAdm')
        worksheet.protect()
        ws1.protect()
        row_num = 0     
        #columns = ['number', 'stu_id', 'firstname' , 'middlename', 'lastname', 'fee', 'balance','total  paid', 'amount' ]
        columns = ['number', 'stu_id', 'firstname' , 'middlename', 'lastname','level', 'fee', 'balance','total  paid', 'amount' ]
        for col_num in range(len(columns)):
            f1.set_bold(True)
            worksheet.write(row_num, col_num, columns[col_num], f1) 
            worksheet.set_column(row_num, col_num, 20)

        rows = fees_update.objects.all().filter(school = sch).filter(level = t).values_list('stu_id', 'firstname' , 'middlename', 'lastname', 'level', 'fee','balance', 'amount' )
        c1 = pd.DataFrame(fees_update.objects.values().all().filter(school = sch).filter(level = t).values_list('stu_id', 'firstname' , 'middlename', 'lastname', 'fee', 'level', 'balance', 'amount' ))
        shape = c1.shape
        shape = shape[1]
        for row in rows:
            row_num += 1
            for col_num in range(shape):##check this one
                worksheet.write(row_num, col_num+1, row[col_num])
                worksheet.write(row_num, shape +1, 0, unlocked)




        columns = ['number', 'firstname' , 'middlename', 'lastname', 'fee' ]
        row_num = 0
        for col_num in range(len(columns)):
            ws1.write(row_num, col_num, columns[col_num], f1)  # at 0 row 0 column 
            ws1.set_column(row_num, col_num, 20)

        for k in range(30): ##add new person editable
            for r in range(100):
                ws1.write(k+1, r, '', unlocked) 

        
        columns1 = ['Stu_id' , 'Firstname' , 'Middlename', 'Lastname', 'Class']
        columns2 = ['Fee', 'Amount paid', 'Previous Balance',  'New Balance','Date' ]
        row_num = 3
        alp = list(string.ascii_uppercase[2:len(columns1)])
        for col_num in range(len(columns1)):
            wsr.write(row_num, col_num, columns1[col_num], merge_format)  # at 0 row 0 column 
            wsr.set_column(row_num, col_num, 20)
#            wsr.write_formula('C2','=VLOOKUP(B2,Creche!B2:I100,3,FALSE)') 
            
        wsr.merge_range('A1:E1', schr, merge_format)
        wsr.merge_range('A2:E2', 'Tel: '+tel , merge_format)
        wsr.write_formula('B5','=VLOOKUP(A5,'+t+'!B2:J100, 2,FALSE)', merge_format1)
        wsr.write_formula('C5','=VLOOKUP(A5,'+t+'!B2:J100, 3,FALSE)', merge_format1) 
        wsr.write_formula('D5','=VLOOKUP(A5,'+t+'!B2:J100, 4,FALSE)', merge_format1)
        wsr.write_formula('E5','=VLOOKUP(A5,'+t+'!B2:J100, 5,FALSE)', merge_format1)
        wsr.write_formula('E5','=VLOOKUP(A5,'+t+'!B2:J100, 5,FALSE)', merge_format1)
        wsr.write_formula('A8','=VLOOKUP(A5,'+t+'!B2:J100, 6,FALSE)', merge_format1)
        wsr.write_formula('C8','=VLOOKUP(A5,'+t+'!B2:J100, 7,FALSE)', merge_format1)
        wsr.write_formula('B8','=VLOOKUP(A5,'+t+'!B2:J100, 9,FALSE)', merge_format1)
        wsr.write_formula('D8','=C8 - B8', merge_format1)
        wsr.write(7, 4, str(date.today()), merge_format1)

        dft = pd.DataFrame(fees_update.objects.all().values().filter(school = sch).filter(level = t))
        if list(dft) == []:
            drp = []
        else:           
            drp = list(dft['stu_id'])
        wsr.data_validation(
            'A5',
            {
                'validate': 'list',
                'source': drp,
                'input_title': 'Choose one:',
                'input_message': 'Select a value from the list',
            }
        )

        for col_num in range(len(columns2)):
            wsr.write(row_num+3, col_num, columns2[col_num], merge_format)  # at 0 row 0 column 

    workbook.close()
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename='upload.xlsx')