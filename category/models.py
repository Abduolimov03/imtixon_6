from django.db import models
from django.contrib.auth.admin import User

class Category(models.Model):
    name = models.CharField(max_length=120)

    class Meta:
        db_table = 'category'

    def __str__(self):
        return self.name

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.CharField(max_length=50, null=True )
    desc = models.TextField()
    price =models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', default='default/products.jpg', blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)


    class Meta:
        ordering = ['-created_at']
        db_table = 'products'

    def __str__(self):
        return self.desc

class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.title}"