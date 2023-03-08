from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('date_time_start', 'date_time_end', 'description', 'category_id', 'reservation', 'on_main')