from rest_framework import permissions


class OnlyAdminPermissions(permissions.BasePermission):

    message = 'Доступ разрешен только администраторам'

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.is_admin_or_superuser)


class IsAdminOrReadOnly(permissions.BasePermission):

    message = 'Редактировать разрешено только Администаторам'

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (request.user.is_admin_or_superuser)


class ReadOnlyOrAuthorOrAdmin(permissions.BasePermission):

    message = 'Вы не можете совершать данную операцию'

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated
                and request.user.is_admin_or_moderator)
            or (request.user.is_authenticated
                and request.user == obj.author)
        )
