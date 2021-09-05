from django.core.mail import EmailMessage


def send_mail(email, confirmation_link, first_name):

    email = EmailMessage(
        to=[f"{email}"],
    )

    email.from_email = None
    email.template_id = '3148660'
    email.merge_global_data = {
        'first_name': first_name,
        'confirmation_link': confirmation_link

    }
    email.send()
    return email
