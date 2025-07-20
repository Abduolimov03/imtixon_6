import random, string
from pyexpat.errors import messages
from django.core.mail import send_mail
# from conf.settings import DEFAULT_FROM_EMAIL


def generate_code():
    letter = string.ascii_letters + string.digits
    return ''.join([letter[random.randint(0, len(letter) - 1)] for _ in range(6)])

def send_to_mail(email, code):
    subject = 'Tasdiqlash kodi'
    message = f'Sizning kodingiz {code}'
    send_mail(subject=subject, message=message, from_email=None, recipient_list=[email,])