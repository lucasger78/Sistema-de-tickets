from django.contrib import admin
from django.utils import timezone
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin
from import_export.formats import base_formats
from django.http import HttpResponse
from .models import Category, Ticket, Comment, Attachment
from .resources import CategoryResource, TicketResource, CommentResource, AttachmentResource

# Eliminar registros previos para evitar el error "AlreadyRegistered"
if Ticket in admin.site._registry:
    admin.site.unregister(Ticket)
if Category in admin.site._registry:
    admin.site.unregister(Category)
if Comment in admin.site._registry:
    admin.site.unregister(Comment)
if Attachment in admin.site._registry:
    admin.site.unregister(Attachment)

@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    resource_class = CategoryResource
    list_display = ('name', 'description', 'color')
    search_fields = ('name', 'description')
    list_editable = ('color',)

@admin.register(Ticket)
class TicketAdmin(ImportExportActionModelAdmin):
    resource_class = TicketResource
    list_display = ('title', 'status', 'priority', 'category', 'created_by', 'created_at')
    list_filter = ('status', 'priority', 'category', 'created_at')
    search_fields = ('title', 'description')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')
    
    def get_export_filename(self, request, queryset, file_format):
        """Personalizar el nombre del archivo de exportación"""
        return f"tickets_export_{timezone.now().strftime('%Y-%m-%d_%H-%M')}.{file_format.get_extension()}"

@admin.register(Comment)
class CommentAdmin(ImportExportModelAdmin):
    resource_class = CommentResource
    list_display = ('ticket', 'author', 'created_at')
    list_filter = ('created_at', 'author')
    search_fields = ('content', 'ticket__title')
    readonly_fields = ('created_at',)

@admin.register(Attachment)
class AttachmentAdmin(ImportExportModelAdmin):
    resource_class = AttachmentResource
    list_display = ('ticket', 'uploaded_by', 'uploaded_at')
    list_filter = ('uploaded_at', 'uploaded_by')
    readonly_fields = ('uploaded_at',)

# Configuración adicional para el admin site
admin.site.site_header = "Sistema de Tickets Agropecuarios - Administración"
admin.site.site_title = "Admin Tickets Agro"
admin.site.index_title = "Bienvenido al sistema de administración"

def export_selected_tickets(modeladmin, request, queryset):
    """Exportar tickets seleccionados"""
    resource = TicketResource()
    dataset = resource.export(queryset)
    
    # Usar XLSX
    format = base_formats.XLSX()
    export_data = format.export_data(dataset)
    
    response = HttpResponse(
        export_data,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="tickets_seleccionados_{timezone.now().strftime("%Y-%m-%d")}.xlsx"'
    return response

export_selected_tickets.short_description = "Exportar tickets seleccionados (Excel)"

# Registrar la acción
TicketAdmin.actions = [export_selected_tickets]