from django.core.mail import send_mail

def mail_sender(subject, recipient_list, message, html_message):
    try:
        send_mail(
                subject=subject,
                from_email="themaxibot1@gmail.com",
                message=message,
                recipient_list=recipient_list,
                html_message=html_message,
                fail_silently=False
            )
        return "success"
    except Exception as e:
        print("Error Sending Mail", e)
        return "Failed"

def send_verification(name, email, url):
    return mail_sender(subject="Verification Code", recipient_list=[
        email], message=f"Thanks for registering kindly verify your email by clicking this link {url}",
        html_message=f"<h1>Hello {name}</h1> <p>Thanks for registering kindly verify your email by clicking this link {url}</p>")