from django.shortcuts import render
from .models import report
from .forms import ReportForm
from uploading.models import fees_update
from users.models import use, sch_reg,act
import pandas as pd
import xlsxwriter
from django.http import FileResponse
import io
from datetime import date
import string
import openpyxl
from itertools import islice


# Create your views here.

#['stu_id', 'subjectA', 'subjectB', 'subjectC', 'subjectD', 'subjectE', 'subjectF', 'subjectG', 'subjectH','subjectI','subjectJ', 'subjectK', 'subjectL',]
def download_sub(request):
    buffer = io.BytesIO()
    workbook = xlsxwriter.Workbook(buffer)
    username = None
    usernamed = request.user.username
    df_act = pd.DataFrame(act.objects.all().values().filter(username=usernamed))
    term = list(df_act['active_term']) 
    term = term[0]
    dfr = pd.DataFrame(sch_reg.objects.all().values().filter(username=usernamed))
    if list(dfr['date']) == []:
        dfr = pd.DataFrame(use.objects.all().values().filter(username = usernamed))
    ffr = list(dfr['full_sch'])
    ffrc = list(dfr['contact_details'])
    schr = ffr[0]
    tel = ffrc[0]
    df = pd.DataFrame(use.objects.all().values().filter(username = usernamed))
    if list(df) == []:
        df = pd.DataFrame(sch_reg.objects.all().values().filter(username = usernamed))
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


    subjects = pd.DataFrame(report.objects.all().values().filter(school = sch).filter(stu_id = 'stu_id'))
    col = ['number','stu_id', 'subjectA', 'subjectB', 'subjectC', 'subjectD', 'subjectE', 'subjectF', 'subjectG', 'subjectH','subjectI','subjectJ', 'subjectK', 'subjectL']
    subjects = subjects[col]
    #filter(stu_id = 'stu_id').values_list('number','subjectA', 'subjectB', 'subjectC', 'subjectD', 'subjectE', 'subjectF', 'subjectG', 'subjectH','subjectI','subjectJ', 'subjectK', 'subjectL')
    subjects['number'] = '###'
    subjects.columns = subjects.iloc[0]
    sub_list = subjects.columns
    sub_list = sub_list.insert(2, "Full Name")
    ree = ['Creche', 'Nursery1', 'Nursery2','K.G1', 'K.G2','Class1', 'Class2', 'Class3', 'Class4', 'Class5', 'Class6', 'J.H.S1', 'J.H.S2', 'J.H.S3']

    for t in ree:
        worksheet = workbook.add_worksheet(t+'-30%')
        worksheet2 = workbook.add_worksheet(t+'-70%')
        worksheet2.protect()
        worksheet.protect()

        row_num = 0 
        columns = sub_list
        for col_num in range(len(columns)):
            f1.set_bold(True)
            worksheet.write(row_num, col_num, columns[col_num], f1) 
            worksheet2.write(row_num, col_num, columns[col_num], f1)
          #  worksheet.write(row_num+1, col_num, 0, f1)
            worksheet.set_column(row_num, col_num, 13)
            worksheet2.set_column(row_num, col_num, 13)

        df = pd.DataFrame(fees_update.objects.all().values().filter(school = sch).filter(level = t))
        if list(df) == []:
            df
        else:
            stu_id = list(df['stu_id'])
            f_name = list(df['firstname'])
            for m in f_name:
                f_name = list(map(lambda x: x.replace(m, ' '+ m+ ' '), f_name))
            m_name = list(df['middlename'])
            m_name = list(map(lambda x: x.replace('None', ''), m_name))
            l_name = list(df['lastname'])
            for m in l_name:
                l_name = list(map(lambda x: x.replace(m, ' '+ m+ ' '), l_name))            
            d = [i+j+k for i,j,k in zip(l_name,m_name,f_name)]
            for row in range(len(d)):
                worksheet.write(row+1, 2, d[row])
                worksheet2.write(row+1, 2, d[row])               
                worksheet.write(row+1, 1, stu_id[row])
                worksheet2.write(row+1, 1, stu_id[row])
                for col_num in range(len(columns)-3):
                    worksheet.write(row+1, col_num+3, 0, unlocked)
                    worksheet2.write(row+1, col_num+3, 0, unlocked)
                    alph = list(string.ascii_uppercase[3:len(columns)])
                    for j in alph:
                        place = j+str(row+1)
                        worksheet.data_validation(place, {'validate': 'decimal',
                                        'criteria': '<',
                                        'value': 31,
                                        'input_message': 'Please ensure cell contains only figures and it should be less than or equal to 30%'
                                        })
                        worksheet2.data_validation(place, {'validate': 'decimal',
                                        'criteria': '<',
                                        'value': 71,
                                        'input_message': 'Please ensure cell contains only figures and it should be less than or equal to 70%'
                                        })
    workbook.close()
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename='reports.xlsx')

def upload_report(request):
    if "GET" == request.method:
        return render(request, 'report.html', {})
    else:
        excel_file = request.FILES["excel_file"]

        # you may put validations here to check extension or file size

        wb = openpyxl.load_workbook(excel_file)
        username = None
        usernamed = request.user.username 
        # getting a particular sheet by name out of many sheets
        ree = ['Creche', 'Nursery1', 'Nursery2', 'K.G1', 'K.G2','Class1', 'Class2', 'Class3', 'Class4', 'Class5', 'Class6', 'J.H.S1', 'J.H.S2', 'J.H.S3']
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
            worksheet = wb[i+'-30%']
            data = worksheet.values
            cols = next(data)[1:]
            data = list(data)
            idx = [r[0] for r in data]
            data = (islice(r, 1, None) for r in data)
            df = pd.DataFrame(data, index=idx, columns=cols)
            df = df.drop(['Full Name'], axis=1)
            df.insert(0, "number", 0, True)
            c_list = list(df.columns)
            chief = ['number', 'stu_id', 'subjectA', 'subjectB', 'subjectC', 'subjectD', 'subjectE', 'subjectF', 'subjectG', 'subjectH','subjectI','subjectJ', 'subjectK', 'subjectL',]
            lol
            chief = chief[:len(c_list)]
            for a,b in zip(c_list, chief):
                model = report()
                model.b = a
            model.save()
        return render(request, 'upload.html', {})




def report_reg(request):
    form = ReportForm(request.POST or None)
    username = None
    usernamed = request.user.username 
    dfs = pd.DataFrame(use.objects.all().values().filter(username = usernamed))
    if list(dfs) == []:
        dfs = pd.DataFrame(sch_reg.objects.all().values().filter(username = usernamed))
    ff = list(dfs['school'])
    sch = ff[0]
    if request.method == 'POST'and form.is_valid():
        subjectA = request.POST.get('subjectA')
        subjectB = request.POST.get('subjectB')
        subjectC = request.POST.get('subjectC')
        subjectD = request.POST.get('subjectD')
        subjectE = request.POST.get('subjectE')
        subjectF = request.POST.get('subjectF')
        subjectG = request.POST.get('subjectG')
        subjectH = request.POST.get('subjectH')
        subjectI = request.POST.get('subjectI')
        subjectJ = request.POST.get('subjectJ')
        subjectK = request.POST.get('subjectK')
        subjectL = request.POST.get('subjectL')
        mod =report(school = sch, stu_id = 'stu_id', subjectA=subjectA, subjectB=subjectB, subjectC=subjectC,subjectD=subjectD, subjectE=subjectE, subjectF=subjectF, subjectG=subjectG, subjectH=subjectH, subjectI=subjectI, subjectJ=subjectJ, subjectK=subjectK, subjectL=subjectL )
        mod.save()
 #       thanks = 'Subjects added as follows'
        
    subjects = report.objects.all().filter(school = sch).values_list('subjectA', 'subjectB', 'subjectC', 'subjectD', 'subjectE', 'subjectF', 'subjectG', 'subjectH','subjectI','subjectJ', 'subjectK', 'subjectL')
    
#rows = fees_update.objects.all().filter(school = sch).filter(level = t).values_list('stu_id', 'firstname' , 'middlename', 'lastname', 'level', 'fee','balance', 'amountpaid_term1', 'amountpaid_term2','amountpaid_term3' )
    df = pd.DataFrame(report.objects.all().filter(school = sch).filter(stu_id = 'stu_id'))
    if list(df) == []:
        return render(request, 'addsubject.html',{'form': form, 'subjects': subjects})
    else: 
        return render (request, 'correct.html', {})


