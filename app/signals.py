from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.db import connection
from .models import center

@receiver(post_delete, sender=center)
def delete_schema_with_tenant(sender, instance, **kwargs):
    schema_name = instance.schema_name
    if schema_name not in ['public', 'template1']:  # حماية احتياطية
        with connection.cursor() as cursor:
            cursor.execute(f'DROP SCHEMA IF EXISTS "{schema_name}" CASCADE')
