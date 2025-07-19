from django import forms
from .models import Subasta, Oferta
from django.forms import modelformset_factory
from .models import ImagenCarga
from localflavor.ar.forms import ARProvinceSelect

ImagenCargaFormSet = modelformset_factory(
    ImagenCarga,
    fields=("imagen",),
    extra=5,
    max_num=5,
    widgets={"imagen": forms.ClearableFileInput(attrs={"multiple": False})}
)


class CrearSubastaForm(forms.ModelForm):
    destino_provincia = forms.CharField(widget=ARProvinceSelect(), label="Provincia de destino")
    class Meta:
        model = Subasta
        fields = ['origen', 'destino_calle', 'destino_localidad', 'destino_provincia', 'fecha_envio', 'descripcion', 'tiempo_limite', 'precio_referencia']
        widgets = {
            
            'fecha_envio': forms.DateInput(attrs={'type': 'date'}),
            'tiempo_limite': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }

#controla las ofertas que hacen los choferes/empresas
class OfertaForm(forms.ModelForm):
    class Meta:
        model = Oferta
        fields = ["precio"]
        widgets = {
            "precio": forms.NumberInput(attrs={"placeholder": "Precio ofrecido", "min": "1"})
        }

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio <= 0:
            raise forms.ValidationError("El precio debe ser mayor a cero.")
        return precio