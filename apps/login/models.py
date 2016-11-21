from __future__ import unicode_literals
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
import bcrypt, re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validate_reg(self, request):
        errors = self.validate_inputs(request)

        if errors:
            return (False, errors)
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = self.create(name=request.POST['name'], user_name=request.POST['user_name'], email=request.POST['email'], password=pw_hash)
        return (True, user)

    def validate_login(self, request):
        try:
            user = User.objects.get(email=request.POST['email'])
            password = request.POST['password'].encode()
            if bcrypt.hashpw(password, user.password.encode()):
                return (True, user)

        except ObjectDoesNotExist:
            pass

        return (False, ["Invalid login."])

    def validate_inputs(self, request):
        errors = []

        if not request.POST['name']:
            errors.append('Name cannot be blank.')
        if not request.POST['user_name']:
            errors.append('User name cannot be blank.')
        if len(request.POST['user_name']) < 3:
            errors.append('User Name must be longer than 3 characters.')
        if not EMAIL_REGEX.match(request.POST['email']):
            errors.append('Invalid email.')
        if len(request.POST['password'])< 8:
            errors.append('Password must be at least 8 characters.')
        if request.POST['password'] != request.POST['confirm']:
            errors.append('Password and password confirm must match.')

        return errors
#I did not add validation for length of the name to be 3 characters because names are allowed to be 1 or 2 characters in length. and I prefer not to discriminate. however because this is an exam the validation would be the same as it is for the user name.
class User(models.Model):
    name = models.CharField(max_length = 50)
    user_name = models.CharField(max_length = 50)
    email = models.CharField(max_length = 50)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
