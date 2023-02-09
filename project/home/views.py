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
from django.db.models import Q
from sklearn.neighbors import KNeighborsClassifier
dic={0:'very poor',1:'poor',2:'average',3:'good',4:'very good'}
todo_category={'programing':['basics python','basics c','basics c++','basics java'],
               'Database Management Systems':['mySQL','NoSQL','MongoDB'],
               'Cryptography':['Symmetric key algorithms','Asymmetric key algorithms','Cryptographic protocols:','Quantum Cryptography'],
               'Information Security':['Network Security','Cryptography','Cloud Security'],
               'Artificial Intelligence':['Data Science','Data Mining','Machine Learning','Deep Learning'],
               'Machine Learning':['Python','Data Science','Data Mining'],
               'Graphic Design':['Adobe Creative Suite','Affinity Designer','Blender']}
todo_subjects={'Core JAVA':'programing','SQL':'Database Management Systems', 'Blockchain':'Cryptography', 'Cyber Security':'Information Security',
              'Artificail Intelligence':'Artificial Intelligence', 'Machine Learning':'Machine Learning', 'UX/UI':'Graphic Design'}
def poor_good_std():
	std=student.objects.all()
	poor=[]
	good=[]
	for i in std:
		temp=np.array(i.marks).reshape(-1,1)
		analysis_det=loaded_model.predict(temp)
		if(int(analysis_det)<3):
			poor.append(i)
		else:
			good.append(i)
	return poor,good

def home(request):
	return render(request,'file.html',{'name':'mani'})
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
def search(request):
	# retrieving the column course from database
	# all_course=student.objects.values_list("course_name")
	# all_course=[str(x)[2:-3] for x in pd.Series(all_course).unique()]
	# status={0:'very poor',1:'poor',2:'average',3:'good',4:'very good'}
	# all_names=student.objects.all()
	# details_course={"details_course":all_course,'status':status.values(),"details":all_names}
	details=student.objects.all()
	loaded_model = joblib.load("media/analysis_d.sav")
	status=[]
	for i in details:
		temp=np.array(i.marks).reshape(-1,1)
		analysis_det=loaded_model.predict(temp)
		if(int(analysis_det[0])<3):
			status.append(True) # true if student is poor to highlight in search page
		else:
			status.append(False) # false if student is good
	details=zip(details,status)
	return render(request,"search.html",{'details':details})
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
		all_names=student.objects.filter(Q(cand_name=name))
		loaded_model = joblib.load("media/analysis_d.sav")
		for i in all_names:
				temp=np.array(i.marks).reshape(-1,1)
				analysis_det=loaded_model.predict(temp)
				res[str(i.course_name)]=dic[int(analysis_det)]
		lis1=res.values()
		lis2=res.keys()
		l=zip(lis1,lis2)
		return render(request,"single_search_person.html",{'details':all_names,'show':True,'name':name,'res_anal1':lis1,'res_anal2':lis2,'res':res})
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

		return render(request,'entire_search_person.html',{'details':all_names,'res':pd.Series(res).unique(),'course':course,"status":dic.values,"details_course":all_course,"astatus":astatus,"todo_status":todo_status})
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
		if(f.name.endswith('csv')):
			data=pd.read_csv("media/"+f.name)
		elif(f.name.endswith('xlsx')):
			data=pd.read_excel("media/"+f.name)
		data.to_csv("media/data.csv")
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
		messages.info(request,'uploaded file successfully')
		return render(request,'entire_upload.html')
	else:
		return render(request,'entire_upload.html')
def todo_list(request):
	if(request.method=='POST'):
		global dic,todo_subjects,todo_category
		rollno=request.POST['rollno']
		std=student.objects.filter(Q(cand_name=rollno)).values()
		loaded_model = joblib.load("media/analysis_d.sav")
		subjects=list(todo_subjects.keys())
		categories=list(todo_subjects.values())
		x=[]
		y=[]
		for i,sub in enumerate(subjects):
			x.append(i)
		for i,cat in enumerate(categories):
			y.append(i)
		classes=np.arange(len(categories))
		pair=np.array(y).reshape(-1,1)
		knn = KNeighborsClassifier(n_neighbors=1)
		knn.fit(pair, classes)
		todo_course={}
		for i in std:
			temp=np.array(i['marks']).reshape(-1,1)
			analysis_det=loaded_model.predict(temp)
			if(int(analysis_det)<3):
				new_x = subjects.index(i['course_name'])
				new_point = np.array(new_x).reshape(-1,1)
				prediction = knn.predict(new_point)
				todo_course[i['course_name']]=todo_category[categories[int(prediction)]]
		print(todo_course)
		return render(request,'todo_list.html',{'todo_course':todo_course,'rollno':rollno})
	else:
		all_course=student.objects.values_list("course_name")
		all_course=[str(x)[2:-3] for x in pd.Series(all_course).unique()]
		return render(request,'todo_list.html',{"details_course":all_course})
# def todo_list(request):
# 	all_course=student.objects.values_list("course_name")
# 	all_course=[str(x)[2:-3] for x in pd.Series(all_course).unique()]
# 	if(request.method == 'POST'):
# 		global dic,todo_subjects,todo_category
# 		rollno=request.POST['rollno']
# 		course=request.POST['course']
# 		std=student.objects.filter(Q(cand_name=rollno) & Q(course_name=course)).values()
# 		loaded_model = joblib.load("media/analysis_d.sav")
# 		poor_student_list={}
# 		for i in std:
# 			temp=np.array(i['marks']).reshape(-1,1)
# 			analysis_det=loaded_model.predict(temp)
# 			if(int(analysis_det)<3):
# 				poor_student_list[str(i['course_name'])]=dic[int(analysis_det)]
# 		subjects=list(todo_subjects.keys())
# 		categories=list(todo_subjects.values())
# 		x=[]
# 		y=[]
# 		for i,sub in enumerate(subjects):
# 			x.append(i)
# 		for i,cat in enumerate(categories):
# 			y.append(i)
# 		classes=np.arange(len(categories))
# 		pair=np.array(y).reshape(-1,1)
# 		knn = KNeighborsClassifier(n_neighbors=1)
# 		knn.fit(pair, classes)
# 		new_x = subjects.index(course)
# 		new_point = np.array(new_x).reshape(-1,1)
# 		prediction = knn.predict(new_point)
# 		todo_subject_list=todo_category[categories[int(prediction)]]
# 		print(todo_subject_list)
# 		return render(request,'todo_list.html',{'poor_student_list':poor_student_list,'rollno':rollno,'todo_category':todo_category,'todo_subjects':todo_subjects,"details_course":all_course,'todo_subject_list':todo_subject_list})
# 	else:
# 		return render(request,'todo_list.html',{"details_course":all_course})
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
			global partners_list_df
			partners_list=zip(poor_std,clev_std)
			if(len(clev_std)==len(poor_std)):
				partners_list_df=pd.DataFrame({'poor':poor_std,'good':clev_std})
			elif(len(clev_std)>len(poor_std)):
				partners_list_df=pd.DataFrame({'poor':poor_std,'good':clev_std[:len(poor_std)]})
			elif(len(clev_std)<len(poor_std)):
				partners_list_df=pd.DataFrame({'poor':poor_std[:len(clev_std)],'good':clev_std})
			partners_list_df.to_csv("media/partners_list_df.csv")
		return render(request,'partners.html',{'partners_list':partners_list,'details_course':all_course})
	else:
		all_course=student.objects.values_list("course_name")
		all_course=[str(x)[2:-3] for x in pd.Series(all_course).unique()]
		return render(request,'partners.html',{'details_course':all_course})

# offer =request.POST.get('offer',False)




	

