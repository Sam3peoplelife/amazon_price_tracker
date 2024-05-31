from django.db import models
from .utils import get_link_data

class Link(models.Model):
    name = models.CharField(max_length=220, blank=True)
    url = models.URLField()
    current_price = models.FloatField(blank=True, null=True)
    old_price = models.FloatField(default=0)
    price_difference = models.FloatField(default=0)
    updated = models.TimeField(auto_now=True)
    created = models.TimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ('price_difference', '-created')

    def save(self, *args, **kwargs):
        name, price = get_link_data(self.url)
        try:
            price = float(price)
        except (ValueError, TypeError):
            price = 0.0

        old_price = self.current_price or 0.0
        if self.current_price is not None:
            if price != old_price:
                diff = price - old_price
                self.price_difference = round(diff, 2)
                self.old_price = old_price
        else:
            self.old_price = 0
            self.price_difference = 0

        self.name = name
        self.current_price = price

        super().save(*args, **kwargs)
