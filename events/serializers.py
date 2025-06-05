from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework.authtoken.models import Token
from .models import Events, Attendee

User = get_user_model()

class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')   
        user = User(**validated_data)               
        user.set_password(password)                 
        user.save()                                 
        Token.objects.create(user=user)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(username=attrs['username'], password=attrs['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        token, created = Token.objects.get_or_create(user=user)
        return {'token': token.key}
    
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = ['id', 'event_name', 'location', 'start_time', 'end_time', 'max_capacity', 'is_active']
        
        def validate(self, data):
            if data['start_time'] >= data['end_time']:
                raise serializers.ValidationError("End time must be after start time")
            if data['max_capacity'] <= 0:
                raise serializers.ValidationError("Max capacity must be greater than zero")
            return data
    
class AttendeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendee
        fields = ['id', 'attentee_name', 'email_id', 'registered_at']
        
    def validate(self, data):
        event = self.context['event']
        
        if event.attendees.count() >= event.max_capacity:
            raise serializers.ValidationError("Event is fully booked")
        if Attendee.objects.filter(event=event, email_id=data['email_id']).exists():
            raise serializers.ValidationError("You have already registered for this event")
        return data
    
    def create(self, validated_data):
        event = self.context['event']
        return Attendee.objects.create(event=event, **validated_data)