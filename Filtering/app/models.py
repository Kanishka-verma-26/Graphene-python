from django.db import models

# Create your models here.
class Animal(models.Model):

    DOG = 'DO'
    CAT = "CA"
    RABBIT = "RA"
    COW="CO"
    MOUSE = 'MO'
    PARROT = 'PA'
    OTHER = 'OT'

    animal_choices = [(DOG,'Dog'),(CAT,'Cat'),(RABBIT,'Rabbit'),
                      (COW,'Cow'),(MOUSE,'Mouse'),(PARROT,'Parrot'),(OTHER,'Other'),]

    name = models.CharField(max_length=100)
    animal = models.CharField(max_length=2, choices=animal_choices, default=DOG,)
    age = models.IntegerField()
    is_domestic = models.BooleanField(default=True)

    def __str__(self):
        return self.name