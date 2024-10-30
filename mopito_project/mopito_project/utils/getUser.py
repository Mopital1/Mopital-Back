

def get_user_name(self):
    """
        get user if is connected or not.Use on viewsets
    """
    if hasattr(self.request.user, "email"):
        return self.request.user.email
    else:
        return self.request.user


def _get_user_name_(self):
    """
        get user if is connected or not.Use on serializer
    """
    if hasattr(self.context["request"].user, "email"):
        return self.context["request"].user.email
    else:
        return self.context["request"].user
