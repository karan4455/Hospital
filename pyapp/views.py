from datetime import date
import email
from importlib.abc import ExecutionLoader
from logging import exception
from multiprocessing import context
from time import time
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
import random
# from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages


def home(request):
    if "email"  in request.session:
        uid = User.objects.get(email = request.session['email'])
        if uid.role == "doctor":
            did = doctor.objects.get(User_id= uid)
            d_count = doctor.objects.all().count()
            context={
                'uid' : uid,
                'did' : did,
                'd_count' : d_count,
            }
            return render(request, "pyapp/index.html", context)
        else:
            pid = patient.objects.get(User_id= uid)
            p_count = doctor.objects.all().count()
            context={
                'uid' : uid,
                'pid' : pid,
                'p_count':p_count,
            }
        return render(request, "pyapp/index1.html", context)
    else:
        return redirect("login")

def register(request):
    if "email" in request.session:
        return redirect("home")
    else:
        if request.POST:
            p_role= request.POST['role']
            p_firstname= request.POST['firstname']
            p_lastname= request.POST['lastname']
            p_email= request.POST['email']
            p_contact= request.POST['contact']
            l1=['zxc147','qws963','drf852','rdf753','aqw943','bow789','qrm546']
            password=random.choice(l1) + p_email[3:6] + p_contact[4:8]
            

            uid= User.objects.create(email=p_email, password=password, role=p_role)

            # send_mail("AUTHENTICATION","password :"+str(password),"karanjethava012@gmail.com",[p_email])

            # subject = 'welcome to medsphere!'
            # message = f'Hello {p_firstname},\n\nWelcome to Doctor Finder application!\n\nPlease note your password for initial login is "{password}".\n\nThanks,\nTeam Doctor Finder'
            # email_from = settings.EMAIL_HOST_USER
            # recipient_list = [User.email,]
            # send_mail( subject, message, email_from, recipient_list )

            message = f'Hello {p_firstname},\n\nWelcome to MedSphere!\n\nPlease note your password for initial login is "{password}".\n\nThanks,\nTeam MedSphere'
            from_email = settings.EMAIL_HOST_USER
            send_mail("Welcome to MedSphere",
                        message, from_email, [p_email])



            if p_role=="doctor":
                did= doctor.objects.create(User_id=uid,firstname=p_firstname,lastname=p_lastname,mobile=p_contact)
                if did:
                    print("-->successfully registered!!")
                    context={
                        "s_msg": "successfully registered!! \n\n please check your E-mail Box!"
                    }
                    return render(request, "pyapp/register.html",context, )
                else:
                    return render(request, "pyapp/register.html")


                    
            else:
                pid= patient.objects.create(User_id=uid,firstname=p_firstname,lastname=p_lastname,mobile=p_contact)
                if pid:
                    print("-->successfully registered!!")
                    context={
                        "s_msg": "successfully registered!!  \n\n please check your E-mail Box!"
                    }
                    return render(request, "pyapp/register.html",context, )
                else:
                    return render(request, "pyapp/register.html")
                    

        else:
            print("page just loadded")
            return render(request, "pyapp/register.html")


def login(request):
    if "email" in request.session:
        return redirect('home')
    else:
        try:
            if request.POST:
                email = request.POST['email']
                password = request.POST['password']
                print("----> login", email)
                try:
                    uid= User.objects.get(email= email)
                    print("===>", uid.password)

                    if uid.password == password:
                        if uid.is_verify:
                            request.session["email"]= uid.email
                            if uid.role == "doctor":
                                did = doctor.objects.get(User_id = uid)
                                
                                return redirect("home")
                            
                            else:
                                pid = patient.objects.get(User_id = uid)
                                context={
                                    "uid" :uid,
                                    "pid" :pid,
                                }
                                return render(request, "pyapp/index1.html", context)
                        else:
                            context={
                                "email": uid.email
                            }
                            return render(request, "pyapp/change_password.html", context)

                    else:
                        print("-->wrong password")
                        context={
                            "e_msg": "invalid password"
                        }
                        return render(request, "pyapp/login.html", context)
                except User.DoesNotExist:
                    context={
                        'e_msg' : "email address does not exist"
                    }
                    return render(request, "pyapp/login.html", context)

            else:
                return render(request, "pyapp/login.html")
        except:
            context={
                        'e_msg' : "email already exist"
            }
            return render(request, "pyapp/login.html", context)


def logout(request):
    if "email" in request.session:
        del request.session['email']
        return render(request, "pyapp/login.html")

    else:
         return render(request, "pyapp/login.html")

def profile(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        if uid.role == "doctor":
            did = doctor.objects.get(User_id = uid)
            context = {
                'uid' : uid,
                'did' : did,
            }
            return render(request, "pyapp/profile.html", context)

def doc_profile(request):
    try:
        if request.POST:
            print("-->inside the doc profile")
            uid= User.objects.get(email= request.session['email'])
            did = doctor.objects.get(User_id= uid)
            print("-->doc firstname=", request.POST['firstname'])
            if request.POST['firstname']:
                did.firstname = request.POST['firstname']
            did.lastname = request.POST['lastname']
            did.qualification = request.POST['qualification']
            did.specification = request.POST['specification']
            did.available_time = request.POST['available_time']
            did.experience = request.POST['experience']
            did.clinic_name = request.POST['clinic_name']
            did.clinic_city = request.POST['clinic_city']
            did.clinic_address = request.POST['clinic_address']
            did.mobile = request.POST['mobile']
            if "pic" in request.FILES:
                did.pic = request.FILES['pic']
            did.save()
            context= {
                    "uid" : uid,
                    "did" : did,
                    "s_msg" : "successfully profile updated!!"
            }
            print("-->going to profile page")
            return render(request, "pyapp/profile.html", context)
        else:
            print("-->inside the else part")
            return redirect("login")
    except Exception as e:
        print("-->",e)
        return redirect("login")



def doc_pass_change(request):
    if "email" in request.session:
        uid= User.objects.get(email= request.session['email'])
        if uid.role=="doctor":
            did = doctor.objects.get(User_id= uid)
            currentpassword = request.POST['currentpassword']
            newpassword = request.POST['newpassword']
            if uid.password == currentpassword:
                uid.password = newpassword
                uid.save()
                del request.session['email']
                context= {
                "uid" : uid,
                "did" : did,
                "s_msg" : "successfully password reset"
                }
                return render(request, "pyapp/login.html", context)
            else:
                e_msg = "invalid current password"
                
                context= {
                    "uid" : uid,
                    "did" : did,
                "e_msg" : e_msg 
                }
                return render(request, "pyapp/profile.html", context)
        else:
            pid = patient.objects.get(User_id= uid)
            currentpassword = request.POST['currentpassword']
            newpassword = request.POST['newpassword']
            if uid.password == currentpassword:
                uid.password = newpassword
                uid.save()
                del request.session['email']
                context= {
                "uid" : uid,
                "pid" : pid,
                "s_msg" : "successfully password reset"
                }
                return render(request, "pyapp/login.html", context)
            else:
                e_msg = "invalid current password"
                
                context= {
                    "uid" : uid,
                    "pid" : pid,
                "e_msg" : e_msg 
                }
                return render(request, "pyapp/patients-profile.html", context)
 


def all_doctors(request):
    if "email" in request.session:
        uid= User.objects.get(email = request.session['email'])
        if uid.role == "doctor":
            did = doctor.objects.get(User_id= uid)
            dall = doctor.objects.filter().exclude(User_id= uid)
            context= {
                'did': did,
                'uid' : uid,
                'dall' : dall,

            }
            return render(request, "pyapp/all-doctors.html", context)
        else:
            pass



def view_doc(request,pk):
    if "email" in request.session:
        uid= User.objects.get(email = request.session['email'])
        if uid.role == "doctor":
            did = doctor.objects.get(User_id= uid)
            did_s = doctor.objects.get(id=pk)
            context= {
                'did': did,
                'uid' : uid,
                'did_s' : did_s

            }
            return render(request, "pyapp/spe-doc-profile.html", context)
        else:
            pass

def patients_profile(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        if uid.role == "patient":
            pid = patient.objects.get(User_id = uid)
            context = {
                'uid' : uid,
                'pid' : pid,
            }
            return render(request, "pyapp/patients-profile.html", context)


def all_patients(request):
    if "email" in request.session:
        uid= User.objects.get(email = request.session['email'])
        if uid.role == "doctor":
            did = doctor.objects.get(User_id= uid)
            pall = Appointment.objects.filter(doctor_id=did, status="PENDING")
            
            context= {
                'did': did,
                'uid' : uid,
                'pall': pall,
            

            }
            return render(request, "pyapp/all-patients.html", context)
        else:
            pass

def pt_profile(request):
    try:
        if request.POST:
            print("-->inside the pt profile")
            uid= User.objects.get(email= request.session['email'])
            pid = patient.objects.get(User_id= uid)
            print("-->pt firstname=", request.POST['firstname'])
            pid.firstname = request.POST['firstname']
            pid.lastname = request.POST['lastname']
            pid.age = request.POST['age']
            pid.gender = request.POST['gender']
            pid.birthdate = request.POST['birthdate']
            pid.blood_group = request.POST['blood_group']
            pid.height = request.POST['height']
            pid.weight = request.POST['weight']
            pid.address = request.POST['address']
            pid.mobile = request.POST['mobile']
            if "pic" in request.FILES:
                pid.pic = request.FILES['pic']
            pid.save()
            context= {
                    "uid" : uid,
                    "pid" : pid,
                    "s_msg" : "successfully profile updated!!"
            }
            print("-->going to profile page")
            return render(request, "pyapp/patients-profile.html", context)
        else:
            print("-->inside the else part")
            return redirect("login")
    except Exception as e:
        print("-->",e)
        return redirect("login")

def p_all_doctors(request):
    if "email" in request.session:
        uid= User.objects.get(email= request.session['email'])
        pid= patient.objects.get(User_id= uid)
        dall= doctor.objects.all()
        context={
            'uid': uid,
            'pid': pid,
            'dall': dall
        }
        return render (request,"pyapp/p-all-doctors.html",context)

def p_spe_doc_profile(request,pk):
    if "email" in request.session:
        uid= User.objects.get(email= request.session['email'])
        pid= patient.objects.get(User_id= uid)
        did_s= doctor.objects.get(id=pk)
        context={
            'uid': uid,
            'pid': pid,
            'did_s':did_s,
        }
        return render (request,"pyapp/p-spe-doc-profile.html",context)

def book_appointment(request,pk):
    if "email" in request.session:
        uid= User.objects.get(email= request.session['email'])
        pid= patient.objects.get(User_id= uid)
        did= doctor.objects.get(id=pk)
        context={
            'uid': uid,
            'pid': pid,
            'did':did,
        }
        return render (request,"pyapp/book-appointment.html",context)


def book_a(request):
    if request.POST:
        pid = request.POST['pid']
        did = request.POST['did']
        time = request.POST['time']
        date = request.POST['date']
        reason = request.POST['reason']
        case_status = request.POST['case_status']

        patient_id= patient.objects.get(id=pid)
        doctor_id= doctor.objects.get(id=did)
        paid= Appointment.objects.create(patient_id=patient_id, doctor_id=doctor_id, a_date=date, a_time=time, reason=reason,case_status=case_status)
        
        if paid:
            context={
                'pid' : patient_id,
                'did' :did,
                "msg" : "successfully appointment request sent !!"

            }
            return render (request,"pyapp/book-appointment.html",context)

    else:
        return redirect("login")

def change_password(request):
    try:
        if request.POST:
            email = request.POST['email']
            oldpassword = request.POST['oldpassword']
            newpassword = request.POST['newpassword']
            confirmpassword = request.POST['confirmpassword']

            uid = User.objects.get(email = email)
            if uid.password == oldpassword and newpassword == confirmpassword:
                uid.password = newpassword
                uid.is_verify = True
                uid.is_active = True
                uid.save()
                context = {
                    's_msg' : "successfully password reset"
                }
                return render (request, "pyapp/login.html", context)

            else:
                context = {
                    'e_msg' : "invalid password"
                }
                return render (request, "pyapp/login.html", context)

        else:
            return render (request, "pyapp/login.html")

    except:
        return render (request, "pyapp/login.html")

def approve_a(request, pk):
    if "email" in request.session:
        uid= User.objects.get(email = request.session['email'])
        if uid.role == "doctor":
            did = doctor.objects.get(User_id= uid)
            aid = Appointment.objects.get(id=pk)
            aid.status="APPROVE"
            aid.save()
#             send_mail("APPOINTMENT STATUS", "YOUR APPOINTMENT HAS BEEN CONFIRMED BY DOCTOR","karanjethava4455@gmail.com",[aid.patient_id.User_id.email])
            message = f'Hello User,\n\n Your Appointment is Approved by Doctor".\n\nThanks,\nTeam MedSphere'
            from_email = settings.EMAIL_HOST_USER
            send_mail("Appointment", message, from_email, [email])
            messages.info(request, "Please check your email inbox.")
            return redirect("all-patients")
        else:
            pass

def reject_a(request, pk):
    if "email" in request.session:
        uid= User.objects.get(email = request.session['email'])
        if uid.role == "doctor":
            did = doctor.objects.get(User_id= uid)
            aid = Appointment.objects.get(id=pk)
            aid.status="REJECT"
            aid.save()
#             send_mail("APPOINTMENT STATUS", "YOUR APPOINTMENT HAS BEEN NOT CONFIRMED BY DOCTOR","karanjethava4455@gmail.com",[aid.patient_id.User_id.email])
            message = f'Hello User,\n\n Your Appointment is Rejected".\n\nThanks,\nTeam MedSphere'
            from_email = settings.EMAIL_HOST_USER
            send_mail("Appointment", message, from_email, [email])
            messages.info(request, "Please check your email inbox.")
            return redirect("all-patients")
        else:
            pass

def forgot_password(request):
    if "email" in request.session:
        return redirect('home')

    else:
        if request.POST:
            email = request.POST['email']

            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                message = f'Hello User,\n\nPlease note your password is "{user.password}".\n\nThanks,\nTeam Doctor Finder'
                from_email = settings.EMAIL_HOST_USER
                send_mail("Password", message, from_email, [email])
                messages.info(request, "Please check your email inbox.")
                return redirect('login')

            else:
                return render(request, "pyapp/forgot-password.html", {'msg': "User doesn't exists."})

        else:
            return render(request, "pyapp/forgot-password.html")
