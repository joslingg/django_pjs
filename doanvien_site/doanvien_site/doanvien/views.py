from django.shortcuts import render,redirect
from .forms import MemberForm
from django.http import HttpResponse
from django.db.models import Q
from .models import Member

def home(request):
    return HttpResponse("<h2>Chào bạn đến với hệ thống quản lý Đoàn viên!</h2>")

def add_member(request):
    if request.method =='POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
         form = MemberForm()
    return render(request, 'doanvien/add_member.html',{'form':form})

def member_list(request):
    search = request.GET.get('q','')
    if search:
        members = Member.objects.filter(nane__icontains=search)
    else:
        members = Member.objects.all()
        
    return render(request, 'doanvien/member_list.html',{
        'members':members,
        'search': search,
    })