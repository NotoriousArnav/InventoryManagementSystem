from django.db import models
from django.template.defaultfilters import slugify  # new
from django.urls import reverse
import uuid
from PIL import Image

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

    def product_count(self):
        return self.product_set.count()

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
    slug = models.SlugField(max_length=200, null=True, unique=True)

    def total_stock(self):
        return f"Rs. {self.qty*self.price}"

    def get_absolute_url(self):
        return reverse("product", kwargs={"slug": self.slug})

    def __str__(self):
        return f"{self.name}:{self.qty}:{str(self.id)[:5]}"

    def attachments(self):
        return self.productattachment_set.count()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, self.id)
        return super().save(*args, **kwargs)

class ProductAttachment(models.Model):
    id = models.UUIDField(
        primary_key = True,
        default = uuid.uuid4,
        editable = False
    )
    file = models.ImageField('Attachment', upload_to='attachments/')
    publication = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Product Image')
    file_name = models.CharField(
        max_length = 200,
        default = publication.name
    )

    class Meta:
        verbose_name = 'Attachment'
        verbose_name_plural = 'Attachments'

    def save(self, *args, **kwargs):
        if self.file:
            # Resize the image using Pillow
            img = Image.open(self.file)
            img = img.resize((500, 500), Image.LANCZOS)  # Adjust dimensions as needed
            img.save('media/attachments/'+str(self.id)+'.jpg')

            # Rename the file using the model instance's ID
            self.file_name = f"{self.id}.{self.file.name}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Product name: {self.publication.name} || Attachment name:{self.file_name}"
