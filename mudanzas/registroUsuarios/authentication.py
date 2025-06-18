from django.contrib.auth import get_user_model

Usuario = get_user_model()

class EmailAuthBackend:
    """Backend de autenticación que permite login con email en lugar de username."""

    def authenticate(self, request, email=None, password=None):  # Cambiar username -> email
        try:
            usuario = Usuario.objects.get(email=email)  # Busca usuario por email correctamente
            if usuario.check_password(password):
                return usuario  # Devuelve el usuario autenticado
        except Usuario.DoesNotExist:
            return None
        return None  # Retorna None si el usuario no existe o la contraseña es incorrecta

    def get_user(self, user_id):
        try:
            return Usuario.objects.get(pk=user_id)  # Devuelve el usuario por ID
        except Usuario.DoesNotExist:
            return None
