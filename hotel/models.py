from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.

class Customer(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
	first_name = models.CharField(max_length=200, null=True)
	last_name = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True)
	image = models.ImageField(default='profile_pic.png', upload_to='customer_pics')

	def __str__(self):
		return str(self.first_name)

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)

		img = Image.open(self.image.path)

		if img.height > 500 or img.width > 500:
			output_size = (500,500)
			img.thumbnail(output_size)
			img.save(self.image.path)
		


class Food(models.Model):
	name = models.CharField(max_length=200, null=True)
	price = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=True)
	available = models.BooleanField(default=True, null=True, blank=False)
	available_plates = models.IntegerField()
	image = models.ImageField(default='hotelpic3.jpg', upload_to='food_pics')

	
	def __str__(self):
		return str(self.name)

	@property
	def availability(self):
		plates_left = this.available_plates
		return self.availability
	
	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)

		img = Image.open(self.image.path)

		if img.height > 500 or img.width > 500:
			output_size = (500,500)
			img.thumbnail(output_size)
			img.save(self.image.path)
	
class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False, blank=False, null=True)
	transaction_id = models.CharField(max_length=200, null=True)


	def __str__(self):
		return str(self.id)

	@property
	def get_tray_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total
	
	@property
	def get_tray_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total
	


class OrderItem(models.Model):
	product = models.ForeignKey(Food, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.product.name)

	@property
	def get_total(self):
		total = self.quantity * self.product.price 
		return total
	

class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
	phone_number = models.CharField(max_length=20, null=False)
	address = models.CharField(max_length=20, null=False)
	city = models.CharField(max_length=20, null=False)
	
	def __str__(self):
		return str(self.address)
