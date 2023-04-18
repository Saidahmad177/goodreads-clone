from django.db import models
from users.models import CustomUser


class Friends(models.Model):
    requester = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='requester')
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='recipient')
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"from [{self.requester}] to [{self.recipient}]"



