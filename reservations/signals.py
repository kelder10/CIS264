from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from email.mime.image import MIMEImage
from .models import Reservation

@receiver(post_save, sender=Reservation)
def send_confirmation_on_save(sender, instance, created, **kwargs):
    if created:
        subject = f"Confirmation: Your Ride #{instance.id}"
        
        context = {
            'user': instance.user,
            'reservation': instance,
            'bike': instance.bike,
        }
        
        html_content = render_to_string('emails/confirmation_email.html', context)
        text_content = strip_tags(html_content)
        
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email='rentals@indiancreekcycles.com',
            to=[instance.user.email],
        )
        email.attach_alternative(html_content, "text/html")
        email.mixed_subtype = 'related'

        logo_path = r'C:\CIS264\IndianCreekCycle\indian-creek-cycles\indian-creek-cycles\static\images\logo\logo-emails.png'
        
        try:
            with open(logo_path, 'rb') as f:
                img = MIMEImage(f.read())
                img.add_header('Content-ID', '<logo_image>')
                img.add_header('Content-Disposition', 'inline', filename='logo-emails.png')
                email.attach(img)
        except FileNotFoundError:
            pass

        email.send(fail_silently=False) 