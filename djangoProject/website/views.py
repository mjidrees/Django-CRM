from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm, SearchForm
from .models import Record
from django.contrib.auth.models import User

# Create your views here.
def home(request):
    records = Record.objects.all()
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)
        if user is not None:

            login(request, user)
            messages.success(request, "You have been logged in!")
            print('success')
            return redirect('home') 
        else:
            messages.error(request, "Error logging in. Please try again.")
            print('Faliure')
            return redirect('home') 
    else:
        print('rendering')
        return render(request, 'home.html', {'records': records})
    
def user(request):
    records = User.objects.all()
    if request.user.is_authenticated:
        return render(request, 'user.html', {'records': records})
    


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out!")
    return redirect('home')  

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            #Authinticatie to login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password= password)
            login(request, user)
            messages.success(request,'You have been registered!!!')
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html',{'form': form})
    return render(request, 'register.html',{'form': form})

def customer_record(request,pk):
    if request.user.is_authenticated:
        individual_record= Record.objects.get(id=pk)
        return render(request, 'record.html',{'individual_record': individual_record})
    else:
        messages.success(request,'You must be logged in to view details!!!')
        return redirect('home')
    
def delete_record(request,pk):
    if request.user.is_authenticated:
        delete_it=Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request,'Record deleted successfully!!!')
        return redirect('home')
    else:
        messages.success(request,'You must be logged in!!!')
        return redirect('home')
    
def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request,'Record Added!!!')
                return redirect('home')


        return render(request, 'add_record.html',{'form':form})
    else:
        messages.success(request,'You must be logged in!!!')
        return redirect('home')
    
def update_record(request,pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None,instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request,'Record Update!!!')
            return redirect('home')
        return render(request, 'update_record.html',{'form':form})
    else:
        messages.success(request,'You must be logged in!!!')
        return redirect('home')
    
def search_view(request):
    form = SearchForm(request.POST or None)
    results = []

    if request.method == 'POST':
        if form.is_valid():
            id_query = form.cleaned_data.get('id')
            state_query = form.cleaned_data.get('state')
            country_query = form.cleaned_data.get('country')

            # Filter based on which fields have values
            if id_query:
                results = Record.objects.filter(id=id_query)
            elif state_query:
                results = Record.objects.filter(state__icontains=state_query)
            elif country_query:
                results = Record.objects.filter(country__icontains=country_query)

    return render(request, 'search.html', {'form': form, 'results': results})