from io import BytesIO
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from django.conf import settings
import weasyprint


def order_created(order):
    subject = f'PMATEL - Commande Numéro° {order.id}'
    message = f'Cher/Chère {order.first_name},\n' \
              f'Vous avez passé une commande avec succès, veuillez trouver votre facture en piece jointe.'

    email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [order.email])
    html = render_to_string('admin/orders/order/pdf.html', {"order":order})
    out = BytesIO()
    #stylesheets = [weasyprint.CSS(settings.STATIC_ROOT + '/css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out)

     # attach PDF file
    email.attach(f'order_{order.id}.pdf', out.getvalue(), 'application/pdf')
    email.send()

    return True;

# @task
# def order_validated(order_id):

#     order = Order.objects.get(id=order_id)
#     subject = f'PMATEL - Commande Numéro° {order.id}'
#     message = 'Merci de nous avoir fait confiance.\n Veuillez trouver votre facture en piece jointe.'
#     email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [order.email])
#     html = render_to_string('orders/order/pdf.html', {"order":order})
#     out = BytesIO()
#     stylesheets = [weasyprint.CSS(settings.STATIC_ROOT + '/css/pdf.css')]
#     weasyprint.HTML(string=html).write_pdf(out)

#      # attach PDF file
#     email.attach(f'order_{order.id}.pdf', out.getvalue(), 'application/pdf')
#     email.send()