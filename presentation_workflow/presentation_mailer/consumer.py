from django.core.mail import send_mail
import json
import pika
import django
import os
import sys


sys.path.append("")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "presentation_mailer.settings")
django.setup()


def process_approval(ch, method, properties, body):
    print("  Received %r" % body)
    accept_mail = json.loads(body)
    send_mail(
        "Your presentation has been accepted",
        f'Hello, {accept_mail["presenter_name"]} your presentation has been accepted.',
        "admin@conference.go",
        [accept_mail["presenter_email"]],
        fail_silently=False,
    )

def process_rejection(ch, method, properties, body):
    print("  Received %r" % body)
    reject_mail = json.loads(body)
    send_mail(
        "Your presentation has been rejected",
        f'Sorry, {reject_mail["presenter_name"]} but your presentation has been rejected.',
        "admin@conference.go",
        [reject_mail["presenter_email"]],
        fail_silently=False,
    )


def main():
    parameters = pika.ConnectionParameters(host="rabbitmq")
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue="presentation_approvals")
    channel.basic_consume(
        queue="presentation_approvals",
        on_message_callback=process_approval,
        auto_ack=True,
    )
    channel.queue_declare(queue="presentation_rejections")
    channel.basic_consume(
        queue="presentation_rejections",
        on_message_callback=process_rejection,
        auto_ack=True,
    )
    channel.start_consuming()







if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
