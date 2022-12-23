from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.core.files.storage import default_storage
from .models import retrieve_file,student
from django.core.files.storage import FileSystemStorage
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
import joblib

def index(request):
	return render(request,'file.html',{'name':'mani'})
def add(request):
	val1=int(request.POST['num1'])
	val2=int(request.POST['num2'])
	val=val1+val2
	return render(request,'res.html',{'result':val})
def login(request):
	if(request.method == 'POST'):
		username=request.POST['UNmae']
		password=request.POST['pass_word']
		user=auth.authenticate(username=username,password=password)
		if(user is not None):
			auth.login(request,user)
			return redirect("/")
		else:
			messages.info(request,"invalid details")
			return redirect("login")
	else:
		return render(request,'login.html')
def registration(request):
	print(request.method)
	if(request.method == 'POST'):
		first_name=request.POST['f_name']
		last_name=request.POST['l_name']
		username=request.POST['UName']
		email=request.POST['Email']
		password=request.POST['password1']
		conform_password=request.POST['password2']
		if(password==conform_password):
			user=User.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email,password=password,)
			user.save()
			messages.info(request,"user created")
			return redirect("login")
		else:
			messages.info(request,"password not matched")
			return redirect('registration')
	else:
		print("not done")
		return render(request,'registration.html')
def logout(request):
	auth.logout(request)
	return redirect("/")
def retrieve(request):
	if(request.method == 'POST'):
		std=student()
		f=request.FILES['myfile']
		fs=retrieve_file()
		name=fs.upload(f.name,f)
		messages.info(request,name)
		data=pd.read_excel("media/"+f.name)
		data.to_csv("media/data.csv")
		# x=data.iloc[:,:-1]
		# y=data.iloc[:,-1]
		# x.to_csv("media/savedcsv1.csv")
		for i in range(len(data)):
			std=student()
			for r in range(len(data.iloc[0,:])):
				v=0
				std.course_name=data.iloc[i,v]
				v+=1
				std.course_id=data.iloc[i,v]
				v+=1
				std.attempted_id=data.iloc[i,v]
				v+=1
				std.cand_name=data.iloc[i,v]
				v+=1
				std.cand_email=data.iloc[i,v]
				v+=1
				std.marks=data.iloc[i,v]
				v+=1
				std.grade=data.iloc[i,v]
				std.save()

		# if(files.myfile.name.endswith('csv')):
		# 	default_storage.save(files.myfile.name,files.myfile)
		# 	# files.myfile.save(files.myfile.name,files.myfile,save=True)
		# 	messages.info(request,"retrieved")
		# 	return redirect("/")
		# else:
		# 	messages.info(request,"incorrect format")
		# 	return redirect("/")
		return redirect("/")
		
	else:
		print("not a post")
def single_upload(request):
	if(request.method=='POST'):
		std=student()
		std.course_name=request.POST['course_name']
		std.course_id=request.POST['course_id']
		std.attempted_id=int(request.POST['attempted_id'])
		std.cand_name=request.POST['cand_name']
		std.cand_email=request.POST['cand_email']
		std.marks=int(request.POST['marks'])
		std.grade=request.POST['grade']
		std.save()
		return redirect("/")

	else:
		messages.info("not done")
		return redirect("/")
def search(request):
	if(request.method=='POST'):
		dic={0:'very poor',1:'poor',2:'average',3:'good',4:'very good'}
		res={}
		name=request.POST['name']
		all_names=student.objects.all()
		show=True
		loaded_model = joblib.load("media/analysis_d.sav")
		for i in all_names:
			if(str(i.cand_name)==str(name)):
				temp=np.array(i.marks).reshape(-1,1)
				analysis_det=loaded_model.predict(temp)
				res[str(i.course_name)]=dic[int(analysis_det)]
				print(res)
			print(i.cand_name)
		lis1=res.values()
		lis2=res.keys()
		l=zip(lis1,lis2)
		print(l)
		# for i,j in zip(lis1,lis2):
		# 	print(i,j)
		return render(request,"file.html",{'details':all_names,'show':show,'name':name,'res_anal1':lis1,'res_anal2':lis2,'res':res})
	else:
		return redirect("/")


