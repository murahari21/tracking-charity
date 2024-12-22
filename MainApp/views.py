import base64

from django.shortcuts import render
from Blockchain import *
from Block import *
import os
import csv
from datetime import date

from statsmodels.iolib import csv2st

blockchain = Blockchain()
if os.path.exists('blockchain_contract.txt'):
    with open('blockchain_contract.txt', 'rb') as fileinput:
        blockchain = pickle.load(fileinput)
    fileinput.close()

# Create your views here.
def index(request):
    return render(request,'index.html')
def login(request):
    return render(request,'Charity/Users.html')
def Register(request):
    return render(request,'Charity/Register.html')
def RegAction(request):
    if request.method=='POST':
        name=request.POST.get('cname', False)
        email=request.POST.get('email', False)
        address=request.POST.get('address', False)
        username=request.POST.get('username', False)
        password=request.POST.get('password', False)
        record = 'none'
        for i in range(len(blockchain.chain)):
            if i>0:
                b= blockchain.chain[i]
                data=b.transactions[0]
                data=base64.b64decode(data)
                decrypt=blockchain.decrypt(data)
                decrypt=decrypt.decode("utf-8")
                arr=decrypt.split("#")
                if arr[0] == "signup":
                    if arr[1]==name:
                        record="exits"
                        break

        if record == 'none':
            data = "signup#"+name+"#"+email+"#"+address+"#"+username+"#"+password
            enc=blockchain.encrypt(str(data))
            enc = str(base64.b64encode(enc),'utf-8')
            blockchain.add_new_transaction(enc)
            hash=blockchain.mine()
            b=blockchain.chain[len(blockchain.chain)-1]
            blockchain.save_object(blockchain,'blockchain_contract.txt')
            context= {'data':'Signup process completed...!!.','ph':'Previous HashCode: '+str(b.previous_hash),'bno':'BlockNo: '+str(b.index),'ch':"Current HashCode: "+str(b.hash)}
            return render(request, 'Charity/Register.html', context)
        else:
            context= {'data':'This Charity already Registered'}
            return render(request, 'Charity/Register.html', context)



def LogAction(request):
    username = request.POST.get('username', False)
    password = request.POST.get('password', False)
    status = 'none'
    email = 'none'
    cname='none'
    for i in range(len(blockchain.chain)):
        if i > 0:
            b = blockchain.chain[i]
            data = b.transactions[0]
            data = base64.b64decode(data)
            decrypt = blockchain.decrypt(data)
            decrypt = decrypt.decode("utf-8")
            arr = decrypt.split("#")
            if arr[0] == "signup":
                if arr[4] == username and arr[5] == password:
                    email=arr[2]
                    cname=arr[1]
                    status = 'success'
                    break
    if status == 'success':
        request.session['cemail']=email
        request.session['cusername']=username
        request.session['cname']=cname
        return render(request, 'Charity/UserHome.html')

    else:
        context= {'data':'Invalid login details'}
        return render(request, 'Charity/Users.html', context)

def chome(request):
    return render(request,'Charity/UserHome.html')
def CreateCampaign(request):
    return render(request,'Charity/CreateCampaign.html')
def CamapignAction(request):
    name=request.POST['name']
    title=request.POST['ctitle']
    desc=request.POST['description']
    amount=request.POST['tamount']
    duration=request.POST['duration']
    date=request.POST['date']
    accno=request.POST['accno']
    ifsc=request.POST['ifsc']
    record = 'none'
    for i in range(len(blockchain.chain)):
        if i>0:
            b= blockchain.chain[i]
            data=b.transactions[0]
            data=base64.b64decode(data)
            decrypt=blockchain.decrypt(data)
            decrypt=decrypt.decode("utf-8")
            arr=decrypt.split("#")
            if arr[0] == "campaign":
                if arr[2]==title:
                    record="exits"
                    break
    if record=='none':
        data ="campaign#"+name+"#"+title+"#"+desc+"#"+amount+"#"+duration+"#"+accno+"#"+ifsc+"#"+date
        enc=blockchain.encrypt(str(data))
        enc=str(base64.b64encode(enc), "utf-8")
        blockchain.add_new_transaction(enc)
        hash=blockchain.mine()
        b=blockchain.chain[len(blockchain.chain)-1]
        blockchain.save_object(blockchain,'blockchain_contract.txt')
        context= {'data':'Campaign Successfully Created..!!','ph':'Previous HashCode: '+str(b.previous_hash),'bno':'BlockNo: '+str(b.index),'ch':"Current HashCode: "+str(b.hash)}
        return render(request, 'Charity/CreateCampaign.html', context)
    else:
        context={'data':'Campaign Creation Failed..!!',}
        return render(request,'Charity/CreateCampaign.html', context)

def dlogin(request):
    return render(request,'Donor/Donor.html')
def dRegister(request):
    return render(request,'Donor/DRegister.html')

#Donor Operations
def DRegAction(request):
    if request.method=='POST':
        name=request.POST.get('name', False)
        email=request.POST.get('email', False)
        address=request.POST.get('address', False)
        password=request.POST.get('password', False)
        record = 'none'
        for i in range(len(blockchain.chain)):
            if i>0:
                b= blockchain.chain[i]
                data=b.transactions[0]
                data=base64.b64decode(data)
                decrypt=blockchain.decrypt(data)
                decrypt=decrypt.decode("utf-8")
                arr=decrypt.split("#")
                if arr[0] == "Dsignup":
                    if arr[2]==email:
                        record="exits"
                        break

        if record == 'none':
            data = "Dsignup#"+name+"#"+email+"#"+address+"#"+password
            enc=blockchain.encrypt(str(data))
            enc = str(base64.b64encode(enc),'utf-8')
            blockchain.add_new_transaction(enc)
            hash=blockchain.mine()
            b=blockchain.chain[len(blockchain.chain)-1]
            blockchain.save_object(blockchain,'blockchain_contract.txt')
            context= {'data':'Signup process completed.','ph':'Previous HashCode: '+str(b.previous_hash),'bno':'BlockNo: '+str(b.index),'ch':"Current HashCode: "+str(b.hash)}
            return render(request, 'Donor/DRegister.html', context)
        else:
            context= {'data':email+' Email ID already exists'}
            return render(request, 'Donor/DRegister.html', context)



def DLogAction(request):
    name = request.POST.get('name', False)
    password = request.POST.get('password', False)
    status = 'none'
    demail = 'none'
    for i in range(len(blockchain.chain)):
        if i > 0:
            b = blockchain.chain[i]
            data = b.transactions[0]
            data = base64.b64decode(data)
            decrypt = blockchain.decrypt(data)
            decrypt = decrypt.decode("utf-8")
            arr = decrypt.split("#")
            if arr[0] == "Dsignup":
                if arr[1] == name and arr[4] == password:
                    demail=arr[2]
                    status = 'success'
                    break
    if status == 'success':
        request.session['demail']=demail
        request.session['dname']=name
        return render(request, 'Donor/DonorHome.html')

    else:
        context= {'data':'Invalid login details'}
        return render(request, 'Donor/Donor.html', context)

def dhome(request):
    return render(request,'Donor/DonorHome.html')
def dBrowseCamp(request):
    output = '<table border=1 align=center>'
    output+='<tr><th style="background:black;"><font size=3 color=white>Charity Name</font></th>'
    output+='<th style="background:black;"><font size=3 color=white>Campaign Name</font></th>'
    output+='<th style="background:black;"><font size=3 color=white>Description</font></th>'
    output+='<th style="background:black;"><font size=3 color=white>Target Amount</font></th>'
    output+='<th style="background:black;"><font size=3 color=white>Duration</font></th>'
    output+='<th style="background:black;"><font size=3 color=white>Account NO</font></th>'
    output+='<th style="background:black;"><font size=3 color=white>IFSC Code</font></th>'
    output+='<th style="background:black;"><font size=3 color=white>Campaign Created On</font></th>'
    output+='<th style="background:black;"><font size=3 color=white>Check TrustWorthy</font></th></tr>'
    for i in range(len(blockchain.chain)):
        if i > 0:
            b = blockchain.chain[i]
            data = b.transactions[0]
            data = base64.b64decode(data)
            decrypt = blockchain.decrypt(data)
            decrypt = decrypt.decode("utf-8")
            arr = decrypt.split("#")
            if arr[0] == 'campaign':
                output+="<tr><td><font size=3 color=black>"+arr[1]+"</font></td>"
                output+="<td><font size=3 color=black>"+arr[2]+"</font></td>"
                output+="<td><font size=3 color=black>"+str(arr[3])+"</font></td>"
                output+="<td><font size=3 color=black>"+str(arr[4])+"</font></td>"
                output+="<td><font size=3 color=black>"+arr[5]+"</font></td>"
                output+="<td><font size=3 color=black>"+arr[6]+"</font></td>"
                output+="<td><font size=3 color=black>"+arr[7]+"</font></td>"
                output+="<td><font size=3 color=black>"+arr[8]+"</font></td>"
                output+='<td><a href=\'CheckTrust?cname='+arr[1]+'&accno='+arr[6]+'&ifsc='+arr[7]+'\'><font size=3 color=black>Click</font></a></td></tr>'
    output+="</table><br/><br/><br/><br/><br/><br/>"
    context= {'data':output}
    return render(request, 'Donor/ViewCampaigns.html', context)

def CheckTrust(request):
    cname=request.GET['cname']
    accno=request.GET['accno']
    ifsc=request.GET['ifsc']

    with open('charity-company-numbers.csv', mode='r', newline='', encoding='utf-8') as file:
        csv_reader=csv.reader(file)
        for row in csv_reader:
            if row[2] == cname:
                request.session['cname']=cname
                request.session['accno']=accno
                request.session['ifsc']=ifsc
                context={'msg':'It is a Trustworthy Charity..!!'}
                return render(request,'Donor/PaymentGateway.html',context)
            else:
                output = '<table border=1 align=center>'
                output+='<tr><th style="background:black;"><font size=3 color=white>Charity Name</font></th>'
                output+='<th style="background:black;"><font size=3 color=white>Campaign Name</font></th>'
                output+='<th style="background:black;"><font size=3 color=white>Description</font></th>'
                output+='<th style="background:black;"><font size=3 color=white>Target Amount</font></th>'
                output+='<th style="background:black;"><font size=3 color=white>Duration</font></th>'
                output+='<th style="background:black;"><font size=3 color=white>Account NO</font></th>'
                output+='<th style="background:black;"><font size=3 color=white>IFSC Code</font></th>'
                output+='<th style="background:black;"><font size=3 color=white>Campaign Created On</font></th>'
                output+='<th style="background:black;"><font size=3 color=white>Check TrustWorthy</font></th></tr>'
                for i in range(len(blockchain.chain)):
                    if i > 0:
                        b = blockchain.chain[i]
                        data = b.transactions[0]
                        data = base64.b64decode(data)
                        decrypt = blockchain.decrypt(data)
                        decrypt = decrypt.decode("utf-8")
                        arr = decrypt.split("#")
                        if arr[0] == 'campaign':
                            output+="<tr><td><font size=3 color=black>"+arr[1]+"</font></td>"
                            output+="<td><font size=3 color=black>"+arr[2]+"</font></td>"
                            output+="<td><font size=3 color=black>"+str(arr[3])+"</font></td>"
                            output+="<td><font size=3 color=black>"+str(arr[4])+"</font></td>"
                            output+="<td><font size=3 color=black>"+arr[5]+"</font></td>"
                            output+="<td><font size=3 color=black>"+arr[6]+"</font></td>"
                            output+="<td><font size=3 color=black>"+arr[7]+"</font></td>"
                            output+="<td><font size=3 color=black>"+arr[8]+"</font></td>"
                            output+='<td><a href=\'CheckTrust?cname='+arr[1]+'&accno='+arr[6]+'&ifsc='+arr[7]+'\'><font size=3 color=black>Click</font></a></td></tr>'
                output+="</table><br/><br/><br/><br/><br/><br/>"

                context={'data':output, 'msg':'Not a trustworthy Charity..!!'}
                return render(request, 'Donor/ViewCampaigns.html', context)

def dDonationAction(request):
    demail=request.session['demail']
    cname=request.session['cname']
    amount=request.POST['amount']
    today = date.today()


    data="Donation#"+demail+"#"+cname+"#"+amount+"#"+str(today)

    enc=blockchain.encrypt(str(data))
    enc = str(base64.b64encode(enc),'utf-8')
    blockchain.add_new_transaction(enc)
    hash=blockchain.mine()
    b=blockchain.chain[len(blockchain.chain)-1]
    blockchain.save_object(blockchain,'blockchain_contract.txt')

    output = '<table border=1 align=center>'
    output+='<tr><th style="background:black;"><font size=3 color=white>Charity Name</font></th>'
    output+='<th style="background:black;"><font size=3 color=white>Campaign Name</font></th>'
    output+='<th style="background:black;"><font size=3 color=white>Description</font></th>'
    output+='<th style="background:black;"><font size=3 color=white>Target Amount</font></th>'
    output+='<th style="background:black;"><font size=3 color=white>Duration</font></th>'
    output+='<th style="background:black;"><font size=3 color=white>Account NO</font></th>'
    output+='<th style="background:black;"><font size=3 color=white>IFSC Code</font></th>'
    output+='<th style="background:black;"><font size=3 color=white>Campaign Created On</font></th>'
    output+='<th style="background:black;"><font size=3 color=white>Check TrustWorthy</font></th></tr>'
    for i in range(len(blockchain.chain)):
        if i > 0:
            b = blockchain.chain[i]
            data = b.transactions[0]
            data = base64.b64decode(data)
            decrypt = blockchain.decrypt(data)
            decrypt = decrypt.decode("utf-8")
            arr = decrypt.split("#")
            if arr[0] == 'campaign':
                output+="<tr><td><font size=3 color=black>"+arr[1]+"</font></td>"
                output+="<td><font size=3 color=black>"+arr[2]+"</font></td>"
                output+="<td><font size=3 color=black>"+str(arr[3])+"</font></td>"
                output+="<td><font size=3 color=black>"+str(arr[4])+"</font></td>"
                output+="<td><font size=3 color=black>"+arr[5]+"</font></td>"
                output+="<td><font size=3 color=black>"+arr[6]+"</font></td>"
                output+="<td><font size=3 color=black>"+arr[7]+"</font></td>"
                output+="<td><font size=3 color=black>"+arr[8]+"</font></td>"
                output+='<td><a href=\'CheckTrust?cname='+arr[1]+'&accno='+arr[6]+'&ifsc='+arr[7]+'\'><font size=3 color=black>Click</font></a></td></tr>'
    output+="</table><br/><br/><br/><br/><br/><br/>"


    context= {'data':output,'msg':'Donation process completed.','ph':'Previous HashCode: '+str(b.previous_hash),'bno':'BlockNo: '+str(b.index),'ch':"Current HashCode: "+str(b.hash)}
    return render(request, 'Donor/ViewCampaigns.html', context)


def dviewmydonatoins(request):
    demail=request.session['demail']
    output = '<table border=1 align=center>'
    output+='<tr><th style="background:black;"><font size=3 color=white>Charity Name</font></th>'
    output+='<th style="background:black;"><font size=3 color=white>Amount</font></th>'
    output+='<th style="background:black;"><font size=3 color=white>Date</font></th></tr>'
    for i in range(len(blockchain.chain)):
        if i > 0:
            b = blockchain.chain[i]
            data = b.transactions[0]
            data = base64.b64decode(data)
            decrypt = blockchain.decrypt(data)
            decrypt = decrypt.decode("utf-8")
            arr = decrypt.split("#")
            if arr[0] == 'Donation' and arr[1]==demail:

                output+="<td><font size=3 color=black>"+arr[2]+"</font></td>"
                output+="<td><font size=3 color=black>"+str(arr[3])+"</font></td>"
                output+="<td><font size=3 color=black>"+str(arr[4])+"</font></td></tr>"
    output+="</table><br/><br/><br/><br/><br/><br/>"
    context= {'data':output}
    return render(request, 'Donor/ViewDonations.html', context)

def ViewReceiveFunds(request):
    cname=request.session['cname']
    output = '<table border=1 align=center>'
    output+='<tr><th style="background:black;"><font size=3 color=white>Charity Name</font></th>'
    output+='<th style="background:black;"><font size=3 color=white>Donor Name</font></th>'
    output+='<th style="background:black;"><font size=3 color=white>Amount</font></th>'
    output+='<th style="background:black;"><font size=3 color=white>Date</font></th></tr>'
    for i in range(len(blockchain.chain)):
        if i > 0:
            b = blockchain.chain[i]
            data = b.transactions[0]
            data = base64.b64decode(data)
            decrypt = blockchain.decrypt(data)
            decrypt = decrypt.decode("utf-8")
            arr = decrypt.split("#")
            if arr[0] == 'Donation' and arr[2]==cname:

                output+="<td><font size=3 color=black>"+arr[1]+"</font></td>"
                output+="<td><font size=3 color=black>"+arr[2]+"</font></td>"
                output+="<td><font size=3 color=black>"+str(arr[3])+"</font></td>"
                output+="<td><font size=3 color=black>"+str(arr[4])+"</font></td></tr>"
    output+="</table><br/><br/><br/><br/><br/><br/>"
    context= {'data':output}
    return render(request, 'Charity/ViewDonations.html', context)

def AddFundsUsage(request):
    return render(request, 'Charity/AddFUsedDetails.html')

def AddFUsedAction(request):
    cname=request.POST['name']
    workname=request.POST['workname']
    description=request.POST['description']
    samount=request.POST['samount']
    sdate=request.POST['sdate']



    data="FundsUsed#"+cname+"#"+workname+"#"+description+"#"+samount+"#"+sdate

    enc=blockchain.encrypt(str(data))
    enc = str(base64.b64encode(enc),'utf-8')
    blockchain.add_new_transaction(enc)
    hash=blockchain.mine()
    b=blockchain.chain[len(blockchain.chain)-1]
    blockchain.save_object(blockchain,'blockchain_contract.txt')
    context= {'msg':'Donation process completed.','ph':'Previous HashCode: '+str(b.previous_hash),'bno':'BlockNo: '+str(b.index),'ch':"Current HashCode: "+str(b.hash)}
    return render(request, 'Charity/AddFUsedDetails.html', context)

def dviewdetails(request):
    output = '<table border=1 align=center>'
    output+='<tr><th style="background:black;"><font size=3 color=white>Charity Name</font></th>'
    output+='<th style="background:black;"><font size=3 color=white>Work Name</font></th>'
    output+='<th style="background:black;"><font size=3 color=white>Description</font></th>'
    output+='<th style="background:black;"><font size=3 color=white>Spent Amount</font></th>'
    output+='<th style="background:black;"><font size=3 color=white>Spent Date</font></th></tr>'
    for i in range(len(blockchain.chain)):
        if i > 0:
            b = blockchain.chain[i]
            data = b.transactions[0]
            data = base64.b64decode(data)
            decrypt = blockchain.decrypt(data)
            decrypt = decrypt.decode("utf-8")
            arr = decrypt.split("#")
            print(arr[0])
            if arr[0] == 'FundsUsed':

                output+="<td><font size=3 color=black>"+arr[1]+"</font></td>"
                output+="<td><font size=3 color=black>"+arr[2]+"</font></td>"
                output+="<td><font size=3 color=black>"+str(arr[3])+"</font></td>"
                output+="<td><font size=3 color=black>"+str(arr[4])+"</font></td>"
                output+="<td><font size=3 color=black>"+str(arr[5])+"</font></td></tr>"
    output+="</table><br/><br/><br/><br/><br/><br/>"
    context= {'data':output}
    return render(request, 'Donor/ViewDetails.html',context)

def alogin(request):
    return render(request, 'AdminApp/Admin.html')

def adminLogAction(request):
    username=request.POST['username']
    password=request.POST['password']
    if username=="Admin" and password=="Admin":
        return render(request, 'AdminApp/AdminHome.html')
    else:
        context={'data':'Login Failed..!!'}
        return render(request,'AdminApp/Admin.html',context)

def aTransaction(request):
    output = '<table border=1 align=center>'
    output+='<tr><th style="background:black;"><font size=3 color=white>Charity Name</font></th>'
    output+='<th style="background:black;"><font size=3 color=white>Work Name</font></th>'
    output+='<th style="background:black;"><font size=3 color=white>Description</font></th>'
    output+='<th style="background:black;"><font size=3 color=white>Spent Amount</font></th>'
    output+='<th style="background:black;"><font size=3 color=white>Spent Date</font></th></tr>'
    for i in range(len(blockchain.chain)):
        if i > 0:
            b = blockchain.chain[i]
            data = b.transactions[0]
            data = base64.b64decode(data)
            decrypt = blockchain.decrypt(data)
            decrypt = decrypt.decode("utf-8")
            arr = decrypt.split("#")
            print(arr[0])
            if arr[0] == 'FundsUsed':

                output+="<td><font size=3 color=black>"+arr[1]+"</font></td>"
                output+="<td><font size=3 color=black>"+arr[2]+"</font></td>"
                output+="<td><font size=3 color=black>"+str(arr[3])+"</font></td>"
                output+="<td><font size=3 color=black>"+str(arr[4])+"</font></td>"
                output+="<td><font size=3 color=black>"+str(arr[5])+"</font></td></tr>"
    output+="</table><br/><br/><br/><br/><br/><br/>"
    context= {'data':output}
    return render(request,'AdminApp/Transactions.html',context)

def adminhome(request):
    return render(request,'AdminApp/AdminHome.html')

def aDTransaction(request):
    output = '<table border=1 align=center>'
    output+='<tr><th style="background:black;"><font size=3 color=white>Donor Name</font></th>'
    output+='<th style="background:black;"><font size=3 color=white>Charity Name</font></th>'
    output+='<th style="background:black;"><font size=3 color=white>Amount</font></th>'
    output+='<th style="background:black;"><font size=3 color=white>Date</font></th></tr>'

    for i in range(len(blockchain.chain)):
        if i > 0:
            b = blockchain.chain[i]
            data = b.transactions[0]
            data = base64.b64decode(data)
            decrypt = blockchain.decrypt(data)
            decrypt = decrypt.decode("utf-8")
            arr = decrypt.split("#")
            print(arr[0])
            if arr[0] == 'Donation':

                output+="<td><font size=3 color=black>"+arr[1]+"</font></td>"
                output+="<td><font size=3 color=black>"+arr[2]+"</font></td>"
                output+="<td><font size=3 color=black>"+str(arr[3])+"</font></td>"
                output+="<td><font size=3 color=black>"+str(arr[4])+"</font></td></tr>"
    output+="</table><br/><br/><br/><br/><br/><br/>"
    context= {'data':output}
    return render(request,'AdminApp/DonationTransactions.html',context)
