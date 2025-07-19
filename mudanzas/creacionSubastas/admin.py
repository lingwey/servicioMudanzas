from django.contrib import admin
from .models import Subasta, Oferta, TicketSubasta

@admin.register(Subasta)
class SubastaAdmin(admin.ModelAdmin):
    list_display = ("id", "cliente", "origen", "destino_provincia", "fecha_envio", "tiempo_limite", "precio_referencia", "finalizada")
    list_filter = ("finalizada", "destino_provincia", "fecha_envio")
    search_fields = ("cliente__email", "origen", "destino_localidad", "destino_provincia")
    ordering = ("-fecha_envio",)

@admin.register(Oferta)
class OfertaAdmin(admin.ModelAdmin):
    list_display = ("id", "subasta", "ofertante", "precio", "fecha_creacion")
    list_filter = ("subasta", "ofertante")
    search_fields = ("ofertante__email",)

@admin.register(TicketSubasta)
class TicketSubastaAdmin(admin.ModelAdmin):
    list_display = ("id", "subasta", "cliente", "ganador", "precio_final", "modo_cierre", "fecha_cierre")
    list_filter = ("modo_cierre", "fecha_cierre")
    search_fields = ("cliente__email", "ganador__email")

