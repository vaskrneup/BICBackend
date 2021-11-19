from django.db import models


class Base(models.Model):
    def get_serialized_data(self, fields, default_on_none=None):
        output = {}

        for field in fields:
            output[field] = getattr(self, field, default_on_none)

        return output


class Stock(Base):
    product_name = models.CharField("Product Name", max_length=256)
    product_quantity = models.IntegerField("Product Quantity")
    product_cost_price = models.FloatField("Product Cost Price")
    product_sell_price = models.FloatField("Product Sell Price")
    profit = models.FloatField("Profit")

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.profit = self.product_sell_price - self.product_cost_price
        return super(Stock, self).save(
            force_insert=False, force_update=False, using=None,
            update_fields=None
        )

    def __str__(self):
        return self.product_name


class Message(Base):
    sent_date = models.DateTimeField("Sent On", auto_now_add=True)
    sender = models.CharField("Sender", max_length=256)
    message_text = models.TextField("Message")

    def __str__(self):
        return self.message_text


class MarketPlace(Base):
    product_name = models.CharField("Product Name", max_length=256)
    farmer_sell_price = models.FloatField("Farmer Sell Price")
    location = models.CharField("Location", max_length=128)

    def __str__(self):
        return self.product_name
