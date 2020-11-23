from rest_framework import serializers


def not_slash_in_name(value):
    if '/' in value:
        raise serializers.ValidationError('Meno nesmie obsahovat "/"!')


class GallerySerializerPostRead(serializers.Serializer):
    name = serializers.CharField(required=True, validators=[not_slash_in_name])


