from django.shortcuts import render,redirect, get_object_or_404
from .forms import MemberForm
from django.http import HttpResponse
from django.db.models import Q
from .models import Member,Department,Group
from django.db.models import Count
import openpyxl
from openpyxl.styles import Font

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
    department_filter = request.GET.get('department','')
    group_filter = request.GET.get('group','')
    
    members = Member.objects.all()
    if search:
        members = members.filter(name__icontains=search)
    
    if department_filter:
        members = members.filter(department_id=department_filter)
        
    if group_filter:
        members = members.filter(group_id=group_filter)
        
    departments = Department.objects.all()
    groups = Group.objects.all()
       
    return render(request, 'doanvien/member_list.html',{
        'members':members,
        'search': search,
        'departments': departments,
        'groups': groups,
        'selected_department': department_filter,
        'selected_group': group_filter,
    })
    
def edit_member(request,pk):
    member = get_object_or_404(Member,pk=pk)
    if request.method == 'POST':
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:   
            return render(request, 'doanvien/edit_member.html',{'form':form,'member':member})
    else:
        form = MemberForm(instance=member)
        
    return render(request, 'doanvien/edit_member.html', {'form': form, 'member': member})

def delete_member(request,pk):
    member = get_object_or_404(Member,pk=pk)
    if request.method == 'POST':
        member.delete()
        return redirect('/')

    return render(request,'doanvien/delete_member.html',{'member':member})

def member_stats(request):
    department_stats = (
        Member.objects.values('department__name')
        .annotate(total=Count('id'))
        .order_by('-total')
    )
    
    group_stats = (
        Member.objects.values('group__name')
        .annotate(total=Count('id'))
        .order_by('-total')
    )
    
    return render(request, 'doanvien/member_stats.html', {
        'department_stats': department_stats,
        'group_stats': group_stats,
    })
    
def export_member_list(request):
    # Tạo Workbook mới
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Danh sách Đoàn viên"

    # Header
    headers = ['STT', 'Họ tên', 'Giới tính', 'Khoa/Phòng', 'Tổ', 'Tình trạng', 'Ghi chú']
    ws.append(headers)

    # In đậm Header
    for cell in ws[1]:
        cell.font = Font(bold=True)

    # Lấy dữ liệu từ database
    members = Member.objects.all()
    for index, member in enumerate(members,start=1):
        ws.append([
            index,
            member.name,
            member.gender,
            member.department.name if member.department else "",
            member.group.name if member.group else "",
            member.status,
            member.note if member.note else ""
        ])

    # Tạo response để tải file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Danh_sach_doan_vien.xlsx'
    wb.save(response)

    return response