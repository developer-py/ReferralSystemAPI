from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    referral_code = serializers.CharField(required=False)  # Make referral_code optional

    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'password', 'referral_code']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        referral_code = data.get('referral_code')
        if referral_code:
            try:
                referred_by_user = CustomUser.objects.get(referral_code=referral_code)
            except CustomUser.DoesNotExist:
                raise serializers.ValidationError({"referral_code":"Invalid referral code"})
        return data

    def create(self, validated_data):
        referral_code = validated_data.pop('referral_code', None)
        user = CustomUser.objects.create_user(**validated_data)
        
        if referral_code:
            referred_by_user = CustomUser.objects.get(referral_code=referral_code)
            user.referred_by = referred_by_user
            user.save()
        return user




class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'referral_code', 'date_joined']
        
        
class UserLoginSerialiazer(serializers.ModelSerializer):
    email = serializers.EmailField()
    class Meta:
        model = CustomUser
        fields = ['email', 'password']