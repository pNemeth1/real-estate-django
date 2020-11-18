from django.shortcuts import render, redirect
from django.contrib import messages, auth

# Django has a Usermodel built in!
from django.contrib.auth.models import User

from contacts.models import Contact


# Create your views here.
def register(request):
    if request.method == 'POST':
        #Register user
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        

        # Validation - do passwords match?
        if password == password2:
            #check username
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already taken')
                return redirect(register)
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email already in use')
                    return redirect(register)
                else:
                    user = User.objects.create_user(username=username, password=password, email=email, 
                    first_name=first_name, last_name=last_name)
                    #Login after registration
                    # auth.login(request, user)
                    # messages.success(request, 'You are now Logged In')
                    # return redirect('index')
                    user.save()
                    messages.success(request, 'You are now registered and can log in!')
                    return redirect(login_view)


            

        else:
            messages.error(request, 'Passwords Do Not Match!')
            return redirect(register)

    else:
        return render(request, 'accounts/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now Logged In')
            return redirect('dashboard')
            ...
        else:
            # Return an 'invalid login' error message.
            messages.error(request, 'Invalid username or password')
            return redirect(login_view)

        
    else:
        return render(request, 'accounts/login.html')

def logout_view(request):
    auth.logout(request)
    messages.info(request, 'You are now Logged Out')
    return redirect('index')

def dashboard(request):
    user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)

    context = {
        'contacts': user_contacts
    }
    return render(request, 'accounts/dashboard.html', context)