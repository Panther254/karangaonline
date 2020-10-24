from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import  UserRegisterForm, UserUpdateForm, CustomerUpdateForm
from django.contrib.auth.decorators import login_required
from hotel.models import Customer



# Create your views here.
def register(request):
	if request.method == 'POST':
		form =  UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f"Your Account Has been Created! You can Now Log In")
			return redirect('login')
	else:
		form =  UserRegisterForm()
	return render(request, 'users/register.html', {'form': form})


@login_required
def profiles(request): 
	user = request.user
	if request.method == 'POST':
		customerData = Customer.objects.get(user=user) 
		u_form = UserUpdateForm(request.POST, instance=user)
		c_form = CustomerUpdateForm(request.POST, request.FILES, instance=user.customer)
		if u_form.is_valid() and c_form.is_valid():
			u_form.save()
			c_form.save()
			messages.success(request,f"Your Profile has been Updated Successfully")
			return redirect('profiles')
	else:
		customerData = Customer.objects.get(user=user)
		u_form = UserUpdateForm(instance=user)
		c_form = CustomerUpdateForm(instance=user.customer)

	
	return render(request, 'users/profiles.html',{'customerData':customerData, 'u_form':u_form, 'c_form':c_form})