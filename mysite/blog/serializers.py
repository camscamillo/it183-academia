# serializers.py
from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'likes', 'liked_by']
        read_only_fields = ['likes']  # 'likes' is read-only
