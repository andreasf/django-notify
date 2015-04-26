from models import Challenge, get_user, get_mac
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import email
import json
import datetime
from django.core.mail import EmailMessage
from django.conf import settings

FROM = settings.NOTIFY_FROM

"""
Protocol example
1. client requests challenge: GET /notify/name
2. server responds with challenge
3. client posts notification: POST /notify/name/subject
   {
       "message": "<message>",
       "subject". "<subject>",
       "mac": hmac_sha512(subject + message, challenge + key)
   }
"""


@csrf_exempt
def notify(request, challenge):
    if request.method == "OPTIONS":
        resp = HttpResponse()
        resp["Allow"] = "POST"
        return resp
    elif request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    challenge = get_object_or_404(Challenge, code=challenge)
    addr = challenge.destination.email
    code = challenge.code
    key = challenge.destination.key
    try:
        req = json.loads(request.body)
        subject = req["subject"]
        mac = req["mac"]
        message = req["message"]
        print "subject: " + subject
        print "mac: " + mac
        my_mac = get_mac(subject, message, code, key)
        if my_mac != mac:
            return HttpResponseBadRequest()
        challenge.delete()
        send_mail(addr, subject, message)
        return HttpResponse("OK")
    except (KeyError, ValueError):
        return HttpResponseBadRequest()


def send_mail(addr, subject, message):
    # force 7bit/8bit content-transfer-encoding for text instead of base64
    if addr != "honeypot":
        email.charset.add_charset('utf-8', email.charset.SHORTEST, None, None)
        mail = EmailMessage(subject=subject.encode("utf-8"),
                            from_email=FROM, to=[addr], body=message.encode("utf-8"))
        mail.send()


def make_challenge(request, username):
    user = get_user(username)
    done = False
    while not done:
        try:
            challenge = Challenge(destination=user)
            challenge.save()
            done = True
        except IntegrityError:
            pass
    # occasional cleanup
    if challenge.code[1] == "0":
        Challenge.objects.filter(valid_until__lt=datetime.now()).delete()
    return HttpResponse(challenge.code)
