from django.db import models


class Emails(models.Model):
    sender = models.ForeignKey(
        "Users", on_delete=models.CASCADE, related_name="wrote", to_field="username"
    )
    reciever = models.ForeignKey(
        "Users", on_delete=models.CASCADE, related_name="recieved", to_field="username"
    )
    datetime_of_arrival = models.DateTimeField()
    encrypted_subject = models.TextField()
    encrypted_body = models.TextField()
    synced = models.BooleanField(default=False)


class Users(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, primary_key=True, unique=True)
    public_key = models.CharField(max_length=100)
    salt = models.CharField(max_length=100)
    hashed_password = models.CharField(max_length=100)
