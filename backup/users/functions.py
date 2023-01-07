from .models import UserData
from .serializers import UserSerializer
def get_user_id(username):
    user_data = UserData.objects.get(id=username)
    serializer = UserSerializer(user_data, many=False)
    return serializer.data