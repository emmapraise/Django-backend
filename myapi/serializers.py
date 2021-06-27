from rest_framework import serializers

from myapi.models import User


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    password = serializers.CharField(style={'input_type': 'password'},
                                     write_only=True)

    class Meta:
        model = User
        exclude = ['is_active', 'is_staff', 'is_superuser',
                   'date_joined', 'last_login', 'groups', 'user_permissions']

    def create(self, validated_data):
        # Generates user_code and creates new User object.
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        phone = validated_data['phone']
        avatar = validated_data['avatar']
        user = User.objects.create_user(
            first_name=first_name,
            phone=phone,
            last_name=last_name,
            email=validated_data['email'],
            username=validated_data['email'],
            avatar= avatar,
            password=validated_data['password'],
        )
        return user
