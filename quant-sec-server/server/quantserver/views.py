from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializer import UserSerializer, EmailSerializer
from .models import Users, Emails
from .utils import verifyUser
import datetime
import os
import base64
import hashlib


@api_view(["GET"])
def getUserPublicKey(request):
    username = request.GET.get("username")

    if username == None:
        return Response({"Message": "Invalid request", "Status": "Negative"})
    user = Users.objects.filter(username=username).all()
    if len(user) < 1:
        return Response({"Message": "The user doesn't exist", "Status": "Negative"})

    serializer = UserSerializer(user[0]).data
    return Response(
        {
            "Message": "Request succesfully executed",
            "Status": "Positive",
            "Name": serializer["name"],
            "Public Key": serializer["public_key"],
        }
    )


@api_view(["POST"])
def postEmail(request):
    reciever_username = ""
    sender_username = ""
    aes_encrypted_subject = ""
    aes_encrypted_body = ""
    sender_password = ""

    try:
        reciever_username = request.data["reciever_username"]
        sender_username = request.data["sender_username"]
        aes_encrypted_subject = request.data["subject"]
        aes_encrypted_body = request.data["body"]
        sender_password = request.data["password"]
    except:
        return Response({"Message": "Invalid request", "Status": "Negative"})

    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        sender = Users.objects.get(username=sender_username)
        if not verifyUser(sender, sender_password):
            return Response({"Message": "Request denied", "Status": "Negative"})
        reciever = Users.objects.get(username=reciever_username)
    except:
        return Response(
            {
                "Message": "Email parties don't belong the pool of registered users",
                "Status": "Negative",
            }
        )

    Emails.objects.create(
        sender=sender,
        reciever=reciever,
        datetime_of_arrival=current_datetime,
        encrypted_subject=aes_encrypted_subject,
        encrypted_body=aes_encrypted_body,
    )

    return Response({"Message": "Email sent succesfully", "Status": "Positive"})


@api_view(["GET"])
def checkForUniqueness(request):
    username = request.GET.get("username")

    if username == None:
        return Response({"Message": "Invalid request", "Status": "Negative"})
    user = Users.objects.filter(username=username).all()
    if len(user) < 1:
        return Response({"Message": "The user doesn't exist", "Status": "Positive"})
    else:
        return Response(
            {"Message": "A user exists with this username", "Status": "Negative"}
        )


@api_view(["POST"])
def registerUser(request):
    name = ""
    username = ""
    public_key = ""
    password = ""

    try:
        name = request.data["name"]
        username = request.data["username"]
        public_key = request.data["public_key"]
        password = request.data["password"]
    except:
        return Response({"Message": "Invalid Request", "Status": "Negative"})
    random_salt = str(base64.b64encode(os.urandom(20)), encoding="utf-8")
    hashed_password = hashlib.sha256(
        str(password + random_salt).encode("utf-8")
    ).hexdigest()

    user = Users(
        name=name,
        username=username,
        public_key=public_key,
        salt=random_salt,
        hashed_password=hashed_password,
    )

    try:
        user.save()
    except:
        return Response({"Message": "Some error occured", "Status": "Negative"})

    return Response({"Message": "User registered", "Status": "Positive"})


@api_view(["GET"])
def returnInbox(request):
    username = request.GET.get("username")
    password = request.GET.get("password")

    if username == None or password == None:
        return Response({"Message": "Invalid Request", "Status": "Negative"})

    user = Users.objects.get(username=username)
    if not verifyUser(user, password):
        return Response({"Message": "Request denied", "Status": "Negative"})

    emails = user.recieved.filter(synced=False)
    print(emails)
    serializer = EmailSerializer(emails, many=True).data
    for email in emails:
        email.synced = True
        email.save()

    return Response(
        {"Message": "Request completed", "Status": "Positive", "Emails": serializer}
    )


@api_view(["POST"])
def clearInbox(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username == None or password == None:
        return Response({"Message": "Invalid Request", "Status": "Negative"})

    user = Users.objects.get(username=username)
    if not verifyUser(user, password):
        return Response({"Message": "Request denied", "Status": "Negative"})

    user.recieved.all().delete()

    return Response({"Message": "Deletion succesfull", "Status": "Positive"})
