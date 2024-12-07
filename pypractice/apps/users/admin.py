from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as UserAdmin_
from .models import TipoUsuario, TipoPersona, ClientStatus, Empresa, PlanEmpresa

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'get_full_name', 'email', 'user_type', 'person_type', 'status', 'company', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_active', 'user_type', 'status', 'company')
    ordering = ('-id',)


@admin.register(TipoUsuario)
class TipoUsuarioAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(TipoPersona)
class TipoPersonaAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(ClientStatus)
class ClientStatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'class_css', 'created')
    search_fields = ('name',)
    list_filter = ('created',)


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'estado', 'pais', 'telefono', 'is_active', 'fecha_contratacion', 'fecha_suspension')
    search_fields = ('nombre', 'email', 'telefono', 'rfc')
    list_filter = ('estado', 'is_active', 'pais', 'fecha_contratacion')
    ordering = ('-created_at',)


@admin.register(PlanEmpresa)
class PlanEmpresaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'precio_sin_iva', 'created', 'mostrar')
    search_fields = ('nombre',)
    list_filter = ('mostrar',)
    ordering = ('-created',)
