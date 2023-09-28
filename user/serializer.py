from rest_framework import serializers
from .models import User, Address


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'password']

    def create(self, validate_data):
        password = validate_data.pop("password", None)
        instance = self.Meta.model(**validate_data)
        if password is not None:
            instance.set_password(password)
        else:
            raise ("You should set a password!" )
        instance.save()
        return instance
    

class UserVerifySerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=4)


class LoginOTPSerializer(serializers.Serializer):
    otp=serializers.IntegerField(required=True, allow_null=False)

    def validate(self, data):
        otp=data.get("otp")
        request=self.context.get("request")
        if not otp==request.session.get("otp"):
            raise serializers.ValidationError
        if not User.objects.filter(phone=request.session.get("phone")).exists():
            raise serializers.ValidationError

        return data


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields =("province", "city", "street", "detail", "postal_code")

