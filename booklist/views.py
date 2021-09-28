from django.shortcuts import (render, get_object_or_404, redirect,)
from django.urls import reverse, reverse_lazy
# from django.views import generic
from django.views.generic import (
	TemplateView,
	DetailView,
	CreateView,
	ListView,
	DeleteView,
	UpdateView
)
# ---------------------------------------
from .models import Book
from .forms import BookModelForm
from .filters import BooklistFilter
# ---------------------------------------
from requests import get
from json import loads
from .api_google_book_utils import prepare_listOfJson_to_bulk_create, url_builder
from datetime import date

# ------------------------

# from django.contrib.auth.decorators import login_required
# from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect

from .working_file import BooksImporter


class IndexView(ListView):
    template_name = 'booklist/index.html'
    context_object_name = 'booklist'

    def get_queryset(self):
        return Book.objects.all()


class BookFilterSearchListView(ListView):
	model = Book
	template_name = 'booklist/filter_search.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['filter'] = BooklistFilter(self.request.GET, queryset=self.get_queryset())
		return context


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
		books_to_be_created = prepare_listOfJson_to_bulk_create(response)

		try:
			books_importer = BooksImporter().run()
		except BooksError as e:
			return render(
				'gowno'
			)
		books_importer.objects
		try:
			amount = len(books_to_be_created)
		except exceptions.HTTPError as e:
			print("Error: " + str(e))
			amount = 0
			return amount
		if amount > 0:
			batch = [Book(title=row['title'],
						  authors_name='unknown' if row['authors'] == None else row['authors'],
						  published_date='unknown' if row['publishedDate'] == None else row['publishedDate'],
						  language_book='unknown' if row['language'] == None else row['language'],
						  link_book_cover='unknown' if row['link_book_cover'] == None else row['link_book_cover'],
						  page_number=0 if row['pageCount'] == None else row['pageCount'],
						  isbn13_number=0 if row['isbn_13'] == None else row['isbn_13'],
						  )
					 for row in books_to_be_created
					 ]
			Book.objects.bulk_create(batch)
			# return redirect(reverse('import_success', kwargs={'amount_added': amount}))
			return render(request, 'booklist/import_success.html', {'amount': amount})
		return redirect(reverse('import_failed', kwargs={'amount_added': amount}))


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