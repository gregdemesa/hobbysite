from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from .models import ProductType, Product, Transaction, Profile
from .forms import TransactionForm, ProductForm
from django.views.generic.edit import FormMixin, CreateView, UpdateView


class ProductListView(ListView):
    model = ProductType
    template_name = 'items_list.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            ctx['my_products'] = Product.objects.filter(
                author=self.request.user.profile
            )
            ctx['all_products'] = Product.objects.all()
        return ctx


class ProductDetailView(FormMixin, DetailView):
    model = Product
    form_class = TransactionForm
    template_name = 'items_detail.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        product = self.get_object()
        ctx['form'] = TransactionForm()
        if product.stock == 0:
            ctx['sold_out'] = True
        else:
            ctx['sold_out'] = False
        return ctx

    def post(self, request, *args, **kwargs):
        form = TransactionForm(request.POST)
        product = self.get_object()

        if form.is_valid():
            if request.user.is_authenticated:
                transaction = form.save(commit=False)
                transaction.buyer = request.user.profile
                transaction.product = product
                transaction.status = "ON CART"
                transaction.save()

                product.stock -= transaction.amount
                if product.stock == 0:
                    product.status = "OUT OF STOCK"
                else:
                    product.status = "AVAILABLE"
                product.save()
                return redirect("merchstore:cart")
            else:
                return redirect("login")
        return self.render_to_response(self.get_context_data(form=form))


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    template_name = 'items_create.html'
    form_class = ProductForm

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'items_update.html'
    fields = ('name', 'product_type', 'description',
              'price', 'stock', 'status')

    def get_success_url(self) -> str:
        return reverse_lazy('merchstore:product', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        product = form.save(commit=False)
        if product.stock == 0:
            product.status = 'OUT OF STOCK'
        else:
            product.status = 'AVAILABLE'
        product.save()
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        product = self.get_object()
        if product.stock == 0:
            product.status = "OUT OF STOCK"
        else:
            product.status = "AVAILABLE"
        product.save()
        return super().post(request, *args, **kwargs)


class CartView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'items_cart.html'
    context_object_name = 'author_transactions'
    form_class = TransactionForm

    def get_queryset(self):
        return Transaction.objects.filter(buyer=self.request.user.profile)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        author_transactions = {}
        for transaction in ctx['author_transactions']:
            author = transaction.product.author
            if author:
                author_display_name = author.display_name
                if author_display_name not in author_transactions:
                    author_transactions[author_display_name] = []
                author_transactions[author_display_name].append(transaction)
        ctx['author_transactions'] = author_transactions
        return ctx


class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'items_transaction.html'
    context_object_name = 'transactions'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        owned_products = Product.objects.filter(
            author=self.request.user.profile)

        buyers = Profile.objects.filter(
            transactions__product__in=owned_products).distinct()

        buyers_with_transactions = []
        for buyer in buyers:
            transactions = Transaction.objects.filter(
                buyer=buyer, product__in=owned_products)
            buyers_with_transactions.append((buyer, transactions))

        ctx['buyers_with_transactions'] = buyers_with_transactions
        return ctx
