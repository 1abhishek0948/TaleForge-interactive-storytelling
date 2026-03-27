from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

DEMO_LOGIN_ACCOUNTS = (
    {
        "label": "Demo User",
        "username": "demo_user",
        "email": "demo@example.com",
        "password": "demoxyz12@",
        "is_staff": False,
        "is_superuser": False,
        "group": None,
    },
    {
        "label": "Moderator",
        "username": "moderator_user",
        "email": "moderator@example.com",
        "password": "moderatorxyz34@",
        "is_staff": True,
        "is_superuser": False,
        "group": "Moderators",
    },
    {
        "label": "Admin",
        "username": "admin_user",
        "email": "admin@example.com",
        "password": "adminxyz56@",
        "is_staff": True,
        "is_superuser": True,
        "group": "Admins",
    },
)


def _create_or_update_user(
    user_model,
    *,
    username: str,
    email: str,
    password: str,
    is_staff: bool,
    is_superuser: bool,
):
    user, _ = user_model.objects.get_or_create(
        username=username,
        defaults={
            "email": email,
            "is_staff": is_staff,
            "is_superuser": is_superuser,
        },
    )

    changed = False
    if user.email != email:
        user.email = email
        changed = True
    if user.is_staff != is_staff:
        user.is_staff = is_staff
        changed = True
    if user.is_superuser != is_superuser:
        user.is_superuser = is_superuser
        changed = True
    if not user.check_password(password):
        user.set_password(password)
        changed = True

    if changed:
        user.save()

    return user


def ensure_demo_login_users():
    """Create or update the default demo login accounts."""
    user_model = get_user_model()
    users_by_username = {}

    for account in DEMO_LOGIN_ACCOUNTS:
        user = _create_or_update_user(
            user_model,
            username=account["username"],
            email=account["email"],
            password=account["password"],
            is_staff=account["is_staff"],
            is_superuser=account["is_superuser"],
        )

        group_name = account.get("group")
        if group_name:
            group, _ = Group.objects.get_or_create(name=group_name)
            user.groups.add(group)

        users_by_username[account["username"]] = user

    return users_by_username
