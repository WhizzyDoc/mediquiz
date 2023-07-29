from rest_framework import serializers
from ..models import Department, Course, Topic, Item

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'title', 'slug']

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['order', 'title', 'description']

class CourseSerializer(serializers.ModelSerializer):
    topics = TopicSerializer(many=True, read_only=True)
    class Meta:
        model = Course
        fields = ['id', 'department', 'title', 'slug', 'overview', 'created', 'owner', 'topics']

class ItemRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        return value.render()

class ContentSerializer(serializers.ModelSerializer):
    item = ItemRelatedField(read_only=True)
    class Meta:
        model = Item
        fields = ['order', 'item']

class TopicWithContentSerializer(serializers.ModelSerializer):
    contents = ContentSerializer(many=True)
    class Meta:
        model = Topic
        fields = ['order', 'title', 'description', 'contents']

class CourseWithContentSerializer(serializers.ModelSerializer):
    topics = TopicWithContentSerializer(many=True)
    class Meta:
        model = Course
        fields = ['id', 'department', 'title', 'slug', 'overview', 'created', 'owner', 'topics']
