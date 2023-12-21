from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
# from django.utils.datastructures import MultiValueDict
from .utils import render_to_pdf 
import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
# import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
# Create your views here.
@login_required(login_url='Login')
def Homepage(request):
    return render(request,'Home.html')
def landingpage(request):
    return render(request,'landingpage.html')
def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("your password and conform password are not same!!")
        else:   
            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            # return HttpResponse("user has been created sucessfully!!!")
            return redirect("Login")
            # print(uname,email,pass1,pass2)

    return render(request,'Signup.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        # print(username,pass1)
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('Home')
        else:
            return HttpResponse("User name or Password is incorrect!!!")

    return render(request,'Login.html')

def LogoutPage(request):
    logout(request)
    return redirect('Login')

def result(request):
    data=pd.read_csv(r'C:\Users\ANUP\Desktop\python\diabeteis\dataset\diabetes.csv')

    x=data.drop("Outcome",axis=1)
    y=data['Outcome']
    x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.1)
    
    model=LogisticRegression()
    model.fit(x_train,y_train)

    val1=float(request.GET['pregnancies'])
    val2=float(request.GET['glucose'])
    val3=float(request.GET['blood'])
    val4=float(request.GET['skin'])
    val5=float(request.GET['insulin'])
    val6=float(request.GET['Bmi'])
    val7=float(request.GET['dpf'])
    val8=float(request.GET['age'])
    nm = str(request.GET['Name'])
    pred=model.predict([[val1,val2,val3,val4,val5,val6,val7,val8]])

    result1=""
    if pred==[1]:
        result1="Positive"
    else:
        result1="Negative"
    data={
        'user':nm,
        'val1':val1,
        'val2':val2,
        'val3':val3,
        'val4':val4,
        'val5':val5,
        'val6':val6,
        'val7':val7,
        'val8':val8,
        'result1':result1,

    }

    return GeneratePdf(request,data)

# def answer(request,data,result1):
#     if result1 == "Positive":
#         return render(request,'index1.html',data)
#     else:
#         return render(request, 'index1.html', data)
#     return HttpResponse()
def aboutUs(request):
    return render(request,'contact-us.html')
def GeneratePdf(request,data):
        data1 = {
        "name": "Mama", #you can feach the data from database
        "id": 18,
        "amount": 333,
        }
        pdf = render_to_pdf('index.html',data)
        if pdf:
            response=HttpResponse(pdf,content_type='application/pdf')
            filename = "Report_for_%s.pdf" %(data1['id'])
            content = "inline; filename= %s" %(filename)
            response['Content-Disposition']=content
            return response
        return HttpResponse("Page Not Found")
