from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Transaction, Sequence
from .tasks import *


class IndexView(generic.ListView):
    template_name = 'main/index.html'
    context_object_name = 'sequence_list'

    def get_queryset(self):
        return Sequence.objects.order_by('-id')


class TransactionListView(generic.ListView):
    template_name = 'main/transaction_list.html'
    context_object_name = 'transaction_list'

    def get_queryset(self):
        return Transaction.objects.all()


class TransactionDetailView(generic.DetailView):
    model = Transaction
    template_name = 'main/transaction_detail.html'


class SequenceDetailView(generic.DetailView):
    model = Sequence
    template_name = 'main/sequence_detail.html'


def process_json(request):
    Sequence.objects.all().delete()
    Transaction.objects.all().delete()
    transactions_dict = json_to_dict()
    transactions_list = [Transaction(
        description=vals['description'],
        amount=vals['amount'],
        date=try_strptime(vals['date'])
    ) for vals in transactions_dict]
    Transaction.objects.bulk_create(transactions_list)
    transactions = Transaction.objects.all()
    final_sets = compare(transactions)
    for id_list in final_sets:
        sequence = Sequence.objects.create(
            name=transactions.get(id=id_list[0]).description
        )
        transactions.filter(id__in=id_list).update(sequence=sequence)
    return HttpResponseRedirect(reverse('index'))
