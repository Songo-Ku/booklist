# #  moja źle dzialająca wersja paginacji, ale dobrze dzialajaca wersja filtrowania z BOOKlistFilter
# class BookFilterSearchListView(ListView):
# 	model = Book
# 	template_name = 'booklist/filter_search.html'
# 	paginate_by = 5
# 	form_class = BooklistFilter
# 	# queryset = Book.objects.all()
#
# 	def get_context_data(self, **kwargs):
# 		_request_copy = self.request.GET.copy()
# 		parameters = _request_copy.pop('page', True) and _request_copy.urlencode()
# 		context = super().get_context_data(**kwargs)
# 		context['filter'] = BooklistFilter(self.request.GET, queryset=self.get_queryset())
# 		context['parameters'] = parameters
# 		return context
# 	# tutaj taki pomysł na użycie 2 innych klas, 1 bedzie startowa, a druga juz z przekazanymi parametrami
# 	# obydwa maja miec paignacje
#
#
# # I pierwszy przyklad  nie dzialajacy
# # ---------------------------------------------
# # class PostListView(ListView):
# #     model = Post
# #
# # class ActivePostListView(PostListView):
# #     queryset = Post.objects.filter(active=True)
# #
# # class InactivePostListView(PostListView):
# #     queryset = Post.objects.filter(active=False)
#
#
# # class BookFilterView(FilterView):
# #     model = Book
# #     filterset_class = AvailFilter
# #     paginate_by = 5
# #
# #     def get_context_data(self, *args, **kwargs):
# #         _request_copy = self.request.GET.copy()
# #         parameters = _request_copy.pop('page', True) and _request_copy.urlencode()
# #         context = super().get_context_data(*args, **kwargs)
# #         context['parameters'] = parameters
# #         return context
#
#
# #---------------------------------------------------------
# # II pierwszy przyklad  nie dzialajacy
#
# # cos tutaj jest nie tak z queryset lub get_queryset
# # class FilteredListView(ListView):
# # 	filterset_class = None
# # 	template_name = 'booklist/filterset_book.html'
# #
# # 	def get_queryset(self):
# # 		queryset = super().get_queryset()
# # 		self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
# # 		return self.filterset.qs.distinct()
# #
# # 	def get_context_data(self, **kwargs):
# # 		context = super().get_context_data(**kwargs)
# # 		# Pass the filterset to the template - it provides the form.
# # 		context['filterset'] = self.filterset
# # 		return context
# #
# #
# # class BookFilterSet(django_filters.FilterSet):
# # 	def __init__(self, data, *args, **kwargs):
# # 		data = data.copy()
# # 		# data.setdefault('format', 'paperback')
# # 		# data.setdefault('order', '-added')
# # 		super().__init__(data, *args, **kwargs)
# #
# #
# # class BookListView(FilteredListView):
# #     # filterset_class = BookFilterset
# # 	filterset_class = BookFilterSet
#
#
# # III pierwszy przyklad  nie dzialajacy
# # ---------------------------------------------
# # drugi przyklad czemu to nie działa ?
#
# class FilteredListView(ListView):
# 	filterset_class = None
#
# 	def get_queryset(self):
# 		queryset = super().get_queryset()
# 		self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
# 		return self.filterset.qs.distinct()
#
# 	def get_context_data(self, ** kwargs):
# 		context = super().get_context_data( ** kwargs)
# 		context['filterset'] = self.filterset
# 		return context
#
#
# class BookFilterSet(django_filters.FilterSet):
# 	def __init__(self, data, * args, ** kwargs):
# 		data = data.copy()
# 		data.setdefault('format', 'paperback')
# 		data.setdefault('order', '-added')
# 		super().__init__(data, * args, ** kwargs)
#
#
# class BookListView(FilteredListView):
# 	filterset_class = BookFilterSet
# 	paginate_by = 5
#
#
# # ---------------------------------------------
# # IV tu z kolei nie zwraca mi form żadnych pól do wypełnienia?????
# class BookFilter(django_filters.FilterSet):
# 	title = django_filters.CharFilter(lookup_expr='iexact')
#
# 	class Meta:
# 		model = Book
# 		fields = ['published_date', 'authors_name', 'language_book', ]
#
#
# # class BookFilterSearchListView(ListView):
# # 	model = Book
# # 	template_name = 'booklist/filter_book_search.html'
# # 	paginate_by = 5
# 	# form_class = BookFilter
#
#
#
#
# # --------------------------------
# # to do osobnego url bez definiowania view tutaj w views
# # dla widoku FilterView
#
# # dlaczego jak filtr nie ma rezultatów to mi sypie that page contains no results
# # excpetion type emptypage
#
#
#
# class F(django_filters.FilterSet):
# 	#  co jest w tym złego ?
# 	title = django_filters.CharFilter(method='my_custom_filter')
# 	published_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
#
# 	class Meta:
# 		model = Book
#
# 		fields = {
# 			'title': ['icontains'],
# 			'authors_name': ['icontains'],
# 			'language_book': ['icontains'],
# 			'published_date': ['gte'],
# 			# 'published_date': ['gte', 'lte'],
# 		}
# 		# widgets = {'published_date': DateInput(), }
#
# 	def my_custom_filter(self, queryset, name, value):
# 		return queryset.filter(**{name: value, })
#
#
# class MojFilterWithPag(FilterView):
# 	filterset_class = F
# 	paginate_by = 5
# 	# jak to sie ma do uzycia innych metod, ktore robia zmiany dla queryset i jak to jest nadpisywane?
# 	# queryset = User.objects.all()
#
# 	def get_queryset(self):
# 		queryset = super().get_queryset()
# 		self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
# 		# ---------------------------------------------
#
# 		# co to robi tutaj
# 		# ---------------------------------------------
#
# 		return self.filterset.qs.distinct()
#
# 	# w html zmienna {{filterset}} pojawi sie tylko jesli context bedzie ja mal
# 	# def get_context_data(self, **kwargs):
# 	# 	context = super().get_context_data(**kwargs)
# 	# 	context['filterset'] = self.filterset
# 	# 	return context
#
# 	def get_paginate_by(self, queryset):
#
# 		# ---------------------------------------------
# 		# co tutaj zrobic zeby ta paignacja dostala odpowiednie dane do paginowania
# 		# ---------------------------------------------
#
# 		return super().get_paginate_by(queryset=self.filterset)
#
# 	# ---------------------------------------------
# 	#  moze da sie jakos uzyc paginate queryset
# 	# ---------------------------------------------
#
# 	# def paginate_queryset(self, queryset, page_size):
# 	# 	"""Paginate the queryset, if needed."""
# 	# 	paginator = self.get_paginator(
# 	# 		queryset, page_size, orphans=self.get_paginate_orphans(),
# 	# 		allow_empty_first_page=self.get_allow_empty())
# 	# 	page_kwarg = self.page_kwarg
# 	# 	page = self.kwargs.get(page_kwarg) or self.request.GET.get(page_kwarg) or 1
# 	# 	try:
# 	# 		page_number = int(page)
# 	# 	except ValueError:
# 	# 		if page == 'last':
# 	# 			page_number = paginator.num_pages
# 	# 		else:
# 	# 			raise Http404(_('Page is not “last”, nor can it be converted to an int.'))
# 	# 	try:
# 	# 		page = paginator.page(page_number)
# 	# 		return (paginator, page, page.object_list, page.has_other_pages())
# 	# 	except InvalidPage as e:
# 	# 		raise Http404(_('Invalid page (%(page_number)s): %(message)s') % {
# 	# 			'page_number': page_number,
# 	# 			'message': str(e)
# 	# 		})
# 	# ---------------------------------------------------------
#
#
# class BookFilterSearchPag(FormView):
# 	template_name = 'booklist/book_filter_search_pag.html'
# 	form_class = BookFilterSearchPagForm
# 	queryset = Book.objects.all()
# 	# success_url = reverse_lazy('booklist:index')
#
# 	# def form_valid(self, form):
# 	# 	print(form.cleaned_data)
# 	# 	return super().form_valid(form)
#
#
# class BookFilterSearchPagList(ListView):
# 	pass