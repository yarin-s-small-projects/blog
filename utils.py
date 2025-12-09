import smtplib

def send_mail(sender , password , reciver , subject,msg):
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=sender, password=password)
        connection.sendmail(
            from_addr=sender,
            to_addrs=reciver,
            msg=f"Subject:{subject}\n\n{msg}"
        )
    return True