from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# python manage.py makemigrations
# python manage.py migrate

class Category(models.Model):
	name = models.CharField(max_length=256, null=False)
	image = models.ImageField(null=True, blank=True, upload_to="images/")
	active = models.BooleanField(default=True)

	# get all products with the same category
	@property
	def get_products(self):
		return Product.objects.filter(category=self)

	def __str__(self):
		return self.name

class Product(models.Model):
	name = models.CharField(max_length=256, null=False)
	code = models.CharField(max_length=256, null=False)
	price = models.DecimalField(decimal_places=2, max_digits=10, null=False)
	category = models.ForeignKey(Category, blank=True, default=None, on_delete = models.CASCADE)
	hot = models.BooleanField(default=False)
	cold = models.BooleanField(default=False)
	date_created = models.DateTimeField(default=timezone.now)
	active = models.BooleanField(default=True)

	def __str__(self):
		return self.name


class Customer(models.Model):
	name = models.CharField(max_length=200, null=True)
	phone = models.CharField(max_length=8, null=True, blank=True) # using Hong Kong phone num
	email = models.EmailField(null=True, blank=True)

	def __str__(self):
		return f"{self.name}, {self.phone}"

class Order(models.Model):
	
	STORE = [
		('A', 'A'),
		('B', 'B'),
		('C', 'C'),
	]
	
	STAY = [
		('Stay', 'Stay'),
		('Takeaway', 'Takeaway')
	]

	STATUS = [
		('Pending', 'Pending'),
		('Delivered', 'Delivered'),
		('Cancelled', 'Cancelled'),
	]

	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	store = models.CharField(max_length=64, null=True, choices=STORE)
	stay = models.CharField(max_length=64, null=True, choices=STAY) # stay in or takeaway
	date_created = models.DateTimeField(default=timezone.now)
	status = models.CharField(max_length=64, null=True, choices=STATUS, default='Pending')

	def __str__(self):
		return f"Order {self.id}"

	# get all OrderItems in the same order
	@property
	def get_items(self):
		return OrderItem.objects.filter(order=self)

	# count total items of same order
	@property
	def get_total_items(self):
		items = self.orderitem_set.all()
		total = sum([item.qty for item in items])
		return total 

	# count amount of same order
	@property
	def get_amount(self):
		items = self.orderitem_set.all()
		total = sum([item.get_subtotal for item in items])
		return total


class OrderItem(models.Model):
	
	HC = [
		('Hot', 'Hot'),
		('Cold', 'Cold')
	]
	
	order = models.ForeignKey(Order, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, null=True, on_delete= models.CASCADE, related_name='order_product')
	hotOrCold = models.CharField(max_length=64, null=True, choices=HC)
	qty = models.PositiveSmallIntegerField(null=True)

	def __str__(self):
		return self.product.name

	# count subtotal of each product item
	@property
	def get_subtotal(self):
		total = self.product.price * self.qty
		return total
