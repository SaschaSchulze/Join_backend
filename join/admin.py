# admin.py
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist

# Funktion, um den Token des Benutzers abzurufen
def get_user_token(user):
    try:
        return Token.objects.get(user=user).key
    except ObjectDoesNotExist:
        return None

# Benutzer-Admin anpassen
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'user_token')

    # Methode zur Anzeige des Tokens im Admin Interface
    def user_token(self, obj):
        return get_user_token(obj)
    user_token.short_description = 'Token'

# Existierendes User Admin abmelden und das neue anmelden
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
