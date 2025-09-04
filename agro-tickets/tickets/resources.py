from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import Category, Ticket, Comment, Attachment
from django.contrib.auth.models import User

class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category
        import_id_fields = ['id']
        fields = ('id', 'name', 'description', 'color')
        export_order = fields

class UserResource(resources.ModelResource):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')
        export_order = fields

class TicketResource(resources.ModelResource):
    created_by = fields.Field(
        column_name='created_by',
        attribute='created_by',
        widget=ForeignKeyWidget(User, 'username')
    )
    
    assigned_to = fields.Field(
        column_name='assigned_to',
        attribute='assigned_to',
        widget=ForeignKeyWidget(User, 'username')
    )
    
    category = fields.Field(
        column_name='category',
        attribute='category',
        widget=ForeignKeyWidget(Category, 'name')
    )
    
    class Meta:
        model = Ticket
        import_id_fields = ['id']
        fields = ('id', 'title', 'description', 'status', 'priority', 'category', 
                 'created_by', 'assigned_to', 'created_at', 'updated_at', 'due_date')
        export_order = fields
    
    def before_import_row(self, row, **kwargs):
        # Convertir fechas string a objetos datetime si es necesario
        if 'created_at' in row and row['created_at']:
            from django.utils.dateparse import parse_datetime
            row['created_at'] = parse_datetime(row['created_at'])
        
        if 'due_date' in row and row['due_date']:
            from django.utils.dateparse import parse_datetime
            row['due_date'] = parse_datetime(row['due_date'])

class CommentResource(resources.ModelResource):
    ticket = fields.Field(
        column_name='ticket',
        attribute='ticket',
        widget=ForeignKeyWidget(Ticket, 'id')
    )
    
    author = fields.Field(
        column_name='author',
        attribute='author',
        widget=ForeignKeyWidget(User, 'username')
    )
    
    class Meta:
        model = Comment
        fields = ('id', 'ticket', 'author', 'content', 'created_at')
        export_order = fields

class AttachmentResource(resources.ModelResource):
    ticket = fields.Field(
        column_name='ticket',
        attribute='ticket',
        widget=ForeignKeyWidget(Ticket, 'id')
    )
    
    uploaded_by = fields.Field(
        column_name='uploaded_by',
        attribute='uploaded_by',
        widget=ForeignKeyWidget(User, 'username')
    )
    
    class Meta:
        model = Attachment
        fields = ('id', 'ticket', 'file', 'uploaded_by', 'uploaded_at')
        export_order = fields