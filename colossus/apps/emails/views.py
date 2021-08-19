from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from decouple import config
import os

from .forms import EmailForms
from .models import EmailUsers


@login_required
def get_email_details(request):
    if request.method == 'POST':
        form = EmailForms(request.POST)
        if form.is_valid():
            email_default = form.cleaned_data['email_default']
            email_server = form.cleaned_data['email_server']
            email_backend = form.cleaned_data['email_backend']
            email_host = form.cleaned_data['email_host']
            email_port = form.cleaned_data['email_port']
            email_host_user = form.cleaned_data['email_host_user']
            email_host_password = form.cleaned_data['email_host_password']
            email_default_text = form.cleaned_data['email_default_text']
            user = request.user
            try:
                email_detail = EmailUsers.objects.get(user=user)
                email_detail.email_default = email_default
                email_detail.email_server = email_server
                email_detail.email_backend = email_backend
                email_detail.email_host = email_host
                email_detail.email_port = email_port
                email_detail.email_host_user = email_host_user
                email_detail.email_host_password = make_password(email_host_password)
                email_detail.email_default_text = email_default_text
                email_detail.save()
            except EmailUsers.DoesNotExist:
                email_details = EmailUsers.objects.create(
                    user=user,
                    email_default=email_default,
                    email_host_user=email_host_user,
                    email_host_password=make_password(email_host_password),
                    email_server=email_server,
                    email_backend=email_backend,
                    email_port=email_port,
                    email_host=email_host,
                    email_default_text=email_default_text
                )
                email_details.save()

            os.environ["DEFAULT_FROM_EMAIL"] = email_default
            os.environ["SERVER_EMAIL"] = email_server
            os.environ["EMAIL_BACKEND"] = email_backend
            os.environ["EMAIL_HOST"] = email_host
            os.environ["EMAIL_PORT"] = email_port
            os.environ["EMAIL_HOST_USER"] = email_host_user
            os.environ["EMAIL_HOST_PASSWORD"] = email_host_password
            os.environ["EMAIL_USE_TLS"] = "True"
            print(config('SERVER_EMAIL'))
            return render(
                request,
                'emails/email_setup.html',
                {
                    'form': form,
                    'success': 'Email Settings  Are Configred'
                }
            )

    else:
        email_form = EmailForms()
        return render(
            request,
            'emails/email_setup.html',
            {
                'menu': 'emails',
                'form': email_form
            }
        )
