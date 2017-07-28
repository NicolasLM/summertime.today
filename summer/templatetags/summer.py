from django import template


register = template.Library()


@register.simple_tag
def user_has_usable_password(user) -> bool:
    return user.has_usable_password()
