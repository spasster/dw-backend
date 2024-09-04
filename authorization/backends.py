from django.contrib.auth.backends import BaseBackend
from authorization.models import DwUser, Role

class RoleBasedBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        print("RoleBasedBackend.authenticate called")
        try:
            user = DwUser.objects.get(username=username)
            if user.check_password(password):
                return user
        except DwUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        print("RoleBasedBackend.get_user called")
        try:
            return DwUser.objects.get(pk=user_id)
        except DwUser.DoesNotExist:
            return None

    def has_perm(self, user_obj, perm, obj=None):
        if isinstance(user_obj, DwUser):
            return user_obj.role in [Role.MANAGER.value, Role.CEO.value]
        return False

    def has_module_perms(self, user_obj, app_label):
        if isinstance(user_obj, DwUser):
            return user_obj.role in [Role.MANAGER.value, Role.CEO.value]
        return False

