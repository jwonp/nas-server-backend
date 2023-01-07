from django.contrib.auth import authenticate
u = authenticate(username="prodge", password="1234")
print(u.is_staff)
print(u.is_superuser)
print(u.is_active)