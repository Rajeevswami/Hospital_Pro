"""Hospital (Tenant) model — each hospital is a tenant."""
from django.db import models
from django_tenants.models import TenantMixin, DomainMixin


class Hospital(TenantMixin):
    """Each hospital is an isolated tenant with its own schema."""
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    logo = models.ImageField(upload_to='hospitals/logos/', blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, default='IN')
    postal_code = models.CharField(max_length=20, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    license_number = models.CharField(max_length=100, blank=True)
    bed_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    auto_create_schema = True

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Domain(DomainMixin):
    """Domain mapping for multi-tenant routing."""
    pass


class Department(models.Model):
    """Hospital departments — tenant-scoped."""
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='departments')
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20)
    head_doctor = models.ForeignKey(
        'doctors.Doctor', on_delete=models.SET_NULL, null=True, blank=True, related_name='headed_departments'
    )
    floor = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('hospital', 'code')

    def __str__(self):
        return f"{self.name} ({self.hospital.name})"
