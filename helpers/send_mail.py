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


def send_verification(name, email, url, code):
    return mail_sender(subject="Verification Code", recipient_list=[
        email], message=f"Thanks for registering kindly verify your email by clicking this link {url}",
        html_message=f"<h1>Hello {name}</h1> \
        <h3>Thanks for registering Please verify your email </h3> \
        <p>Copy the verification code or click the verify button to verify</p> \
        <p> Code: {code}</p> \
        <a style='margin: 1rem 0; padding: 1rem; color: #fff; background-color: #27ae60; border: none; border-radius: 7px; text-decoration: none;' href='{url}'>Verify</a>")
