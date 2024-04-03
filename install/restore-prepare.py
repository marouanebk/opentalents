from django.contrib.contenttypes.models import ContentType
ContentType.objects.all().delete()
from django.contrib.auth.models import Group
Group.objects.all().delete()
