from django.db import models
from django.utils.text import slugify
from django.conf import settings


class Recipe(models.Model):
    """
    Recet je "glavni" entitet.

    Django model = Python klasa koja se mapira na tablicu u bazi.
    Svaki atribut ispod je stupac u tablici.
    """
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="recipes",
        db_index=True,
    )

    title = models.CharField(max_length=200)

    slug = models.SlugField(max_length=220, unique=True, blank=True)

    description = models.TextField(blank=True)

    instructions = models.TextField(blank=True)

    prep_time_minutes = models.PositiveSmallIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    is_public = models.BooleanField(default=False)

    image = models.ImageField(upload_to="recipes/", blank=True, null=True)

    def save(self, *args, **kwargs):
        """
        Ovdje auto-generiramo slug ako ga korisnik nije upisao.
        """

        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 2

            while Recipe.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter +=1
            self.slug = slug
        
        super().save(*args, **kwargs)

    def __str__(self):
        #Prikaz u adminu i shellu
        return self.title
    

class Ingredient(models.Model):
    """Sastojak pripada jednom receptu: jedan recept -- više sastojaka"""

    #ForeignKey , veza many-to-one (više sastojaka na jedan recept)
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="ingredients",
    )

    #npr "Brašno", "Jaja", "Mlijeko"
    name = models.CharField(max_length=120)

    # količina kao tekst ne brojevi, jer bude "200g" ili "1/2 žličice" ili "po želji"
    amount = models.CharField(max_length=80, blank=True)

    def __str__(self):
        if self.amount:
            return f"{self.name} ({self.amount})"
        return self.name
    