from .forms import UserLoginForm, UserRegistrationForm, ProfileForm
from django.conf import settings
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.views import LoginView
from django.contrib import auth
from django.contrib.auth.decorators import login_required

def index(request):
    context = {
        'title': _('Stay Zen, Stay Secure'),
        'content': _("""
Welcome to our super SecureZen site.
We help you to stay secure at all times.
STAY ON THE SAFE SIDE
                     """),
    }
    return render(request, 'main/index.html', context)

def contact(request):
    context = {
        'title': _('Contact Information'),
        'text_on_page': _("""
            Our offices located in:
            - Address: Berlin, Potsdam, Onemorestadt
            
            - Telephone: 110
            
            - Email: everywhere@gmail.com
        """)
    }
    return render(request, 'main/contact.html', context)

def about(request):
    context = {
        'title': _('About Our Service'),
        'content': _("""
SecureZen is a cutting-edge security service offered by a dedicated team of professionals. 
Our mission is to safeguard your digital assets and provide peace of mind through comprehensive security checks.
Leveraging the power of the renowned VirusTotal API, we offer robust security assessments to protect against online threats.

With SecureZen, you can trust that your systems are thoroughly scrutinized for vulnerabilities,
malware, and other malicious activities. Our seamless integration with VirusTotal enables us
to deliver accurate and timely results, empowering you to make informed decisions about your cybersecurity posture.

Whether you're a small business, a large enterprise, or an individual user, SecureZen caters to all
your security needs. From website scanning to file analysis, we offer a range of services tailored
to fit your requirements. Our team of experts is committed to providing top-notch support and guidance every step of the way.

Experience the peace of mind that comes with knowing your digital assets are in safe hands. 
Choose SecureZen for comprehensive security checks powered by VirusTotal's industry-leading technology.
Stay ahead of online threats and keep your digital ecosystem secure with SecureZen.
        """)
    }
    return render(request, 'main/about.html', context)

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)

            if user:
                auth.login(request, user)
                messages.success(request, f"{username}, you have successfully logged in")

                redirect_page = request.POST.get('next', None)
                if redirect_page and redirect_page != reverse('secure:logout'):
                    return HttpResponseRedirect(request.POST.get('next'))
                    
                return HttpResponseRedirect(reverse('secure:index'))
    else:
        form = UserLoginForm()

    context = {
        'title': 'Home - Authorization',
        'form': form
    }
    return render(request, 'users/login.html', context)

def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            
            user = form.instance
            messages.success(request, f"{user.username}, You have successfully registered")
            return HttpResponseRedirect(reverse('secure:login'))
        else:
            # Print form errors for debugging
            print("Form errors:", form.errors)
            messages.error(request, "Registration failed. Please correct the errors.")
    else:
        form = UserRegistrationForm()

    context = {
        'title': 'Home - Registration',
        'form': form
    }
    return render(request, 'users/registration.html', context)

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile successfully updated")
            return HttpResponseRedirect(reverse('secure:index'))
    else:
        form = ProfileForm(instance=request.user)     

    context = {
        'title': 'Home - Profile',
        'form': form,
    }
    return render(request, 'users/profile.html', context)

@login_required
def logout_view(request):
    username = request.user.username  # Store the username
    auth.logout(request)
    messages.success(request, f"{username}, you have logged out")  # Use the stored username
    return redirect(reverse('secure:index'))

def custom_404(request, exception):
    return render(request, 'main/error_404.html', status=404)

class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    