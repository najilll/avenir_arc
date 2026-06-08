from django.db import models
from django.utils import timezone


class ProjectCategory(models.Model):
    name  = models.CharField(max_length=100)
    slug  = models.SlugField(unique=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Project(models.Model):
    STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('ongoing',   'Ongoing'),
        ('concept',   'Concept'),
    ]

    title        = models.CharField(max_length=200)
    slug         = models.SlugField(unique=True)
    category     = models.ForeignKey(ProjectCategory, on_delete=models.SET_NULL,
                                     null=True, blank=True, related_name='projects')
    location     = models.CharField(max_length=200)
    year         = models.PositiveIntegerField()
    area_sqm     = models.PositiveIntegerField(null=True, blank=True, help_text='Total floor area in m²')
    status       = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed')
    is_featured  = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    short_desc   = models.CharField(max_length=300)
    long_desc    = models.TextField(blank=True)
    tags         = models.CharField(max_length=300, blank=True, help_text='Comma-separated')
    cover_image  = models.ImageField(upload_to='projects/covers/', blank=True, null=True)
    accent_color = models.CharField(max_length=7, default='#c42e28')
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    # Sketchfab / 3D embed
    sketchfab_id = models.CharField(
        max_length=200, blank=True,
        help_text='Sketchfab model ID (e.g. 70ab4f4164b54afbad87f174f8b285c1)'
    )
    sketchfab_title = models.CharField(max_length=200, blank=True,
                                       help_text='Display name for the 3D model')

    class Meta:
        ordering = ['-year', '-is_featured', 'title']

    def __str__(self):
        return f"{self.title} ({self.year})"

    def get_tags_list(self):
        return [t.strip() for t in self.tags.split(',') if t.strip()]

    def cover_url(self):
        if self.cover_image:
            return self.cover_image.url
        return None

    def sketchfab_embed_url(self):
        if self.sketchfab_id:
            return (
                f"https://sketchfab.com/models/{self.sketchfab_id}/embed"
                "?autostart=1&ui_hint=0&ui_infos=0&ui_stop=0"
                "&ui_inspector=0&ui_watermark=0&ui_ar=0&ui_help=0"
                "&ui_settings=0&ui_vr=0&ui_fullscreen=1&preload=1&dnt=1"
            )
        return None


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='gallery')
    image   = models.ImageField(upload_to='projects/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    order   = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.project.title} — image {self.order}"


# ── Lead Enquiry ──────────────────────────────────────────────
class LeadEnquiry(models.Model):
    PROJECT_TYPE_CHOICES = [
        ('residential',  'Residential Design'),
        ('commercial',   'Commercial Project'),
        ('interior',     'Interior Design'),
        ('landscape',    'Landscape Design'),
        ('renovation',   'Renovation'),
        ('consultation', 'Consultation'),
        ('other',        'Other'),
    ]

    full_name    = models.CharField(max_length=200)
    email        = models.EmailField()
    phone        = models.CharField(max_length=30, blank=True)
    project_type = models.CharField(max_length=50, choices=PROJECT_TYPE_CHOICES, blank=True)
    location     = models.CharField(max_length=200, blank=True)
    message      = models.TextField()
    submitted_at = models.DateTimeField(default=timezone.now)
    is_read      = models.BooleanField(default=False)
    ip_address   = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = 'Lead Enquiry'
        verbose_name_plural = 'Lead Enquiries'

    def __str__(self):
        return f"{self.full_name} — {self.project_type} — {self.submitted_at:%d %b %Y}"
