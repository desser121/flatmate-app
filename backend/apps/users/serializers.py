from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserPhoto, Preference

User = get_user_model()


class UserPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPhoto
        fields = ['id', 'image', 'order', 'is_primary', 'created_at']


class UserSerializer(serializers.ModelSerializer):
    photos = UserPhotoSerializer(many=True, read_only=True)
    age = serializers.IntegerField(read_only=True)
    profile_complete = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'phone', 'name', 'birth_date', 'gender', 'city', 'bio',
            'role_seeker', 'role_roommate', 'role_landlord',
            'photos', 'age', 'profile_complete',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'phone', 'created_at', 'updated_at']


class UserPublicSerializer(serializers.ModelSerializer):
    photos = UserPhotoSerializer(many=True, read_only=True)
    age = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'age', 'gender', 'city', 'bio', 'photos',
                  'role_seeker', 'role_roommate', 'role_landlord']


class RegisterSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20)
    password = serializers.CharField(min_length=6, write_only=True)
    name = serializers.CharField(max_length=100, required=False, default='')

    def validate_phone(self, value):
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError('Пользователь с таким телефоном уже существует')
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            phone=validated_data['phone'],
            password=validated_data['password'],
            name=validated_data.get('name', ''),
        )
        Preference.objects.create(user=user)
        return user


class PreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preference
        fields = [
            'city', 'district', 'budget_min', 'budget_max',
            'gender_pref', 'age_min', 'age_max',
            'smoking', 'pets', 'schedule', 'rental_period',
        ]
