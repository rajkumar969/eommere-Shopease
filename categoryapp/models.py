from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from PIL import Image
from .utils import optimize_image

# Create your models here.

class Category(models.Model):
    category_name=models.CharField(max_length=100,null=False)
    slug=models.SlugField(max_length=150,unique=True)
    profile_image = models.ImageField(
        upload_to="categories/",
        blank=True,
        null=True
        )
    description=models.TextField(blank=True)
    status = models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['category_name']
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category_name
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.profile_image:
            optimize_image(
                self.profile_image.path,
                max_size=(800, 800)
            )
    
class Subcategory(models.Model):
        id=models.BigAutoField(primary_key=True,help_text='Unique id of subcategory')
        category_name=models.ForeignKey(Category , on_delete=models.CASCADE,
               related_name='subcategories',
               help_text="Reference to parent category."  ,
                db_column='categories' )   
        name=models.CharField(max_length=100,null=False)   
        slug=models.SlugField(max_length=150,unique=True,help_text="URL friendly unique name")                                                                                    
        description=models.TextField(null=True,blank=True,help_text="Description about subCategory")
        status=models.BooleanField(default=True,help_text="True = Active, False = Inactive")
        created_at = models.DateTimeField(default=timezone.now, help_text="Subcategory creation date.") 
        class Meta:
            db_table = 'subcategory'
            verbose_name_plural = "SubCategories"

        def __str__(self):
            return f"{self.name} ({self.category_name.category_name})" 



class Brand(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(
        max_length=200,
        unique=True,
        null=True,
        blank=True
    )
    image = models.ImageField(
        upload_to='BrandImage/',
        null=True,
        blank=True
    )
    description = models.TextField(
        blank=True,
        null=True
    )
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now) 

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            optimize_image(
                self.image.path,
                max_size=(800, 800)
            )


class Products(models.Model):
     category=models.ForeignKey( Category,on_delete=models.CASCADE,
       related_name='products', 
       db_column='categories_id',
       help_text="Reference to parent category."                                       
     )
     subcategory=models.ForeignKey(Subcategory,on_delete=models.CASCADE,
                                   related_name='products',
                                   db_column='subcategory_id'
                                   )
     brand=models.ForeignKey(Brand,on_delete=models.CASCADE,
                              related_name='products',
                             db_column='Brand_id'
                             ) 
     
     product_name=models.CharField(max_length=100,null=False ,unique=True)
     slug=models.SlugField(max_length=200,unique=True)  
     price=models.DecimalField(max_digits=10,decimal_places=2)
     discount=models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)
     description=models.TextField(blank=True,null=True)
     stock=models.PositiveIntegerField(default=0)
     image=models.ImageField(upload_to='productsImage/')
     rating=models.DecimalField(max_digits=5,decimal_places=3,default=0.00)
     status=models.BooleanField(default=True)
     created_at=models.DateTimeField(auto_now_add=True)
     def save(self,*args,**kwargs):
          if not self.slug:
               self.slug=slugify(self.product_name)
          super().save(*args,**kwargs)
          if self.image:
                      optimize_image(
                          self.image.path,
                          max_size=(800, 800)
                      )
          
         
     def __str__(self):
          return self.product_name      

       