#generate one type token for email confirmation , this prevents spams !

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.email_confirmed) + 'add_raandom_string_to_be_on a_safer_side'
        )

account_activation_token = AccountActivationTokenGenerator()