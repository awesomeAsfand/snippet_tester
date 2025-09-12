from django.db import models
from django.contrib.auth.models import User


class Page(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pages")
    url = models.URLField(help_text="Full URL of the page you want to test")

    def __str__(self):
        return f"{self.url} ({self.user.username})"


class SnippetVariant(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name="variants")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    variant_label = models.CharField(
        max_length=5,
        help_text="Label for the variant, e.g., A, B, C"
    )

    def __str__(self):
        return f"{self.variant_label} for {self.page.url}"


class Test(models.Model):
    STATUS_CHOICES = [
        ("created", "Created"),
        ("running", "Running"),
        ("completed", "Completed"),
    ]

    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name="tests")
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="created")

    def __str__(self):
        return f"Test on {self.page.url} ({self.status})"

    def duration(self):
        return (self.end_date-self.start_date).days

    def get_variants(self):
        return self.page.variants.all()


