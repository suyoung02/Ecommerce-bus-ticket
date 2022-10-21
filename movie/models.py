from django.db import models

class Trip(models.Model):
    product_name=models.CharField(max_length=255)
    departure =  models.CharField(max_length=200, null=False)
    destination =  models.CharField(max_length=200, null=False)
    booked_seats=models.ManyToManyField('Seat',blank=True)
    price = models.IntegerField()
    start_date = models.DateTimeField()
    is_available = models.BooleanField(default=True)
    #category = models.ForeignKey(Category, on_delete=models.CASCADE)    # Khi xóa category thì Product bị xóa
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    def __str__(self) -> str:
        return f"{self.product_name} (${self.price})"

class Seat(models.Model):
    seat_no=models.IntegerField()
    occupant_username =models.CharField(max_length=255)        
    occupant_email=models.EmailField(max_length=555)     
    purchase_time=models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.occupant_username} seat_no {self.seat_no}"

class Payment(models.Model):
    username=models.CharField(max_length=255)
    email=models.EmailField(max_length=255)
    phone=models.CharField(max_length=255)
    trip=models.ForeignKey(Trip,on_delete=models.SET_NULL,null=True,blank=True)
    seat_no=models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)