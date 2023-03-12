from functools import wraps
from typing import Callable, List, Optional

from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest, HttpResponse
from django.core.exceptions import PermissionDenied

from user.models import User


def has_roles(roles: List[User.UserRolesEnum]):
    def wrapper(cls):
        @wraps(cls)
        def check(self, request: HttpRequest, **kwargs):
            user: Optional[User] = request.user
            if isinstance(user, AnonymousUser):
                raise HttpResponse("J")
            has_role = False
            for role in roles:
                has_role |= user.has_role(role)
            if has_role:
                return cls(self, request, **kwargs)
            raise HttpResponse("J")
        return check
    return wrapper