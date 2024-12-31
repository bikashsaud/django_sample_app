from datetime import timezone
from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self, using=None, keep_parents=False):
        super().delete(using=using, keep_parents=keep_parents)

    def restore(self):
        self.deleted_at = None
        self.save()

    @classmethod
    def all_objects(cls):
        return cls.objects.filter(deleted_at__isnull=True)

    @classmethod
    def deleted_objects(cls):
        return cls.objects.filter(deleted_at__isnull=False)
        


class Category(BaseModel):
    name = models.CharField(max_length=100, db_index=True) 

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}')>"

    @property
    def name_upper(self):
        return self.name.upper()
    
    
class Expense(models.Model):
    date = models.DateField()
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.date}: {self.description} - ${self.amount}"