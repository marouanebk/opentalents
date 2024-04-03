from scolar.models import User
User.objects.create_superuser('admin', 'admin@etablissement.dz', 'password')
