from django.conf.urls import url
import quantserver.views as vi

urlpatterns = [
    url("get-public-key", vi.getUserPublicKey),
    url("post-email", vi.postEmail),
    url("register-user", vi.registerUser),
    url("check-uniqueness", vi.checkForUniqueness),
    url("get-inbox", vi.returnInbox),
    url("clear-inbox", vi.clearInbox),
]
