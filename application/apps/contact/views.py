from django.shortcuts import render, render_to_response
from django.template.loader import get_template
from application import settings
from forms import *
from django.template import RequestContext, Context
from django.core.mail import send_mail


def index(request):
    if request.method == "POST":
        form = ContactForm(data=request.POST, request=request)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            email = form.cleaned_data['email']
            cc_myself = form.cleaned_data['cc_myself']

            recipients = ['lennart.sjoblom@bidpart.se']

            if cc_myself:
                recipients.append(email)

            email_message = get_template('contact/contact_email.txt').render(Context({
                'email': email,
                'subject': subject,
                'message': message
            }))

            send_mail(subject, email_message, settings.DEFAULT_FROM_EMAIL, recipients)

            form.save()

            return render_to_response('contact/contact_thanks.html', None, context_instance=RequestContext(request))
    else:
        form = ContactForm()

    return render(request, 'contact/contact_form.html', {
        'form': form,
    })
