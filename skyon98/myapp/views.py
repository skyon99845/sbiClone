from django.db.utils import IntegrityError
from django.shortcuts import render, redirect
from django.contrib import messages
from myapp.models import Customer, Userfeed, OTP
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
import random
import operator
import pyotp


totp = pyotp.TOTP('base32secret3232')
operators = [('+', operator.add), ('-', operator.sub), ('*', operator.mul)]
op, fn = random.choice(operators)

# Create your views here.
# defining the value of otp to be global variable for processing
gotp = int(0)


def home(request):
    return render(request, "home.html")


def userreg(request):
    return render(request, 'newuser.html')


def loginreg(request):
    return render(request, 'newuserlogin.html')


def submituserinfo(request):
    if (request.method == 'POST'):

        name = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        contactnumber = request.POST.get("contactnumber")
        user_exist = User.objects.filter(username=email).exists()

        n = random.randint(10000, 999999)
        while (Customer.objects.filter(accno=n).exists()):
            n = (random.randint(111, 9999))

        prn = random.randint(1000, 9999)
        while (Customer.objects.filter(pernumber=prn).exists()):
            prn = (random.randint(1000, 1000))

        if not user_exist:
            user = User.objects.create_user(
                username=email, password=password, is_staff="True", is_active="True")
            user.save()
            cust = Customer(customername=name, accno=n, pernumber=prn,
                            operator=op, email=email, contactnumber=contactnumber)
            cust.save()
            user.save()
            post = Customer.objects.get(customername=name)
            optrec = OTP(identity=post.id)
            optrec.save()
            messages.success(
                request, "Your Account Has Been Successfully created.")
            return redirect("/")
        else:
            messages.error(
                request, 'Email id already used. Please Enter Different Email Id.')
            return redirect("/userreg")


def userlogout(request):
    logout(request)
    return redirect("/")


def loginauth(request):
    if (request.method == 'POST'):
        name = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=name, password=password)
        # return HttpResponse(name, password)

        if user is not None:
            login(request, user)
            # writing query to display all the users
            request.session["email"] = name
            post = Customer.objects.get(email=name)
            request.session["name"] = post.customername

            return redirect(dashboard)

        messages.error(
            request, 'Please enter the correct username or password')
        return render(request, 'newuserlogin.html')


def dashboard(request):
    name = request.session["email"]
    post = Customer.objects.get(email=name)
    data = {
        "name": post.customername,
        "bal": post.initialbal,
        "accno": post.accno,
        "pernumber": post.pernumber,
        "operator": post.operator,
        "email": post.email,
        "mobile": post.contactnumber

    }
    # return HttpResponse(post.customername)
    return render(request, 'dashboard.html', data)


def addmoney(request):
    post = Customer.objects.get(customername=request.session['name'])
    data = {
        "name": post.customername,
        "bal": post.initialbal,
        "accno": post.accno,
    }
    return render(request, 'addmoney.html', data)


def updateaddmoney(request):
    money = request.GET.get("amount")
    amount = int(money)
    post = Customer.objects.get(customername=request.session['name'])
    post.initialbal = int(post.initialbal + amount)
    post.save()

    return redirect(dashboard)


def withdrawmoney(request):
    post = Customer.objects.get(customername=request.session['name'])
    data = {
        "name": post.customername,
        "bal": post.initialbal,
        "accno": post.accno,
    }
    return render(request, 'withdrawmoney.html', data)


def transfermoney(request):
    post = Customer.objects.get(customername=request.session['name'])
    data = {
        "name": post.customername,
        "bal": post.initialbal,
        "accno": post.accno,
    }
    return render(request, 'transfer.html', data)


def updatetransfermoney(request):
    money = request.GET.get("money")
    amount = int(money)
    raccno = float(request.GET.get("taccno"))
    try:
        pp = Customer.objects.get(accno=int(raccno))
    except ObjectDoesNotExist:
        messages.error(
            request, "Transaction is being Abort. Please Check the Account Number And The Try Again.")
        messages.error(
            request, "You are redirected to the Dashboard. Sorry for inconvience.")
        return redirect(dashboard)
    selfpp = Customer.objects.get(customername=request.session['name'])
    if pp.accno == selfpp.accno:
        messages.error(
            request, "You cannot mention Your Account Number For Transfer")
        messages.error(request, "Transaction is being Abort.")
        messages.error(
            request, "You are redirected to the Dashboard. Sorry for inconvience.")
        return redirect(dashboard)
    post = Customer.objects.get(customername=request.session['name'])
    # if the account balance of tranferer is less then 0 abort
    if (post.initialbal < 0):
        messages.error(
            request, "You have not sufficient balance in your account.")
        messages.error(request, "Transaction being Aborted.")
        return redirect(dashboard)
    # updating the balance of the transferee
    pp.initialbal = int(pp.initialbal)+int(money)
    post = Customer.objects.get(customername=request.session['name'])
    post.initialbal = int(post.initialbal - amount)

    if(post.initialbal <= 0):
        messages.error(request, "You Donot Have Sufficient Balance.")
        messages.error(request, "Transaction Aborted.")
        return redirect(dashboard)
    post.save()
    messages.success(
        request, "You transaction has been completed successfully.")
    pp = Customer.objects.get(accno=raccno)
    pp.initialbal = pp.initialbal+amount
    pp.save()

    return redirect(dashboard)


def updatewithdrawmoney(request):
    try:
        money = request.GET.get("amount")
    except ValueError:
        messages.error(request, "Please enter the numeric value")
        return redirect(withdrawmoney)
    amount = int(money)
    post = Customer.objects.get(customername=request.session['name'])

    # if post.initialbal<=0
    # error message
    if post.initialbal <= 0:
        messages.error(request, "You Donot Have Sufficient Balance ")
        return redirect(dashboard)
    post.initialbal = int(post.initialbal - amount)
    post.save()

    return redirect(withdrawmoney)


def updatepasswordform(request):
    return render(request, "newupass.html")


def updatepassword(request):
    if (request.method == 'POST'):
        name = request.POST.get("username")
        opassword = request.POST.get("opassword")
        npassword = request.POST.get("npassword")

        user = authenticate(username=name, password=opassword)
        if user is None:
            messages.error(
                request, "Please Enter the Correct Username And Password ")
            return render(request, "updatepassword.html")

        u = User.objects.get(username=name)
        u.set_password(npassword)
        u.save()
        messages.error(request, "Your Password Has Been Succesfully Changed.")
        return render(request, 'home.html')
    return HttpResponse("The password update process is terminated due to non availability of the username in the database")


def complaint(request):
    messages.info(
        request, "Kindly give correct information, your complaint is important to us to improve customer service.")
    return render(request, "newcomplaint.html")


def updatecomplaint(request):
    if(request.method == 'POST'):
        contactno = request.POST.get("contact")
        des = request.POST.get("descript")
        cust = Userfeed(contactno=contactno, complaintdes=des)
        data = {
            "contactno": contactno,
            "des": des,
        }
       # return render(request, 'blank.html', data)
        cust.save()
        messages.success(
            request, "Your complaint has been registered and our customer representative will get back to you shortly.")
        return redirect(dashboard)
    messages.error(request, "Your Complaint has Been Not Registered.")
    return redirect(dashboard)


def generateotp(request):
    post = Customer.objects.get(customername=request.session['name'])
    otprec = OTP.objects.get(identity=post.id)
    otprec.otpnumber = random.randint(1000, 9999)
    otprec.save()
    data = {
        "name": post.customername,
        "bal": post.initialbal,
        "accno": post.accno,
        "otpsend": otprec.otpnumber,
    }
    return render(request, 'resendtranfer.html', data)


def cal(coperator, pernumber, otp):
    if (coperator == '+'):
        return(int(otp)+int(pernumber))
    if (coperator == '-'):
        return(int(otp)-int(pernumber))
    if (coperator == '*'):
        return(int(otp)*int(pernumber))


def verify_otp(request):
    post = Customer.objects.get(customername=request.session['name'])
    otprec = OTP.objects.get(identity=post.id)
    coperator = post.operator
    pernumber = post.pernumber
    otp = otprec.otpnumber
    usertop = int(0)
    calculatedotp = abs(cal(coperator, pernumber, otp))
    if(request.method == 'POST'):
        (userotp) = request.POST.get("enteredotp")
        try:
            aa = abs(int(userotp))
            print("the userotp is:", userotp)
            print("the abs is :", aa)
            print("the calculatedotp is", calculatedotp)
        except ValueError:
            messages.success(
                request, "Please enter the processed OTP. To continue further.")
            return redirect(generateotp)
        if (aa == int(calculatedotp)):

            messages.success(
                request, "Your OTP has been Successfully Verfied.User Confirmed")
            return redirect(transfermoney)
        else:
            messages.success(
                request, "USer has not been confirmed. Please try Again.")
            messages.success(
                request, "Formular to Calculate otp is: {Shown otp}{operator}{Pernumber} ")
            messages.success(
                request, "You are redirected to the Dashboard. Sorry for inconvience.")
            return redirect(dashboard)


def blank(request):
    return render(request, 'blank.html')
