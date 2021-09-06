class BookCreateView(CreateView):
	model = Book
	fields = [
		'title', 'language_book', 'published_date',
		'isbn13_number', 'authors_name',
		'page_number', 'link_book_cover'
	]
	template_name = 'booklist/book_create_form.html'
	# success_url = reverse_lazy('booklist:index')

	def get_success_url(self):
		return reverse('booklist:index')