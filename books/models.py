from django.core.validators import MinValueValidator
from django.db import models


class Book(models.Model):
    class CoverType(models.TextChoices):
        HARD = "HARD", "Hardcover"
        SOFT = "SOFT", "Softcover"

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.CharField(
        max_length=4,
        choices=CoverType.choices,
        default=CoverType.SOFT,
        null=True,
        blank=True,
    )
    inventory = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    daily_fee = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.title} by {self.author} ({self.cover})"

    class Meta:
        ordering = [
            "title",
        ]
