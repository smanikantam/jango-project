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
dic={0:'very poor',1:'poor',2:'average',3:'good',4:'very good'}
todo_category={'programing':['basics python','basics c','basics c++','basics java'],'practical':['core java','basic sql','DBMS','transaction'],'thearitical':['science','chemistry','mathematics']}
todo_subjects={'python':'programing','sql':'practical','c':'programing','physics':'thearitical','SQL':'practical'}
def home(request):
	return render(request,'file.html',{'name':'mani'})
def add(request):
	val1=int(request.POST['num1'])
	val2=int(request.POST['num2'])
	val=val1+val2
	return render(request,'res.html',{'result':val})
def login(request):
	if(request.method == 'POST'):
		username=request.POST['UName']
		password=request.POST['pass_word']
		# authenticating the user
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
	if(request.method == 'POST'):
		first_name=request.POST['f_name']
		last_name=request.POST['l_name']
		username=request.POST['UName']
		email=request.POST['Email']
		password=request.POST['password1']
		conform_password=request.POST['password2']
		if(password==conform_password):
			user=User.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email,password=password)
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
		# creating the obect for student
		std=student()
		f=request.FILES['myfile']
		# creating an object for class retrieve_file
		fs=retrieve_file()
		# saving the file
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
		messages.info(request,'uploaded file successfully')
		return render(request,'upload.html')
	else:
		print("not a post")

def search(request):
	# retrieving the column course from database
	# all_course=student.objects.values_list("course_name")
	# all_course=[str(x)[2:-3] for x in pd.Series(all_course).unique()]
	# status={0:'very poor',1:'poor',2:'average',3:'good',4:'very good'}
	# all_names=student.objects.all()
	# details_course={"details_course":all_course,'status':status.values(),"details":all_names}
	return render(request,"search.html")

def find(request):
	if(request.method=='POST'):
		# dic={0:'very poor',1:'poor',2:'average',3:'good',4:'very good'}
		# res={}
		# name=request.POST['name']
		# all_names=student.objects.all()
		# show=True
		# loaded_model = joblib.load("media/analysis_d.sav")
		# for i in all_names:
		# 	if(str(i.cand_name)==str(name)):
		# 		temp=np.array(i.marks).reshape(-1,1)
		# 		analysis_det=loaded_model.predict(temp)
		# 		res[str(i.course_name)]=dic[int(analysis_det)]
		# lis1=res.values()
		# lis2=res.keys()
		# l=zip(lis1,lis2)
		# for i,j in zip(lis1,lis2):
		# 	print(i,j)
		return render(request,"search.html")
	else:
		return redirect("/")

def findall(request):
	if(request.method=='POST'):
		course=request.POST['acourse']
		astatus=request.POST['astatus']
		dic={0:'very poor',1:'poor',2:'average',3:'good',4:'very good'}
		all_names=student.objects.all()
		loaded_model = joblib.load("media/analysis_d.sav")
		res=[]
		for i in all_names:
			temp=np.array(i.marks).reshape(-1,1)
			analysis_det=loaded_model.predict(temp)
			if(dic[int(analysis_det[0])]==astatus and i.course_name==course):
				res.append(i.cand_name)
		all_course=student.objects.values_list("course_name")
		all_course=[str(x)[2:-3] for x in pd.Series(all_course).unique()]
		all_names=student.objects.all()
		todo_status=True

		return render(request,'search.html',{'details':all_names,'res':res,'course':course,"status":dic.values,"details_course":all_course,"astatus":astatus,"todo_status":todo_status})
	else:
		return redirect("/")
def upload(request):
	return render(request,'upload.html')
def profile(request):
	return render(request,'profile.html')
def settings(request):
	return render(request,'settings.html')
def single_search_person(request):
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
		lis1=res.values()
		lis2=res.keys()
		l=zip(lis1,lis2)
		# for i,j in zip(lis1,lis2):
		# 	print(i,j)
		return render(request,"single_search_person.html",{'details':all_names,'show':show,'name':name,'res_anal1':lis1,'res_anal2':lis2,'res':res})
	else:
		return render(request,'single_search_person.html')
def entire_search_person(request):
	if(request.method=='POST'):
		course=request.POST['acourse']
		astatus=request.POST['astatus']
		dic={0:'very poor',1:'poor',2:'average',3:'good',4:'very good'}
		all_names=student.objects.all()
		loaded_model = joblib.load("media/analysis_d.sav")
		res=[]
		for i in all_names:
			temp=np.array(i.marks).reshape(-1,1)
			analysis_det=loaded_model.predict(temp)
			if(dic[int(analysis_det[0])]==astatus and i.course_name==course):
				res.append(i.cand_name)
		all_course=student.objects.values_list("course_name")
		all_course=[str(x)[2:-3] for x in pd.Series(all_course).unique()]
		all_names=student.objects.all()
		todo_status=True

		return render(request,'entire_search_person.html',{'details':all_names,'res':res,'course':course,"status":dic.values,"details_course":all_course,"astatus":astatus,"todo_status":todo_status})
	else:
		all_course=student.objects.values_list("course_name")
		all_course=[str(x)[2:-3] for x in pd.Series(all_course).unique()]
		status={0:'very poor',1:'poor',2:'average',3:'good',4:'very good'}
		all_names=student.objects.all()
		details_course={"details_course":all_course,'status':status.values(),"details":all_names}
		return render(request,"entire_search_person.html",details_course)
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
		messages.info(request,"data uploaded successfully")
		return render(request,'single_upload.html')

	else:
		return render(request,'single_upload.html')
def entire_upload(request):
	if(request.method == 'POST'):
		# creating the obect for student
		std=student()
		f=request.FILES['myfile']
		# creating an object for class retrieve_file
		fs=retrieve_file()
		# saving the file
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
		messages.info(request,'uploaded file successfully')
		return render(request,'entire_upload.html')
	else:
		return render(request,'entire_upload.html')
def todo_list(request):
	if(request.method == 'POST'):
		global dic,todo_subjects,todo_category
		rollno=request.POST['rollno']
		std=student.objects.filter(cand_name=rollno).values()
		loaded_model = joblib.load("media/analysis_d.sav")
		poor_student_list={}
		for i in std:
			temp=np.array(i['marks']).reshape(-1,1)
			analysis_det=loaded_model.predict(temp)
			if(int(analysis_det)<3):
				poor_student_list[str(i['course_name'])]=dic[int(analysis_det)]
		return render(request,'todo_list.html',{'poor_student_list':poor_student_list,'rollno':rollno,'todo_category':todo_category,'todo_subjects':todo_subjects})
	else:
		return render(request,'todo_list.html')
def check_progress(request):
	if(request.method == 'POST'):
		var=request.POST['check']
		print(var)
		return render(request,'todo_list.html')
	else:
		return redirect("search")
def partners(request):
	if(request.method == 'POST'):
		global dic
		all_names=student.objects.all()
		course=request.POST['acourse']
		all_course=student.objects.values_list("course_name")
		all_course=[str(x)[2:-3] for x in pd.Series(all_course).unique()]
		loaded_model = joblib.load("media/analysis_d.sav")
		poor_std=[]
		clev_std=[]
		for i in all_names:
			temp=np.array(i.marks).reshape(-1,1)
			analysis_det=loaded_model.predict(temp)
			if(int(analysis_det)<3 and i.course_name==course):
				poor_std.append(i.cand_name)
			if(int(analysis_det)>=3 and i.course_name==course):
				clev_std.append(i.cand_name)
			partners_list=zip(poor_std,clev_std)
		return render(request,'partners.html',{'partners_list':partners_list,'details_course':all_course})
	else:
		all_course=student.objects.values_list("course_name")
		all_course=[str(x)[2:-3] for x in pd.Series(all_course).unique()]
		return render(request,'partners.html',{'details_course':all_course})


	

