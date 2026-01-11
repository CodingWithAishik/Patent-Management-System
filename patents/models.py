from django.db import models
from django.utils.text import slugify


class IPCategory(models.Model):
    """Model for defining custom IP categories"""
    FIELD_TYPES = [
        ('text', 'Text (single line)'),
        ('textarea', 'Text Area (multiple lines)'),
        ('number', 'Number'),
        ('date', 'Date'),
        ('select', 'Dropdown/Select'),
    ]
    
    name = models.CharField(max_length=100, unique=True, verbose_name="Category Name")
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(null=True, blank=True, verbose_name="Description")
    field_definitions = models.JSONField(
        default=list,
        verbose_name="Field Definitions",
        help_text="JSON array defining fields for this category"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'ip_categories'
        ordering = ['name']
        verbose_name = 'IP Category'
        verbose_name_plural = 'IP Categories'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class IntellectualProperty(models.Model):
    """Model for storing dynamic IP data"""
    category = models.ForeignKey(
        IPCategory,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Category"
    )
    data = models.JSONField(
        default=dict,
        verbose_name="IP Data",
        help_text="JSON object storing field values"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'intellectual_properties'
        ordering = ['-created_at']
        verbose_name = 'Intellectual Property'
        verbose_name_plural = 'Intellectual Properties'
    
    def __str__(self):
        return f"{self.category.name} - {self.pk}"
    
    def get_display_title(self):
        """Get a display title from the first text field or ID"""
        if self.data:
            for key, value in self.data.items():
                if value and isinstance(value, str) and len(value) > 0:
                    return f"{value[:50]}" if len(value) > 50 else value
        return f"Item #{self.pk}"


class Copyright(models.Model):
    """Model for Copyright data"""
    sl_no = models.IntegerField(null=True, blank=True, verbose_name="Serial Number")
    year = models.CharField(max_length=10, null=True, blank=True, verbose_name="Year")
    faculty_students = models.TextField(null=True, blank=True, verbose_name="Name of Faculty/Students")
    title = models.TextField(null=True, blank=True, verbose_name="Title of Copy rights")
    filing_info = models.TextField(null=True, blank=True, verbose_name="Filing Informations")
    inventors = models.TextField(null=True, blank=True, verbose_name="Inventor(s)")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'copyrights'
        ordering = ['-year', '-sl_no']
        verbose_name = 'Copyright'
        verbose_name_plural = 'Copyrights'
    
    def __str__(self):
        return f"{self.year} - {self.title[:50] if self.title else 'N/A'}"


class PatentFiled(models.Model):
    """Model for Filed Patents"""
    sl_no = models.IntegerField(null=True, blank=True, verbose_name="Serial Number")
    date_of_filing = models.CharField(max_length=50, null=True, blank=True, verbose_name="Date of Filing")
    inventors = models.TextField(null=True, blank=True, verbose_name="Inventor(s)/Faculty/Student")
    title = models.TextField(null=True, blank=True, verbose_name="Title of Patent")
    application_number = models.CharField(max_length=100, null=True, blank=True, verbose_name="Application Number")
    date_of_publication = models.CharField(max_length=50, null=True, blank=True, verbose_name="Date of Publication")
    abstract = models.TextField(null=True, blank=True, verbose_name="Abstract")
    applicant_name = models.TextField(null=True, blank=True, verbose_name="Applicant Name")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'patents_filed'
        ordering = ['-date_of_filing', '-sl_no']
        verbose_name = 'Patent (Filed)'
        verbose_name_plural = 'Patents (Filed)'
    
    def __str__(self):
        return f"{self.date_of_filing} - {self.title[:50] if self.title else 'N/A'}"


class PatentGranted(models.Model):
    """Model for Granted Patents"""
    sl_no = models.IntegerField(null=True, blank=True, verbose_name="Serial Number")
    granted_patent_no = models.CharField(max_length=100, null=True, blank=True, verbose_name="Granted Patent No.")
    date_of_grant = models.CharField(max_length=50, null=True, blank=True, verbose_name="Date of Grant")
    inventors = models.TextField(null=True, blank=True, verbose_name="Inventor(s)/Faculty/Student")
    title = models.TextField(null=True, blank=True, verbose_name="Title of Patent")
    application_number = models.CharField(max_length=100, null=True, blank=True, verbose_name="Application Number")
    date_of_publication = models.CharField(max_length=50, null=True, blank=True, verbose_name="Date of Publication")
    filing_institute = models.TextField(null=True, blank=True, verbose_name="Patent Filing Institute/Individual(s)")
    abstract = models.TextField(null=True, blank=True, verbose_name="Abstract")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'patents_granted'
        ordering = ['-date_of_grant', '-sl_no']
        verbose_name = 'Patent (Granted)'
        verbose_name_plural = 'Patents (Granted)'
    
    def __str__(self):
        return f"{self.granted_patent_no} - {self.title[:50] if self.title else 'N/A'}"
