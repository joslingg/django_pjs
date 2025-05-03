from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm,CustomUserCreationForm  # <-- nhớ import form
from django.shortcuts import get_object_or_404
from unidecode import unidecode
import csv
from django.http import HttpResponse
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


@login_required
def taskList(request):
    search_input = request.GET.get('search','')
    status_filter = request.GET.get('status','')
    form = TaskForm()
    
    tasks = Task.objects.filter(user=request.user).order_by('-created_at')
    
    total_tasks = len(tasks)
    completed_tasks = len([t for t in tasks if t.completed])
    pending_tasks = len([t for t in tasks if not t.completed])
    
    # Nếu có từ khoá tìm kiếm
    if search_input:
        normalized_input = unidecode(search_input.lower())
        tasks = [t for t in tasks if normalized_input in unidecode(t.title.lower())]

    # Nếu có filter trạng thái
    if status_filter == 'completed':
        tasks = [t for t in tasks if t.completed]
    elif status_filter == 'pending':
        tasks = [t for t in tasks if not t.completed]
        
        
    form = TaskForm()
    
    if request.method == 'POST':
        if 'title' in request.POST:
            form = TaskForm(request.POST)
            if form.is_valid():
                task = form.save(commit=False)
                task.user = request.user
                task.save()
        elif 'task_id' in request.POST:
            task = Task.objects.get(id=request.POST['task_id'])
            task.completed = not task.completed
            task.save()
        return redirect('/')
    
    context = {'tasks':tasks,
                'form':form,
                'total_tasks': total_tasks,
                'completed_tasks': completed_tasks,
                'pending_tasks': pending_tasks,
                }
    return render(request,'todo/task_list.html',context)

def deleteTask(request,pk):
    task = get_object_or_404(Task,id=pk)
    task.delete()
    return redirect('/')

def editTask(request,pk):
    task = get_object_or_404(Task,id=pk)
    form = TaskForm(instance=task)
    
    if request.method=='POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('/')
    
    return render(request, 'todo/edit_task.html',{'form':form})

def export_csv(request):
    # Tạo response dùng encoding UTF-8 with BOM để Excel hiểu
    response = HttpResponse(
        content_type='text/csv; charset=utf-8-sig'
    )
    response['Content-Disposition'] = 'attachment; filename="cong_viec.csv"'

    # Ghi BOM (Byte Order Mark) đầu file để Excel đọc đúng font
    writer = csv.writer(response)
    writer.writerow(['Tên công việc', 'Trạng thái', 'Ngày tạo'])

    tasks = Task.objects.all().order_by('-created_at')
    for task in tasks:
        trang_thai = 'Đã hoàn thành' if task.completed else 'Chưa làm'
        writer.writerow([task.title, trang_thai, task.created_at.strftime("%d/%m/%Y %H:%M")])

    return response

def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    
    form = CustomUserCreationForm()
    if request.method =='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('/')
        
    return render(request,'todo/register.html',{'form':form})