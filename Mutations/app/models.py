from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Category(models.Model):
    topic = models.CharField(max_length=250)

    def __str__(self):
        return self.topic

class Pet(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



""" Django Rest Framework """

class Product(models.Model):

    category = models.CharField(max_length=100)
    title = models.CharField(verbose_name=_("title"),help_text=_("Required"),max_length=255)
    description = models.TextField(verbose_name=_("description"),help_text=_("Not Required"),blank=True)
    slug = models.SlugField(max_length=250)
    regular_price = models.DecimalField(verbose_name=_("Regular Price"),help_text=_("Maximum 999.99"),
                                        error_messages={                                                               # error_messages argument lets you specify manual error messages for attributes of the field.
                                            "name" : {
                                                "max_length": _("The price must be between 0 and 999.99"),
                                            },
                                        },
                                        max_digits=5, decimal_places=2
                                        )
    discount_price = models.DecimalField(verbose_name=_("Discount Price"),help_text=_("Maximum 999.99"),
                                        error_messages={                                                               # error_messages argument lets you specify manual error messages for attributes of the field.
                                            "name" : {
                                                "max_length": _("The price must be between 0 and 999.99"),
                                            },
                                        },
                                        max_digits=5, decimal_places=2
                                        )


    def __str__(self):
        return self.title