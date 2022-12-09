from django.shortcuts import render
from .models import use
import pandas as pd
from .forms import PostForm
from datetime import date
from uploading.models import fees_update
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
        sch = df['school'][0] 
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
    disp = pd.DataFrame(fees_update.objects.all().values().filter(school = sch))
    disp = disp.drop('id', axis=1)
    disp = disp.to_dict()
    return render(request, 'data.html', {"disp": disp})
