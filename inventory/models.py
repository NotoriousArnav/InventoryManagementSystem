from django.db import models
import uuid

# Create your models here.
class Category(models.Model):
    id = models.UUIDField(
        primary_key = True,
        default = uuid.uuid4,
        editable = False
    )
    name = models.CharField(
        max_length=200
    )
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    id = models.UUIDField(
        primary_key = True,
        default = uuid.uuid4,
        editable = False
    )
    name = models.CharField(
        max_length=200
    )
    description = models.TextField(
        blank = True,
        null = True,
    )
    category = models.ManyToManyField(Category)
    price = models.FloatField(default=100)
    qty = models.IntegerField(default=1)

    def __str__(self):
        return self.name

class ProductAttachment(models.Model):
    id = models.UUIDField(
        primary_key = True,
        default = uuid.uuid4,
        editable = False
    )
    file = models.ImageField('Attachment', upload_to='attachments/')
    file_type = models.CharField('File type', choices=AttachmentType.choices, max_length=10)

    publication = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Product Image')

    class Meta:
        verbose_name = 'Attachment'
        verbose_name_plural = 'Attachments'