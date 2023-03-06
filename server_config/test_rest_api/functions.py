import re
from users.models import User
from users.serializers import UserStorageSerializer
# views > register


def save_user(data):

    user_id = data.get('user_id')
    password = data.get('user_password')
    email = data.get('user_email')
    last_name = data.get('user_last_name')
    first_name = data.get('user_first_name')

    regex = re.compile(r'[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+')

    if user_id == "" or password == "" or re.fullmatch(regex, email):
        return False

    user = User.objects.create_user(
        username=user_id, email=email, password=password)
    user.last_name = last_name
    user.first_name = first_name
    user.is_staff = True
    user.save()
    return True


def save_user_storage(username):
    checker = False
    init_data = {
        'username': username,
        'tier': 0,
        'max_storage_size': 1024 * 1024 * 64,
        'used_storage_size': 1024 * 1024 * 64
    }
    serializer = UserStorageSerializer(data=init_data)
    if serializer.is_valid():
        checker = True
        print('success save_user_storage')
        serializer.save()
    else:
        print("fail save_user_storage")
    return checker
