from users.models import User
from users.serializers import UserStorageSerializer
#views > register
def save_user(data):
    user = User.objects.create_user(data.get('user_id'),data.get('user_email'),data.get('user_password'))
    user.last_name = data.get('user_last_name')
    user.first_name = data.get('user_first_name')
    user.save()
    return 0

def save_user_storage(username):
    checker = False
    init_data = {
        'username':username,
        'tier':0,
        'max_storage_size': 1024 * 1024 * 1024,
        'used_storage_size' : 1024 * 1024 * 1024
    }
    serializer = UserStorageSerializer(data=init_data)
    if serializer.is_valid():
        checker = True
        print('success save_user_storage')
        serializer.save()
    else:
        print("fail save_user_storage")
    return checker


