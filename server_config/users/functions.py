from .models import UserData
from .serializers import UserStorageSerializer
def get_user_id(username):
    user_data = UserData.objects.get(id=username)
    serializer = UserStorageSerializer(user_data, many=False)
    return serializer.data