# Cours avancé sur la personnalisation de l'administration Django

## 1. Personnalisation des modèles d'administration

### 1.1 Création de classes ModelAdmin avancées

Pour commencer, créons une classe ModelAdmin avancée :

```python
from django.contrib import admin
from django.utils.html import format_html
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'colored_status')
    list_filter = ('status', 'category')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at',)
    
    def colored_status(self, obj):
        colors = {
            'active': 'green',
            'inactive': 'red',
            'pending': 'orange'
        }
        return format_html(
            '<span style="color: {};">{}</span>',
            colors.get(obj.status, 'black'),
            obj.get_status_display()
        )
    colored_status.short_description = 'Status'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('category')
```

### 1.2 Personnalisation des formulaires d'administration

Utilisons une classe de formulaire personnalisée :

```python
from django import forms
from django.contrib import admin
from .models import Product

class ProductAdminForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}))
    
    class Meta:
        model = Product
        fields = '__all__'
    
    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 0:
            raise forms.ValidationError("Le prix ne peut pas être négatif.")
        return price

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    # ... autres configurations ...
```

## 2. Actions personnalisées

Ajoutons des actions personnalisées à notre modèle d'administration :

```python
from django.contrib import admin, messages
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    actions = ['make_active', 'make_inactive', 'update_stock']
    
    def make_active(self, request, queryset):
        updated = queryset.update(status='active')
        self.message_user(request, f'{updated} produits ont été activés.', messages.SUCCESS)
    make_active.short_description = "Marquer les produits sélectionnés comme actifs"
    
    def make_inactive(self, request, queryset):
        updated = queryset.update(status='inactive')
        self.message_user(request, f'{updated} produits ont été désactivés.', messages.SUCCESS)
    make_inactive.short_description = "Marquer les produits sélectionnés comme inactifs"
    
    @admin.action(description="Mettre à jour le stock")
    def update_stock(self, request, queryset):
        for product in queryset:
            product.update_stock()
        self.message_user(request, "Le stock a été mis à jour.", messages.SUCCESS)
```

## 3. Personnalisation de l'interface utilisateur

### 3.1 Modification du template d'administration

Créez un fichier `templates/admin/base_site.html` dans votre projet :

```html
{% extends "admin/base.html" %}
{% load static %}

{% block title %}{{ title }} | {{ site_title|default:_('Django site admin') }}{% endblock %}

{% block branding %}
<h1 id="site-name">
    <a href="{% url 'admin:index' %}">
        <img src="{% static 'img/logo.png' %}" alt="Logo" height="40" width="auto" style="margin-right: 10px;">
        {{ site_header|default:_('Django administration') }}
    </a>
</h1>
{% endblock %}

{% block nav-global %}{% endblock %}

{% block extrastyle %}
<style>
    #header { background: #4a4a4a; color: #fff; }
    .module h2, .module caption, .inline-group h2 { background: #5E5E5E; }
    div.breadcrumbs { background: #333; }
    a:link, a:visited { color: #447e9b; }
</style>
{% endblock %}
```

### 3.2 Ajout de JavaScript personnalisé

Créez un fichier `static/admin/js/custom_admin.js` :

```javascript
(function($) {
    $(document).ready(function() {
        // Exemple : Ajouter une confirmation avant de supprimer un élément
        $('input[name="action"]').on('change', function() {
            if ($(this).val() === 'delete_selected') {
                $('button[type="submit"]').on('click', function(e) {
                    if (!confirm('Êtes-vous sûr de vouloir supprimer ces éléments ?')) {
                        e.preventDefault();
                    }
                });
            }
        });
    });
})(django.jQuery);
```

Ajoutez ce script à votre `ModelAdmin` :

```python
class ProductAdmin(admin.ModelAdmin):
    class Media:
        js = ('admin/js/custom_admin.js',)
```

## 4. Personnalisation avancée des listes et des formulaires

### 4.1 Personnalisation des champs de liste

```python
from django.db.models import Sum, F
from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'total_value')
    list_editable = ('price', 'stock')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(total_value=F('price') * F('stock'))
    
    def total_value(self, obj):
        return obj.total_value
    total_value.admin_order_field = 'total_value'
    
    def get_list_display(self, request):
        list_display = list(super().get_list_display(request))
        if request.user.is_superuser:
            list_display.append('margin')
        return list_display
    
    def margin(self, obj):
        return obj.price - obj.cost
    margin.short_description = 'Marge'
```

### 4.2 Inlines personnalisés

```python
from django.contrib import admin
from .models import Product, ProductImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    max_num = 5
    
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.form.base_fields['image'].widget.attrs.update({'accept': 'image/*'})
        return formset

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
```

## 5. Personnalisation des permissions et du contrôle d'accès

```python
from django.contrib import admin
from django.contrib.auth import get_permission_codename
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        if obj is not None and obj.status == 'active':
            return request.user.has_perm('myapp.change_active_product')
        return super().has_change_permission(request, obj)
    
    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser and obj is not None:
            return self.readonly_fields + ('price',)
        return self.readonly_fields
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(category__in=request.user.allowed_categories.all())
```

## 6. Personnalisation du dashboard d'administration

Créez un fichier `admin.py` au niveau du projet :

```python
from django.contrib import admin
from django.contrib.admin.apps import AdminConfig

class CustomAdminSite(admin.AdminSite):
    site_header = "Mon Administration Personnalisée"
    site_title = "Portail d'Administration"
    index_title = "Bienvenue dans l'Administration"
    
    def get_app_list(self, request):
        app_list = super().get_app_list(request)
        app_list += [
            {
                "name": "Rapports",
                "app_label": "rapports",
                "models": [
                    {
                        "name": "Rapport de ventes",
                        "object_name": "sales_report",
                        "admin_url": "/admin/rapports/sales/",
                        "view_only": True,
                    },
                ],
            }
        ]
        return app_list

class CustomAdminConfig(AdminConfig):
    default_site = 'myproject.admin.CustomAdminSite'
```

Mettez à jour `INSTALLED_APPS` dans `settings.py` :

```python
INSTALLED_APPS = [
    'myproject.admin.CustomAdminConfig',
    # ... autres apps ...
]
```

## Conclusion

Ce cours avancé couvre de nombreux aspects de la personnalisation de l'administration Django. Il vous permet de créer une interface d'administration sur mesure, adaptée aux besoins spécifiques de votre projet. N'oubliez pas que la personnalisation doit toujours être équilibrée avec la maintenabilité et la lisibilité du code.