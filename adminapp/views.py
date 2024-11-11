import calendar
from datetime import datetime, timedelta
import string
import random
from django.shortcuts import render, redirect, get_object_or_404
from .forms import TaskForm
from .models import Task
# Create your views here.
def projecthomepage(request):
    return render(request, 'adminapp/ProjectHomePage.html')
def printpagecall(request):
    return render(request, 'adminapp/printer.html')
def printpagelogic(request):
    user_input = None
    if request.method == "POST":
        user_input = request.POST.get('user_input')
        if user_input:
            print(f'User input: {user_input}')
    return render(request, 'adminapp/printer.html', {'user_input': user_input})
def exceptionpagecall(request):
    return render(request, 'adminapp/ExceptionExample.html')
def exceptionpagelogic(request):
    result = None
    error_message = None
    if request.method == "POST":
        user_input = request.POST.get('user_input')
        try:
            num = int(user_input)
            result = 10 / num
        except (ValueError, ZeroDivisionError) as e:
            error_message = str(e)
    return render(request, 'adminapp/ExceptionExample.html', {'result': result, 'error': error_message})
def randompagecall(request):
    return render(request, 'adminapp/randomexample.html')
def randompagelogic(request):
    random_string = None
    if request.method == "POST":
        number1 = int(request.POST.get('number1', 0))
        random_string = ''.join(random.sample(string.ascii_uppercase + string.digits, k=number1))
    return render(request, 'adminapp/randomexample.html', {'ran': random_string})
def calculatorpagecall(request):
    return render(request, 'adminapp/calculatorexample.html')
def calculatorpagelogic(request):
    result = None
    error_message = None
    if request.method == 'POST':
        try:
            num1 = float(request.POST.get('num1', 0))
            num2 = float(request.POST.get('num2', 0))
            operation = request.POST.get('operation')
            if operation == 'add':
                result = num1 + num2
            elif operation == 'subtract':
                result = num1 - num2
            elif operation == 'multiply':
                result = num1 * num2
            elif operation == 'divide':
                result = num1 / num2 if num2 != 0 else 'Infinity'
        except (ValueError, ZeroDivisionError) as e:
            error_message = str(e)
    return render(request, 'adminapp/calculatorexample.html', {'result': result, 'error': error_message})
def datetimepagecall(request):
    return render(request, 'adminapp/datetimepage.html')
def datetimepagelogic(request):
    if request.method == "POST":
        try:
            number1 = int(request.POST['date1'])
        except (KeyError, ValueError):
            return render(request, 'adminapp/datetimepage.html',
                          {'error': 'Invalid input. Please enter a valid number.'})

        x = datetime.now()
        ran = x + timedelta(days=number1)
        ran1 = ran.year
        ran3 = "Leap Year" if calendar.isleap(ran1) else "Not leap year"

        a1 = {'ran': ran, 'ran3': ran3, 'ran1': ran1, 'number1': number1}
        return render(request, 'adminapp/datetimepage.html', a1)

    return render(request, 'adminapp/datetimepage.html')
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_task')
    else:
        form = TaskForm()
    tasks = Task.objects.all()
    return render(request, 'adminapp/add_task.html', {'form': form, 'tasks': tasks})
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return redirect('add_task')
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.shortcuts import render
def UserRegisterPageCall(request):
    return render(request, 'adminapp/register.html')
def UserRegisterLogic(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        pass1 = request.POST['password']
        pass2 = request.POST['password1']

        if pass1 == pass2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'OOPS! Username already taken.')
                return render(request, 'adminapp/register.html')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'OOPS! Email already registered.')
                return render(request, 'adminapp/register.html')
            else:
                user = User.objects.create_user(
                    username=username,
                    password=pass1,
                    first_name=first_name,
                    last_name=last_name,
                    email=email
                )
                user.save()
                messages.info(request, 'Account created Successfully!')
                return render(request, 'adminapp/ProjectHomePage.html')
        else:
            messages.info(request, 'Passwords do not match.')
            return render(request, 'adminapp/register.html')
    else:
        return render(request, 'adminapp/register.html')

from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect








def UserLoginPageCall(request):
    return render(request, 'adminapp/login.html')

def UserLoginLogic(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            if len(username) == 10:
                # Redirect to StudentHomePage
                messages.success(request, 'Login successful as student!')
                return redirect('studentapp:StudentHomePage')  # Replace with your student homepage URL name
                # return render(request, 'facultyapp/FacultyHomepage.html')
            elif len(username) == 4:
                # Redirect to FacultyHomePage
                # messages.success(request, 'Login successful as faculty!')
                return redirect('facultyapp:FacultyHomePage')  # Replace with your faculty homepage URL name
                # return render(request, 'facultyapp/FacultyHomepage.html')
            else:
                # Invalid username length
                messages.error(request, 'Username length does not match student or faculty criteria.')
                return render(request, 'adminapp/login.html')
        else:
            # If authentication fails
            messages.error(request, 'Invalid username or password.')
            return render(request, 'adminapp/login.html')
    else:
        return render(request, 'adminapp/login.html')

def logout(request):
    auth.logout(request)
    return redirect('projecthomepage')

# from .forms import StudentForm
# from .models import StudentList
#
# def add_student(request):
#    if request.method == 'POST':
#        form = StudentForm(request.POST)
#        if form.is_valid():
#            form.save()
#            return redirect('student_list')
#     else:
#        form = StudentForm()
#     return render(request, 'adminapp/add_student.html', {'form': form})
from django.contrib.auth.models import User
from .models import StudentList
from .forms import StudentForm
from django.shortcuts import redirect, render
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            register_number = form.cleaned_data['Register_Number']
            try:
                user = User.objects.get(username=register_number)
                student.user = user  # Assign the matching User to the student
            except User.DoesNotExist:
                form.add_error('Register_Number', 'No user found with this Register Number')
                return render(request, 'adminapp/add_student.html', {'form': form})
            student.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'adminapp/add_student.html', {'form': form})
def student_list(request):
    students = StudentList.objects.all()
    return render(request, 'adminapp/student_list.html', {'students': students})
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.contrib import messages
from .models import Contact
from .forms import ContactForm
from django.conf import settings

# Add Contact
def add_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            messages.success(request, "Contact created successfully!")
            # Optional Email Notification
            if 'send_email' in request.POST:
                recipient_email = request.POST.get('recipient_email')
                if recipient_email:
                    send_mail(
                        'New Contact Added',
                        f"Details:\nName: {contact.name}\nEmail: {contact.email}\nPhone: {contact.phone}\nAddress: {contact.address}",
                        settings.DEFAULT_FROM_EMAIL,
                        [recipient_email]
                    )
                    messages.success(request, f"Email sent to {recipient_email}")
            return redirect('list_contacts')
    else:
        form = ContactForm()
    return render(request, 'adminapp/add_contacts.html', {'form': form})

# List and Search Contacts
def list_contacts(request):
    query = request.GET.get('query')
    contacts = Contact.objects.all()
    if query:
        contacts = contacts.filter(models.Q(name__icontains=query) | models.Q(email__icontains=query))
    return render(request, 'adminapp/list_contacts.html', {'contacts': contacts})

# Delete Contact
def delete_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    contact.delete()
    messages.success(request, "Contact deleted successfully!")
    return redirect('list_contacts')