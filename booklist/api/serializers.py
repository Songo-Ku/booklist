from rest_framework import serializers
from ..models import Book


class BookModelSerializer(serializers.ModelSerializer):
	class Meta:
		model = Book
		fields = [
			'pk',
			'title',
			'authors_name',
			'published_date',
			'language_book',
			'isbn13_number',
			'page_number',
			'link_book_cover',
			'created',
		]
		read_only_fields = ['pk', 'created']


class BookCreateUpdateModelSerializer(serializers.ModelSerializer):
	class Meta:
		model = Book
		fields = [
			'title',
			'authors_name',
			'published_date',
			'language_book',
			'isbn13_number',
			'page_number',
			'link_book_cover',
			'created',
		]
		read_only_fields = ['pk', 'created']



