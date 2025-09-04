from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    description = models.TextField(blank=True, verbose_name="Descripción")
    color = models.CharField(max_length=7, default="#2e7d32", verbose_name="Color")
    
    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
    
    def __str__(self):
        return self.name

class Ticket(models.Model):
    STATUS_CHOICES = (
        ('new', 'Nuevo'),
        ('in_progress', 'En progreso'),
        ('resolved', 'Resuelto'),
        ('closed', 'Cerrado'),
    )
    
    PRIORITY_CHOICES = (
        ('low', 'Baja'),
        ('medium', 'Media'),
        ('high', 'Alta'),
        ('critical', 'Crítica'),
    )
    
    title = models.CharField(max_length=200, verbose_name="Título")
    description = models.TextField(verbose_name="Descripción")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Estado")
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium', verbose_name="Prioridad")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Categoría")
    created_by = models.ForeignKey(User, related_name='created_tickets', on_delete=models.CASCADE, verbose_name="Creado por")
    assigned_to = models.ForeignKey(User, related_name='assigned_tickets', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Asignado a")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última actualización")
    due_date = models.DateTimeField(null=True, blank=True, verbose_name="Fecha límite")
    
    class Meta:
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"

class Comment(models.Model):
    ticket = models.ForeignKey(Ticket, related_name='comments', on_delete=models.CASCADE, verbose_name="Ticket")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Autor")
    content = models.TextField(verbose_name="Contenido")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Fecha de creación")
    
    class Meta:
        verbose_name = "Comentario"
        verbose_name_plural = "Comentarios"
        ordering = ['created_at']
    
    def __str__(self):
        return f"Comentario de {self.author} en {self.ticket.title}"

class Attachment(models.Model):
    ticket = models.ForeignKey(Ticket, related_name='attachments', on_delete=models.CASCADE, verbose_name="Ticket")
    file = models.FileField(upload_to='ticket_attachments/%Y/%m/%d/', verbose_name="Archivo")
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Subido por")
    uploaded_at = models.DateTimeField(default=timezone.now, verbose_name="Fecha de subida")
    
    class Meta:
        verbose_name = "Adjunto"
        verbose_name_plural = "Adjuntos"
    
    def __str__(self):
        return f"Adjunto para {self.ticket.title}"

# Create your models here.
