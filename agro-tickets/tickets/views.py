from rest_framework import viewsets, permissions
from .models import Category, Ticket, Comment, Attachment
from .serializers import CategorySerializer, TicketSerializer, CommentSerializer, AttachmentSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]  # Cambiado para desarrollo

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.AllowAny]  # Cambiado para desarrollo
    
    def perform_create(self, serializer):
        # Asigna el primer usuario disponible si no hay autenticación
        if self.request.user.is_authenticated:
            serializer.save(created_by=self.request.user)
        else:
            from django.contrib.auth.models import User
            first_user = User.objects.first()
            serializer.save(created_by=first_user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]  # Cambiado para desarrollo
    
    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(author=self.request.user)
        else:
            from django.contrib.auth.models import User
            first_user = User.objects.first()
            serializer.save(author=first_user)

class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    permission_classes = [permissions.AllowAny]  # Cambiado para desarrollo
    
    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(uploaded_by=self.request.user)
        else:
            from django.contrib.auth.models import User
            first_user = User.objects.first()
            serializer.save(uploaded_by=first_user)