from __future__ import (absolute_import, division, print_function, )
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
from .forms import BookModelForm, InputFormFilter, InputFormSearch
from .filters import BooklistFilter
from .filters import AvailFilter
# AvailFilter

# ---------------------------------------
from requests import get, exceptions
from json import loads
# from .api_google_book_utils import url_builder
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


class BookListViewSearchView(ListView):
	template_name = 'booklist/book_listview_filter_search.html'
	model = Book
	paginate_by = 5

	def get(self, request, *args, **kwargs):
		print('args: ', args)
		print('kwargs: ', kwargs)
		print('to jest request z get : ', request)
		return super().get(request, *args, **kwargs)

	def get_queryset(self):
		# search: https://learndjango.com/tutorials/django-search-tutorial
		queryset = super().get_queryset()
		# print(queryset)
		print('to jest title z request GET get: ', self.request.GET.get('title', ''))
		search_field = self.request.GET.get('search_field', '')
		print('to jest search field\n', search_field)
		if search_field:
			query = Q()
			query |= Q(title__icontains=search_field)
			query |= Q(authors_name__icontains=search_field)
			query |= Q(language_book__icontains=search_field)
			order_search_map = {
				'ascending_title': 'title',
				'descending_title': '-title',
				'ascending_page_number': 'page_number',
				'descending_page_number': '-page_number',
				'ascending_language_book': 'language_book',
				'descending_language_book': '-language_book',
			}
			queryset = queryset.order_by(order_search_map.get(self.request.GET.get('order_search')))
			return queryset.filter(query)
		query = Q()
		title = self.request.GET.get('title', '')
		if title:
			query &= Q(title__icontains=title)
		published_date_gte = self.request.GET.get('published_date_from', '')
		if published_date_gte:
			query &= Q(published_date__gte=published_date_gte)
		published_date_lte = self.request.GET.get('published_date_to', '')
		if published_date_lte:
			query &= Q(published_date__lte=published_date_lte)
		authors_name = self.request.GET.get('authors_name', '')
		if authors_name:
			query &= Q(authors_name__icontains=authors_name)
		language_book = self.request.GET.get('language_book', '')
		if language_book:
			query &= Q(language_book__icontains=language_book)
		# print('querysecik before filtered field added to filter:   \n', queryset)
		# print('to jest queryset: \n', queryset.filter(query))
		if self.request.GET.get('ordering'):
			order_map = {
				'ascending_title': 'title',
				'descending_title': '-title',
				'ascending_pub_date': 'published_date',
				'descending_pub_date': '-published_date',
				'ascending_page_number': 'page_number',
				'descending_page_number': '-page_number',
				'ascending_language_book': 'language_book',
				'descending_language_book': '-language_book',
			}
			queryset = queryset.order_by(order_map.get(self.request.GET.get('ordering')))
		return queryset.filter(query)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		form_dict = {}
		form_dict_order = {}
		# print('czyli to jest context object_list:   ', context['object_list'], '\n i page obj: \n', context['page_obj'])
		form_dict.update(
			language_book=self.request.GET.get('language_book', ''),
			title=self.request.GET.get('title', ''),
			published_date_to=self.request.GET.get('published_date_to', ''),
			published_date_from=self.request.GET.get('published_date_from', ''),
			authors_name=self.request.GET.get('authors_name', ''),
			ordering=self.request.GET.get('ordering', 'descending_pub_date'),
		)
		form_dict_order.update(
			order_search=self.request.GET.get('order_search', 'ascending_title'),
		)
		context['form'] = InputFormFilter(initial=form_dict)
		context['form_search'] = InputFormSearch(initial=form_dict_order)
		if self.request.GET.get('search_field', ''):
			context['search_field_found'] = self.request.GET.get('search_field', '')
		_request_copy = self.request.GET.copy()
		parameters = _request_copy.pop('page', True) and _request_copy.urlencode()
		context['parameters'] = parameters
		return context


# ------------------------------------------------------------------------------
class BookImportView(TemplateView):
	template_name = 'booklist/import_phrase.html'
	# 'awfgsgdrsgdesbdgfbgfbfgbfgbfgbgfbfgbfgbgf'  keyword to test import new book in api google with no results

	def get(self, request, *args, **kwargs):
		return super().get(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		phrase = request.POST.get('phrase', '')
		if not phrase:
			message = 'field is empty pls input some phrase'
			return render(request, 'booklist/import_failed.html', {'error_message': message})
		try:
			books_importer = BooksImporterApi(phrase)
			books_importer.run()
		except Exception as message:
			return render(request, 'booklist/import_failed.html', {'error_message': message})
		print(type(books_importer.objects))
		for book_preparation in books_importer.objects:
			books_importer.objects_books.append(
				Book(title=book_preparation['title'],
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


class BookDetailView(DetailView):
	# model = Book
	template_name = 'booklist/book_detail.html'
	# queryset = Book.objects.all()

	def get_object(self):
		id_ = self.kwargs.get("id")
		return get_object_or_404(Book, id=id_)


class BookCreateView(CreateView):
	template_name = 'booklist/book_create_form.html'
	form_class = BookModelForm
	queryset = Book.objects.all()
	# success_url = reverse_lazy('booklist:index')

	def form_valid(self, form):
		print('to jest cleaned data \n', form.cleaned_data)
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