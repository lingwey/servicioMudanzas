from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Cliente, ChoferParticular, Empresa

class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ["email", "nombre", "tipo_usuario", "is_staff"]
    search_fields = ["email", "nombre"]
    ordering = ["email"]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Información personal", {"fields": ("nombre", "tipo_usuario")}),
        ("Permisos", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Fechas", {"fields": ("fecha_creacion",)}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "nombre", "tipo_usuario", "password1", "password2"),
        }),
    )

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Cliente)
admin.site.register(ChoferParticular)
admin.site.register(Empresa)
