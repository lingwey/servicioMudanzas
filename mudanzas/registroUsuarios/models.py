from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

# Validadores para DNI, CUIL y Patente
dni_validator = RegexValidator(regex=r'^\d{8}$', message="El DNI debe tener 8 dígitos numéricos.")
cuil_validator = RegexValidator(regex=r'^\d{2}-\d{8}-\d{1}$', message="El CUIL debe tener el formato correcto (XX-XXXXXXXX-X).")
patente_validator = RegexValidator(regex=r'^[A-Z]{2}\d{3}[A-Z]{2}$', message="El número de patente debe seguir el formato estándar (ej. AA123BB).")

# Modelo base de Usuario con corrección en grupos y permisos
class Usuario(AbstractUser):
    TIPO_USUARIO_CHOICES = [
        ("cliente", "Cliente"),
        ("chofer_particular", "Chofer Particular"),
        ("empresa", "Empresa")
    ]

    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=150)
    dni = models.CharField(max_length=8, validators=[dni_validator], blank=True, null=True)  # Solo para Cliente y Chofer
    cuil = models.CharField(max_length=13, validators=[cuil_validator], blank=True, null=True)  # Solo para Empresas
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_USUARIO_CHOICES)
    documento_verificado = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    # Correge el conflicto con `auth.User.groups` y `auth.User.user_permissions`
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="usuario_groups",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="usuario_permissions",
        blank=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nombre", "tipo_usuario"]

    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_usuario_display()})"

# Modelo de Cliente
class Cliente(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, limit_choices_to={'tipo_usuario': 'cliente'})
    subastas_creadas = models.IntegerField(default=0)

    def __str__(self):
        return f"Cliente: {self.usuario.nombre} - Subastas: {self.subastas_creadas}"

# Modelo de Chofer Particular con detalles optimizados
class ChoferParticular(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, limit_choices_to={'tipo_usuario': 'chofer_particular'})
    tipo_vehiculo = models.CharField(
        max_length=20,
        choices=[("auto", "Auto"), ("van", "Van"), ("camion", "Camión")]
    )
    tiene_acoplado = models.BooleanField(default=False)
    numero_patente = models.CharField(max_length=10, validators=[patente_validator], unique=True)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    seguro = models.CharField(max_length=255)
    seguro_vigente = models.BooleanField(default=True)
    calificacion = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)

    def __str__(self):
        return f"{self.usuario.nombre} - {self.tipo_vehiculo} ({self.numero_patente})"

# Modelo de Empresa con validaciones de seguridad
class Empresa(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, limit_choices_to={'tipo_usuario': 'empresa'})
    nombre_empresa = models.CharField(max_length=255)
    seguro = models.CharField(max_length=255)
    seguro_vigente = models.BooleanField(default=True)
    calificacion = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)

    def __str__(self):
        return f"{self.nombre_empresa} ({self.usuario.nombre})"
