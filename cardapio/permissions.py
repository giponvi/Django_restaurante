from rest_framework import permissions


# permissão personalizada
# qualquer um que queria utilizar métodos seguros, consegue normalmente
# mas se não, e caso o user não seja admin e registrado, ele não consegue fazer e retorna false
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            if request.user.is_authenticated and request.user.is_staff:
                return True
        return False