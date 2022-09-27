from django.contrib.auth.tokens import default_token_generator
from rest_framework.reverse import reverse
from base64 import urlsafe_b64encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string

def verification_email(user):
    confirmation_token = default_token_generator.make_token(user)
    subject = 'Activate Your cBook Account'
            #actiavation_link = f'{activate_link_url}/user_id={user.i}&confirmation_token={confirmation_token}'
    data = {
            'user': user,
            'url': reverse('activate', args=[urlsafe_b64encode(force_bytes(user.pk)).decode('utf8'), confirmation_token])
            }
    message = render_to_string("email/cbook-update-password.html", data)
    return subject, message