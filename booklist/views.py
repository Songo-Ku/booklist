from functools import reduce

from django.shortcuts import (render, get_object_or_404, redirect,)
from django.urls import reverse, reverse_lazy
# from django.views import generic
from django.views.generic import (
	TemplateView,
	DetailView,
	CreateView,
	ListView,
	DeleteView,
	UpdateView,
	FormView,
)
import django_filters
from django import forms
from django.db.models import Q
import operator

# ---------------------------------------
from .models import Book
from .forms import BookModelForm, DateInput, BookFilterSearchPagForm, InputForm
from .filters import BooklistFilter
from .filters import AvailFilter
# AvailFilter

# ---------------------------------------
from requests import get, exceptions
from json import loads
from .api_google_book_utils import prepare_list_of_json_to_bulk_create, url_builder
from .api_google_book_utils import BooksImporterApi
from django_filters.views import FilterView

# from datetime import date
# import datetime


# ------------------------

# from django.contrib.auth.decorators import login_required
# from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect


class IndexView(ListView):
	template_name = 'booklist/index.html'
	context_object_name = 'booklist'
	paginate_by = 5
	model = Book

	def get_queryset(self):
		return Book.objects.all().order_by('-id')


#  moja źle dzialająca wersja paginacji, ale dobrze dzialajaca wersja filtrowania z BOOKlistFilter
class BookFilterSearchListView(ListView):
	model = Book
	template_name = 'booklist/filter_search.html'
	paginate_by = 5
	form_class = BooklistFilter
	# queryset = Book.objects.all()

	def get_context_data(self, **kwargs):
		_request_copy = self.request.GET.copy()
		parameters = _request_copy.pop('page', True) and _request_copy.urlencode()
		context = super().get_context_data(**kwargs)
		context['filter'] = BooklistFilter(self.request.GET, queryset=self.get_queryset())
		context['parameters'] = parameters
		return context
	# tutaj taki pomysł na użycie 2 innych klas, 1 bedzie startowa, a druga juz z przekazanymi parametrami
	# obydwa maja miec paignacje


# I pierwszy przyklad  nie dzialajacy
# ---------------------------------------------
# class PostListView(ListView):
#     model = Post
#
# class ActivePostListView(PostListView):
#     queryset = Post.objects.filter(active=True)
#
# class InactivePostListView(PostListView):
#     queryset = Post.objects.filter(active=False)


# class BookFilterView(FilterView):
#     model = Book
#     filterset_class = AvailFilter
#     paginate_by = 5
#
#     def get_context_data(self, *args, **kwargs):
#         _request_copy = self.request.GET.copy()
#         parameters = _request_copy.pop('page', True) and _request_copy.urlencode()
#         context = super().get_context_data(*args, **kwargs)
#         context['parameters'] = parameters
#         return context


#---------------------------------------------------------
# II pierwszy przyklad  nie dzialajacy

# cos tutaj jest nie tak z queryset lub get_queryset
# class FilteredListView(ListView):
# 	filterset_class = None
# 	template_name = 'booklist/filterset_book.html'
#
# 	def get_queryset(self):
# 		queryset = super().get_queryset()
# 		self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
# 		return self.filterset.qs.distinct()
#
# 	def get_context_data(self, **kwargs):
# 		context = super().get_context_data(**kwargs)
# 		# Pass the filterset to the template - it provides the form.
# 		context['filterset'] = self.filterset
# 		return context
#
#
# class BookFilterSet(django_filters.FilterSet):
# 	def __init__(self, data, *args, **kwargs):
# 		data = data.copy()
# 		# data.setdefault('format', 'paperback')
# 		# data.setdefault('order', '-added')
# 		super().__init__(data, *args, **kwargs)
#
#
# class BookListView(FilteredListView):
#     # filterset_class = BookFilterset
# 	filterset_class = BookFilterSet


# III pierwszy przyklad  nie dzialajacy
# ---------------------------------------------
# drugi przyklad czemu to nie działa ?

class FilteredListView(ListView):
	filterset_class = None

	def get_queryset(self):
		queryset = super().get_queryset()
		self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
		return self.filterset.qs.distinct()

	def get_context_data(self, ** kwargs):
		context = super().get_context_data( ** kwargs)
		context['filterset'] = self.filterset
		return context


class BookFilterSet(django_filters.FilterSet):
	def __init__(self, data, * args, ** kwargs):
		data = data.copy()
		data.setdefault('format', 'paperback')
		data.setdefault('order', '-added')
		super().__init__(data, * args, ** kwargs)


class BookListView(FilteredListView):
	filterset_class = BookFilterSet
	paginate_by = 5


# ---------------------------------------------
# IV tu z kolei nie zwraca mi form żadnych pól do wypełnienia?????
class BookFilter(django_filters.FilterSet):
	title = django_filters.CharFilter(lookup_expr='iexact')

	class Meta:
		model = Book
		fields = ['published_date', 'authors_name', 'language_book', ]


# class BookFilterSearchListView(ListView):
# 	model = Book
# 	template_name = 'booklist/filter_book_search.html'
# 	paginate_by = 5
	# form_class = BookFilter




# --------------------------------
# to do osobnego url bez definiowania view tutaj w views
# dla widoku FilterView

# dlaczego jak filtr nie ma rezultatów to mi sypie that page contains no results
# excpetion type emptypage



class F(django_filters.FilterSet):
	#  co jest w tym złego ?
	title = django_filters.CharFilter(method='my_custom_filter')
	published_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))

	class Meta:
		model = Book

		fields = {
			'title': ['icontains'],
			'authors_name': ['icontains'],
			'language_book': ['icontains'],
			'published_date': ['gte'],
			# 'published_date': ['gte', 'lte'],
		}
		# widgets = {'published_date': DateInput(), }

	def my_custom_filter(self, queryset, name, value):
		return queryset.filter(**{name: value, })


class MojFilterWithPag(FilterView):
	filterset_class = F
	paginate_by = 5
	# jak to sie ma do uzycia innych metod, ktore robia zmiany dla queryset i jak to jest nadpisywane?
	# queryset = User.objects.all()

	def get_queryset(self):
		queryset = super().get_queryset()
		self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
		# ---------------------------------------------

		# co to robi tutaj
		# ---------------------------------------------

		return self.filterset.qs.distinct()

	# w html zmienna {{filterset}} pojawi sie tylko jesli context bedzie ja mal
	# def get_context_data(self, **kwargs):
	# 	context = super().get_context_data(**kwargs)
	# 	context['filterset'] = self.filterset
	# 	return context

	def get_paginate_by(self, queryset):

		# ---------------------------------------------
		# co tutaj zrobic zeby ta paignacja dostala odpowiednie dane do paginowania
		# ---------------------------------------------

		return super().get_paginate_by(queryset=self.filterset)

	# ---------------------------------------------
	#  moze da sie jakos uzyc paginate queryset
	# ---------------------------------------------

	# def paginate_queryset(self, queryset, page_size):
	# 	"""Paginate the queryset, if needed."""
	# 	paginator = self.get_paginator(
	# 		queryset, page_size, orphans=self.get_paginate_orphans(),
	# 		allow_empty_first_page=self.get_allow_empty())
	# 	page_kwarg = self.page_kwarg
	# 	page = self.kwargs.get(page_kwarg) or self.request.GET.get(page_kwarg) or 1
	# 	try:
	# 		page_number = int(page)
	# 	except ValueError:
	# 		if page == 'last':
	# 			page_number = paginator.num_pages
	# 		else:
	# 			raise Http404(_('Page is not “last”, nor can it be converted to an int.'))
	# 	try:
	# 		page = paginator.page(page_number)
	# 		return (paginator, page, page.object_list, page.has_other_pages())
	# 	except InvalidPage as e:
	# 		raise Http404(_('Invalid page (%(page_number)s): %(message)s') % {
	# 			'page_number': page_number,
	# 			'message': str(e)
	# 		})
	# ---------------------------------------------------------


class BookFilterSearchPag(FormView):
	template_name = 'booklist/book_filter_search_pag.html'
	form_class = BookFilterSearchPagForm
	queryset = Book.objects.all()
	# success_url = reverse_lazy('booklist:index')

	# def form_valid(self, form):
	# 	print(form.cleaned_data)
	# 	return super().form_valid(form)


class BookFilterSearchPagList(ListView):
	pass


class BookListViewSearchView(ListView):
	template_name = 'booklist/book_listview_filter_search.html'
	model = Book
	form = InputForm
	paginate_by = 5
	# pamiętać o Q filtrach and &

	def get(self, request, *args, **kwargs):
		print('args: ', args)
		print('kwargs: ', kwargs)
		print('to jest request z get : ', request)
		return super().get(request, *args, **kwargs)

	# def get_paginator(self, queryset, per_page, orphans=0,
    #                   allow_empty_first_page=True, **kwargs):

	def get_queryset(self):
		queryset = super().get_queryset()
		print(queryset)
		# title = self.kwargs.get('title', '')
		print('to jest title z request GET get: ', self.request.GET.get('title', ''))
		q_list = []
		title = self.request.GET.get('title', '')
		if title:
			q_list.append(Q(title__icontains=title),)
		published_date_gte = self.request.GET.get('published_date_from', '')
		if published_date_gte:
			q_list.append(Q(published_date__gte=published_date_gte),)
			print('pub date from, from, from, from: ', published_date_gte)
		# print('pub date from, from, from, from: ', published_date_gte)
		published_date_lte = self.request.GET.get('published_date_to', '')
		if published_date_lte:
			q_list.append(Q(published_date__lte=published_date_lte),)
		authors_name = self.request.GET.get('authors_name', '')
		if authors_name:
			q_list.append(Q(authors_name__icontains=authors_name),)
		language_book = self.request.GET.get('language_book', '')
		if language_book:
			q_list.append(Q(language_book__icontains=language_book),)


		print('querysecik:   \n', queryset)
		print('dlugosc len od q_list to: ', len(q_list))
		object_filtered = ''
		if len(q_list) > 0:
			object_filtered = queryset.filter(reduce(operator.and_, q_list)).distinct()
			print('obj to: ', object_filtered)
		else:
			print('nie jest dluzszy niz 0 len od q_list')
		if object_filtered:
			print('object with filter Q dates and title:     \n', object_filtered)
			return object_filtered
		else:
			print('nie ma object_filtered dlatego zwroci czysty queryset')
			return queryset

		# filter(fromdate__gte=form_fromdate, todate__lte=form_todate)
		# .objects.filter(reduce(operator.and_, q_list))
		# print('pub date gte: ', published_date_gte)
		# object_list = self.model.objects.all()
		# if title:
		# 	object_list = queryset.filter(title__icontains=title)
		# 	return object_list.order_by('-pk')
		# else:
		# 	return queryset

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['form'] = InputForm
		print('czyli to jest context form:   ', context['form'])
		_request_copy = self.request.GET.copy()
		parameters = _request_copy.pop('page', True) and _request_copy.urlencode()
		context['parameters'] = parameters
		return context












# tu juz dzialajce stary kod
# ------------------------------------------------------------------------------
class BookImportView(TemplateView):
	template_name = 'booklist/import_phrase.html'
	# awfgsgdrsgdesbdgfbgfbfgbfgbfgbgfbfgbfgbgf  keyword to test import new book in api google with no results

	def get(self, request, *args, **kwargs):
		return super().get(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		phrase = request.POST.get('phrase')
		if not phrase:
			message = 'field is empty pls input some phrase'
			return render(request, 'booklist/import_failed.html', {'error_message': message})

		url = url_builder(phrase)
		response = get(url)
		if response.status_code != 200:
			message = 'error inside request for books, pls try again'
			return render(request, 'booklist/import_failed.html', {'error_message': message})
		response = loads(response.text)
		if not response.get('items'):
			return render(
				request,
				'booklist/import_failed.html',
				{'error_message': 'no information about that phrase'}
			)
		books_to_be_created = prepare_list_of_json_to_bulk_create(response)

		try:
			books_importer = BooksImporterApi(phrase)
			books_importer.run()
		except Exception as message:
			return render(request, 'booklist/import_failed.html', {'error_message': message})
		print(type(books_importer.objects))
		for book_preparation in books_importer.objects:
			books_importer.objects_books.append(Book(title=book_preparation['title'],
													 authors_name=book_preparation['authors'],
													 published_date=book_preparation['publishedDate'],
													 isbn13_number=book_preparation['isbn_13'],
													 page_number=book_preparation['pageCount'],
													 language_book=book_preparation['language'],
													 link_book_cover=book_preparation['link_book_cover'],
													 )
												)
		Book.objects.bulk_create(books_importer.objects_books)
		return render(request, 'booklist/import_success.html', {'amount': books_importer.how_many_objects()})


		# 	return render(request, 'booklist/import_success.html', {'amount': amount})
		# message = 'No records which meet the criteria saving for db, please try again with change phrase importing'
		# return render(request, 'booklist/import_failed.html', {'error_message': message})


class BookDetailView(DetailView):
	# model = Book
	template_name = 'booklist/book_detail.html'
	# queryset = Book.objects.all()

	def get_object(self):
		id_ = self.kwargs.get("id")
		return get_object_or_404(Book, id=id_)

# def get_queryset(self):
# 	print(self.kwargs.get("pk"))
# 	return Book.objects.filter(id=pk)


    # Book.objects.filter(pub_date__lte=timezone.now()).exclude(
    #     choice__choice_text__isnull=True).order_by('-pub_date')[:10]

   #  def get_context_data(self, **kwargs):
   #      context = super().get_context_data(**kwargs)
   #      author = context['object']
   #      print(author.id)
   #      context['books'] = Book.objects.filter(author__id=author.id)
   #      if author.id:
   #          context['personal_description'] = AuthorDescription.objects.get(author__id=author.id)
   #      return context


class BookCreateView(CreateView):
	template_name = 'booklist/book_create_form.html'
	form_class = BookModelForm
	queryset = Book.objects.all()
	# success_url = reverse_lazy('booklist:index')

	def form_valid(self, form):
		print(form.cleaned_data)
		return super().form_valid(form)

	# def get_success_url(self):
	# 	return reverse('booklist:index')


class BookDeleteView(DeleteView):
	template_name = 'booklist/delete_book.html'

	def get_object(self):
		id_ = self.kwargs.get("id")
		return get_object_or_404(Book, id=id_)

	def get_success_url(self):
		return reverse('booklist:index')


class BookUpdateView(UpdateView):
	template_name = 'booklist/book_update_form.html'
	form_class = BookModelForm
	# success_url = reverse_lazy('booklist:index')

	def get_object(self):
		id_ = self.kwargs.get("id")
		return get_object_or_404(Book, id=id_)

	def form_valid(self, form):
		print(form.cleaned_data)
		return super().form_valid(form)























# class IndexView(generic.ListView):
#     template_name = 'bestbooks/index.html'
#     context_object_name = 'authors_lists'
#
#     def get_queryset(self):
#         return Author.objects.all()
#
#
# def mainview(request):
#     last_books = Book.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')[:3]
#     authors = Author.objects.filter(created__lte=timezone.now()).order_by('-created')[:3]
#
#     if authors:
#
#         print(f'ksiazki autora: {authors[0].books.all()}')
#     # if not authors and not last_books:
#         # redirect to
#     # 'books': books,
#     return render(request, 'bestbooks/main.html', {'authors': authors,'last_books': last_books})


# def detailview(request, pk):
#     author = get_object_or_404(Author, pk=pk)
#     return render(request, 'bestbooks/detail.html', {'object': author})
#
#
# def detail_book_view(request, pk):
#     book = get_object_or_404(Book, pk=pk)
#     return render(request, 'bestbooks/book_detail.html', {'book': book})
#
#
# def comment_view(request, pk):
#     book = get_object_or_404(Book, pk=pk)
#     return render(request, 'bestbooks/comment_view.html', {'object': book})


# @login_required
# def book_new(request):
#     if request.method == "POST":
#         form = BookForm(request.POST)
#         if form.is_valid():
#             book = form.save(commit=False)
#             book.added_by = request.user
#             # post.published_date = timezone.now()
#             book.save()
#             return redirect('book_detail', pk=book.pk)
#     else:
#         form = BookForm()
#     return render(request, 'blog/book_edit.html', {'form': form})
#
#
# @login_required
# def book_edit(request, pk):
#     book = get_object_or_404(Book, pk=pk)
#     if request.method == "POST":
#         form = BookForm(request.POST, instance=book)
#         if form.is_valid():
#             book = form.save(commit=False)
#             book.added_by = request.user
#             # post.published_date = timezone.now()
#             book.save()
#             return redirect('book_detail', pk=book.pk)
#     else:
#         form = BookForm(instance=book)
#     return render(request, 'blog/post_edit.html', {'form': form})



# class DetailView(generic.DetailView):
#     model = Author
#     template_name = 'bestbooks/detail.html'
    # Book.objects.filter(pub_date__lte=timezone.now()).exclude(
    #     choice__choice_text__isnull=True).order_by('-pub_date')[:10]

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     author = context['object']
    #     print(author.id)
    #     context['books'] = Book.objects.filter(author__id=author.id)
    #     if author.id:
    #         context['personal_description'] = AuthorDescription.objects.get(author__id=author.id)
    #     return context
   # def get_queryset(self):
    #     return Author.objects.filter(id=pk)


# class Detail_Book_View(generic.DetailView):
#     # template_name_suffix = '_detail'
#     # template_name_field = 'book_detail'
#     model = Book
#     template_name = 'bestbooks/book_detail.html'
    # Book.objects.filter(pub_date__lte=timezone.now()).exclude(
    #     choice__choice_text__isnull=True).order_by('-pub_date')[:10]

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     author = context['object']
    #     print(author.id)
    #     context['books'] = Book.objects.filter(author__id=author.id)
    #     if author.id:
    #         context['personal_description'] = AuthorDescription.objects.get(author__id=author.id)
    #     return context


# class MainView(generic.ListView):
#     template_name = 'bestbooks/main.html'
#     context_object_name = 'authors_and_books'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['books'] = Book.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')[:3]
#         context['authors'] = Book.objects.filter(created__lte=timezone.now()).order_by('-created')[:3]
#         print(context)
#         return context

    # def get_queryset(self):
    #     return Book.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')[:3]

    # def get_context_data(self, *args, **kwargs):
    #     ctx = super().get_context_data(*args, **kwargs)
    #     ctx['authors'] = ...
    #     return ctx





# def results(request, question_id):
#     response = 'you are looking at the results of question %s.'
#     return HttpResponse(response % question_id)
#
#
# def vote(request, question_id):
#     return HttpResponse('you are voting on question %s.' % question_id)
#
#
# def authors_list(request):
#     authorsList = Author.objects.all()
#     return render(request, 'bestbooks/authors_list.html', {'authorsList': authorsList})
#
#
# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[0:5]
#     context = {
#         'latest_question_list': latest_question_list,
#     }
#     return render(request, 'polls/index.html', context)


# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     print(f'wyswietl question {question}')
#     return render(request, 'polls/detail.html', {'question': question})