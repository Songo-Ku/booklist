# models.py

class Book(models.Model):
	author = models.CharField()


# views.py

class BookListsView(ListView):
	model = Book

	def get_queryset(self, request, *args, **kwargs):
		"""
		/books?author=wicz&pub_year=2010
		"""
		qs = super().get_queryset(request, *args, **kwargs)
		if request.GET.get('author'):
			qs = qs.filter(author__icontains=request.GET.get('author'))
		if request.GET.get('pub_year'):
			qs = qs.filter(pub_year=request.GET.get('pub_year'))
		...
		return qs

import requests

class BookImportView(TemplateView):
	def post(self, request, *args, **kwargs):
		phrase = request.POST.get('phrase')
		if not phrase:
			return redirect()
		response = requests.get(f'htts://google.com....?q={phrase}', format='json')
		if response.status_code != 200:
			...
		data = response.json()
		books_to_be_created = []
		for item in data.get('items'):
			book = Book(
				author=item.get('author'),
				...
			)
			books_to_be_created.append(book)
		Book.objects.bulk_create(books_to_be_created)

		amount = len(books_to_be_created)
		return redirect(reverse('import_success', kwargs={}))


class BookModelViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['author', 'year', 'num_of_pages']


# serializers.py


# tests.py
