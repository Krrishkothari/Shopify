from django.db import models

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    password = models.CharField(max_length=100)

    def register(self):
        self.save()

    def isEXIST(self):
        if Customer.objects.filter(email=self.email):
            return True 
        return False

    @staticmethod
    def get_customer_by_email(email):
        return Customer.objects.filter(email=email).first()  # This will return the first matching customer or None
