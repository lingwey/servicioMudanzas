from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CrearSubastaForm, OfertaForm, ImagenCargaFormSet
from .models import Subasta, Oferta, ImagenCarga, TicketSubasta
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden, HttpResponse
from reportlab.pdfgen import canvas
from io import BytesIO
from django.template.loader import render_to_string
from django.http import JsonResponse

@login_required
def crear_subasta(request):
    if request.user.tipo_usuario != "cliente":
        return redirect("home")

    if request.method == "POST":
        form = CrearSubastaForm(request.POST)
        formset = ImagenCargaFormSet(request.POST, request.FILES, queryset=ImagenCarga.objects.none())
        if form.is_valid() and formset.is_valid():
            subasta = form.save(commit=False)
            subasta.cliente = request.user
            subasta.save()

            for f in formset:
                if f.cleaned_data:
                    imagen = f.save(commit=False)
                    imagen.subasta = subasta
                    imagen.save()

            return redirect("creacionSubastas:detalle_subasta", subasta_id=subasta.id)
    else:
        form = CrearSubastaForm()
        formset = ImagenCargaFormSet(queryset=ImagenCarga.objects.none())

    return render(request, "creacionSubastas/crear_subasta.html", {
        "form": form,
        "formset": formset
    })
    
@login_required
def detalle_subasta(request, subasta_id):
    subasta = get_object_or_404(Subasta, id=subasta_id)
    ofertas = subasta.ofertas.order_by("precio")

    # Finalizar subasta (solo cliente)
    if request.method == "POST" and "finalizar_manual" in request.POST:
        if request.user.tipo_usuario == "cliente":
            mejor_oferta = subasta.get_oferta_minima()
            if mejor_oferta:
                subasta.oferta_ganadora = mejor_oferta
                subasta.finalizada = True
                subasta.save()

                TicketSubasta.objects.create(
                    subasta=subasta,
                    modo_cierre="manual",
                    precio_final=subasta.oferta_ganadora.precio,
                    cliente=subasta.cliente,
                    ganador=subasta.oferta_ganadora.ofertante
                )
            return redirect("creacionSubastas:detalle_subasta", subasta_id=subasta.id)

    # Enviar oferta (solo chofer/empresa)
    if request.method == "POST" and "enviar_oferta" in request.POST:
        if request.user.tipo_usuario not in ["chofer_particular", "empresa"]:
            return HttpResponse("No autorizado para ofertar", status=403)

        form = OfertaForm(request.POST)
        if form.is_valid():
            nueva_oferta = form.save(commit=False)
            nueva_oferta.ofertante = request.user
            nueva_oferta.subasta = subasta

            if nueva_oferta.precio >= subasta.precio_referencia:
                form.add_error("precio", "Tu oferta debe ser menor al precio máximo dispuesto a pagar por el cliente.")
            else:
                nueva_oferta.save()
                return redirect("creacionSubastas:detalle_subasta", subasta_id=subasta.id)
    else:
        # Preparar formulario si es chofer/empresa
        if request.user.tipo_usuario in ["chofer_particular", "empresa"]:
            form = OfertaForm()
        else:
            form = None

    return render(request, "creacionSubastas/detalle_subasta.html", {
        "subasta": subasta,
        "ofertas": ofertas,
        "form": form,
    })
    
@login_required
def ofertas_subasta_ajax(request, subasta_id):
    subasta = get_object_or_404(Subasta, id=subasta_id)
    ofertas = subasta.ofertas.order_by("precio")
    html = render_to_string("creacionSubastas/partials/_ofertas.html", {"ofertas": ofertas})
    return JsonResponse({"html": html})
    
@login_required
def ofertar_en_subasta(request, subasta_id):
    subasta = get_object_or_404(Subasta, id=subasta_id)

    if request.user.tipo_usuario not in ["chofer_particular", "empresa"]:
        return redirect("home")

    if subasta.finalizada:
        messages.error(request, "La subasta ya finalizó.")
        return redirect("creacionSubastas:detalle_subasta", subasta_id=subasta.id)

    # Verificamos si ya ofertó
    ya_oferto = subasta.ofertas.filter(ofertante=request.user).exists()
    if ya_oferto:
        messages.warning(request, "Ya has ofertado en esta subasta.")
        return redirect("creacionSubastas:detalle_subasta", subasta_id=subasta.id)

    if request.method == "POST":
        form = OfertaForm(request.POST)
        if form.is_valid():
            oferta = form.save(commit=False)
            oferta.subasta = subasta
            oferta.ofertante = request.user

            # Validación: debe ser menor al precio de referencia
            if oferta.precio >= subasta.precio_referencia:
                form.add_error("precio", "Tu oferta debe ser menor al precio máximo dispuesto a pagar por el cliente.")
            else:
                oferta.save()
                messages.success(request, "Oferta enviada con éxito.")
                return redirect("creacionSubastas:detalle_subasta", subasta_id=subasta.id)
    else:
        form = OfertaForm()

    return render(request, "creacionSubastas/ofertar.html", {
        "subasta": subasta,
        "form": form,
    })
    
@login_required
def ticket_subasta(request, subasta_id):
    subasta = get_object_or_404(Subasta, id=subasta_id)
    
    # Solo el cliente o el ganador pueden ver el ticket
    es_cliente = subasta.cliente == request.user
    es_ganador = subasta.oferta_ganadora and subasta.oferta_ganadora.ofertante == request.user

    if not (es_cliente or es_ganador):
        return HttpResponseForbidden("No tenés permiso para ver este ticket.")

    return render(request, "creacionSubastas/ticket_subasta.html", {
        "subasta": subasta,
        "cliente": subasta.cliente,
        "ganador": subasta.oferta_ganadora.ofertante if subasta.oferta_ganadora else None,
        "oferta": subasta.oferta_ganadora,
    })

@login_required
def historial_tickets(request):
    if request.user.tipo_usuario == "cliente":
        tickets = TicketSubasta.objects.filter(cliente=request.user)
    elif request.user.tipo_usuario in ["chofer_particular", "empresa"]:
        tickets = TicketSubasta.objects.filter(ganador=request.user)
    else:
        tickets = TicketSubasta.objects.none()

    return render(request, "creacionSubastas/historial_tickets.html", {
        "tickets": tickets
    })
    
@login_required
def descargar_ticket_pdf(request, subasta_id):
    subasta = get_object_or_404(Subasta, id=subasta_id)

    es_cliente = subasta.cliente == request.user
    es_ganador = subasta.oferta_ganadora and subasta.oferta_ganadora.ofertante == request.user

    if not (es_cliente or es_ganador):
        return HttpResponse("No autorizado", status=403)

    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    # Datos del ticket
    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, 800, "Ticket de cierre de subasta")

    p.setFont("Helvetica", 11)
    p.drawString(100, 770, f"ID Subasta: {subasta.id}")
    p.drawString(100, 750, f"Origen: {subasta.origen}")
    p.drawString(100, 730, f"Destino: {subasta.destino_calle}, {subasta.destino_localidad}, {subasta.destino_provincia}")
    p.drawString(100, 710, f"Fecha de envío: {subasta.fecha_envio}")
    p.drawString(100, 690, f"Descripción: {subasta.descripcion}")

    # Cliente
    p.drawString(100, 660, f"Cliente: {subasta.cliente.nombre} - {subasta.cliente.email}")

    # Ganador
    if subasta.oferta_ganadora:
        p.drawString(100, 640, f"Ganador: {subasta.oferta_ganadora.ofertante.nombre}")
        p.drawString(100, 620, f"Tipo: {subasta.oferta_ganadora.ofertante.get_tipo_usuario_display()}")
        p.drawString(100, 600, f"Email: {subasta.oferta_ganadora.ofertante.email}")
        p.drawString(100, 580, f"Precio aceptado: ${subasta.oferta_ganadora.precio}")
    else:
        p.drawString(100, 640, "Ganador: no disponible")

    p.drawString(100, 560, f"Fecha de cierre: {subasta.tiempo_limite}")
    p.drawString(100, 540, f"Subasta finalizada: {'Sí' if subasta.finalizada else 'No'}")

    p.showPage()
    p.save()

    buffer.seek(0)
    return HttpResponse(buffer, content_type="application/pdf")

@login_required
def listar_subastas_vigentes(request):
    if request.user.tipo_usuario not in ["chofer_particular", "empresa"]:
        return redirect("home")

    subastas = Subasta.objects.filter(finalizada=False).order_by("tiempo_limite")

    return render(request, "creacionSubastas/listado_subastas.html", {
        "subastas": subastas
    })