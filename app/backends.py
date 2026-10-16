# backends.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from .models import TenantUser
class TenantUserBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()
        try:
            user1 = User.objects.get(username=username)
            tenant1 = request.tenant
            testten=TenantUser.objects.filter(user=user1,tenant=tenant1)
            if testten and user1.check_password(password):
                return user1
        except User.DoesNotExist:
            return None