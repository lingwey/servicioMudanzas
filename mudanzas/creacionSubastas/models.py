from django.db import models
from django.utils import timezone
from registroUsuarios.models import Usuario
from django.db import models

class ImagenCarga(models.Model):
    subasta = models.ForeignKey("Subasta", on_delete=models.CASCADE, related_name="imagenes")
    imagen = models.ImageField(upload_to="cargas/")

#crea la subasta del lado del cliente
class Subasta(models.Model):
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="subastas_creadas")
    origen = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)
    fecha_envio = models.DateField()
    descripcion = models.TextField(blank=True)
    tiempo_limite = models.DateTimeField()
    finalizada = models.BooleanField(default=False)
    oferta_ganadora = models.ForeignKey("Oferta", null=True, blank=True, on_delete=models.SET_NULL, related_name="ganadora_de")
    destino_calle = models.CharField(max_length=100)
    destino_localidad = models.CharField(max_length=100)
    destino_provincia = models.CharField(max_length=100)
    precio_referencia = models.DecimalField(
    max_digits=10,
    decimal_places=2,
    default=10000,
    verbose_name="Precio máximo dispuesto a pagar",
    help_text="Este es el precio que el cliente está dispuesto a pagar como máximo."
    )
    fecha_creacion = models.DateTimeField(default=timezone.now, verbose_name="Fecha de creación")



    def tiempo_restante(self):
        return max(self.tiempo_limite - timezone.now(), timezone.timedelta(seconds=0))

    def get_oferta_minima(self):
        return self.ofertas.order_by("precio").first()  # oferta más baja

#controla los la parte de la subasta del lado de los ofertadoress (choferes/empresas)
class Oferta(models.Model):
    subasta = models.ForeignKey(Subasta, on_delete=models.CASCADE, related_name="ofertas")
    ofertante = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="ofertas_realizadas")
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_oferta = models.DateTimeField(auto_now_add=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)

#crea en la db los tikects 
class TicketSubasta(models.Model):
    subasta = models.OneToOneField(Subasta, on_delete=models.CASCADE)
    fecha_cierre = models.DateTimeField(auto_now_add=True)
    modo_cierre = models.CharField(max_length=50)  # "manual" o "automático"
    precio_final = models.DecimalField(max_digits=10, decimal_places=2)
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="tickets_emitidos")
    ganador = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name="tickets_recibidos")
