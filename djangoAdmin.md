# Cours avancé détaillé sur la personnalisation de l'administration Django

## Introduction

Avant de plonger dans les détails de la personnalisation de l'administration Django, définissons d'abord le modèle que nous allons utiliser tout au long de ce cours. Cela nous donnera un contexte clair pour tous nos exemples.

## Définition du modèle

Nous allons travailler avec un modèle `Product` qui représente des produits dans une boutique en ligne. Voici la définition du modèle :

```python
from django.db import models
from django.core.validators import MinValueValidator

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class Product(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('pending', 'Pending'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    cost = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    stock = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def update_stock(self):
        # Logique pour mettre à jour le stock
        pass

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.product.name}"
```

Maintenant que nous avons défini notre modèle, passons à la personnalisation de l'administration Django.

## 1. Personnalisation des modèles d'administration

### 1.1 Création de classes ModelAdmin avancées

La classe `ModelAdmin` est le cœur de la personnalisation de l'interface d'administration pour un modèle spécifique. Voici une classe `ProductAdmin` avancée avec des explications détaillées :

```python
from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Category

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'colored_status', 'category')
    list_filter = ('status', 'category')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Informations de base', {
            'fields': ('name', 'description', 'category')
        }),
        ('Détails du prix', {
            'fields': ('price', 'cost'),
            'classes': ('collapse',)
        }),
        ('Inventaire', {
            'fields': ('stock', 'status')
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
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

# N'oubliez pas d'enregistrer aussi le modèle Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_count')
    search_fields = ('name', 'description')

    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Nombre de produits'
```

Explications :

- `list_display` : Définit les champs à afficher dans la liste des produits.
- `list_filter` : Ajoute des filtres dans la barre latérale pour filtrer les produits.
- `search_fields` : Permet de rechercher des produits par nom ou description.
- `readonly_fields` : Empêche la modification de certains champs.
- `fieldsets` : Organise les champs dans le formulaire d'édition en sections.
- `colored_status` : Méthode personnalisée pour afficher le statut avec une couleur.
- `get_queryset` : Optimise les requêtes en utilisant `select_related`.

### 1.2 Personnalisation des formulaires d'administration

Pour un contrôle plus fin sur le formulaire d'édition, nous pouvons créer une classe de formulaire personnalisée :

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

    def clean(self):
        cleaned_data = super().clean()
        price = cleaned_data.get('price')
        cost = cleaned_data.get('cost')
        if price and cost and price < cost:
            raise forms.ValidationError("Le prix de vente ne peut pas être inférieur au coût.")
        return cleaned_data

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    # ... autres configurations ...
```

Explications :

- Nous personnalisons le widget du champ `description` pour qu'il utilise un `Textarea` plus grand.
- La méthode `clean_price` effectue une validation spécifique pour le champ `price`.
- La méthode `clean` effectue une validation au niveau du formulaire, comparant le prix et le coût.

## 2. Actions personnalisées

Les actions personnalisées permettent d'effectuer des opérations sur plusieurs objets à la fois :

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

Explications :

- Chaque action est une méthode de la classe `ModelAdmin`.
- `make_active` et `make_inactive` utilisent `queryset.update()` pour modifier efficacement plusieurs objets.
- `update_stock` appelle une méthode sur chaque objet individuellement.
- `self.message_user()` affiche un message à l'utilisateur après l'action.
- Le décorateur `@admin.action` est une alternative à la définition manuelle de `short_description`.

## 3. Personnalisation de l'interface utilisateur

### 3.1 Modification du template d'administration

Pour personnaliser l'apparence globale de l'administration, créez un fichier `templates/admin/base_site.html` :

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

Explications :

- Ce template étend le template de base de l'administration Django.
- Nous ajoutons un logo personnalisé dans l'en-tête.
- Des styles CSS personnalisés sont ajoutés pour modifier les couleurs.

### 3.2 Ajout de JavaScript personnalisé

Pour ajouter des fonctionnalités JavaScript, créez un fichier `static/admin/js/custom_admin.js` :

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

        // Exemple : Masquer le champ 'cost' pour les non-superutilisateurs
        if (!$('body').hasClass('superuser')) {
            $('.field-cost').hide();
        }
    });
})(django.jQuery);
```

Ajoutez ce script à votre `ModelAdmin` :

```python
class ProductAdmin(admin.ModelAdmin):
    class Media:
        js = ('admin/js/custom_admin.js',)
```

Explications :

- Le script ajoute une confirmation avant la suppression d'éléments.
- Il cache également le champ 'cost' pour les utilisateurs qui ne sont pas superutilisateurs.
- La classe `Media` dans `ModelAdmin` permet d'inclure des fichiers JS et CSS spécifiques.

## 4. Personnalisation avancée des listes et des formulaires

### 4.1 Personnalisation des champs de liste

```python
from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'total_value', 'margin', 'margin_percentage')
    list_editable = ('price', 'stock')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            total_value=ExpressionWrapper(F('price') * F('stock'), output_field=DecimalField()),
            margin=ExpressionWrapper(F('price') - F('cost'), output_field=DecimalField()),
            margin_percentage=ExpressionWrapper(
                (F('price') - F('cost')) * 100 / F('price'),
                output_field=DecimalField()
            )
        )
    
    def total_value(self, obj):
        return obj.total_value
    total_value.admin_order_field = 'total_value'
    
    def margin(self, obj):
        return obj.margin
    margin.admin_order_field = 'margin'
    
    def margin_percentage(self, obj):
        return f"{obj.margin_percentage:.2f}%"
    margin_percentage.admin_order_field = 'margin_percentage'
    
    def get_list_display(self, request):
        list_display = list(super().get_list_display(request))
        if not request.user.is_superuser:
            list_display.remove('margin')
            list_display.remove('margin_percentage')
        return list_display
```

Explications :

- Nous utilisons `annotate` dans `get_queryset` pour ajouter des champs calculés à notre queryset.
- Les méthodes `total_value`, `margin`, et `margin_percentage` affichent ces valeurs calculées.
- `get_list_display` personnalise les champs affichés en fonction du type d'utilisateur.

### 4.2 Inlines personnalisés

Les inlines permettent d'éditer des modèles liés directement dans le formulaire du modèle parent :

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

    def get_inline_instances(self, request, obj=None):
        if not obj:  # Pas d'inlines sur la page d'ajout
            return []
        return super().get_inline_instances(request, obj)
```

Explications :

- `ProductImageInline` permet d'ajouter et d'éditer des images directement dans le formulaire du produit.
- `extra = 1` ajoute un formulaire vide pour une nouvelle image.
- `max_num = 5` limite le nombre d'images à 5.
- `get_formset` personnalise le widget du champ image pour n'accepter que des