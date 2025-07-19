from django.urls import path
from .views import crear_subasta, detalle_subasta, ofertar_en_subasta, ticket_subasta, historial_tickets, descargar_ticket_pdf, listar_subastas_vigentes, ofertas_subasta_ajax

app_name= "creacionSubasta"

urlpatterns = [
    path("detalle/<int:subasta_id>/", detalle_subasta, name="detalle_subasta"),
    path("crear/", crear_subasta, name="crear_subasta"),
    path("ofertar/<int:subasta_id>/", ofertar_en_subasta, name="ofertar_en_subasta"),
    path("ticket/<int:subasta_id>/", ticket_subasta, name="ticket_subasta"),
    path("historial/", historial_tickets, name="historial_tickets"),
    path("ticket/<int:subasta_id>/descargar/", descargar_ticket_pdf, name="descargar_ticket_pdf"),
    path("subastas/", listar_subastas_vigentes, name="listar_subastas_vigentes"),
   path("ofertas-ajax/<int:subasta_id>/", ofertas_subasta_ajax, name="ofertas_subasta_ajax"),




]
