from django.db import models


class Sequence(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    description = models.CharField(max_length=255)
    date = models.DateField()
    amount = models.DecimalField(
        max_digits=20,
        decimal_places=2
    )
    sequence = models.ForeignKey(
        Sequence,
        on_delete=models.CASCADE,
        null=True,
        related_name='transactions',
        related_query_name='transaction'
    )

    def __str__(self):
        return self.description
