from django.contrib import admin
from .models import Project, ProjectCategory, ProjectImage, LeadEnquiry


class ProjectImageInline(admin.TabularInline):
    model  = ProjectImage
    extra  = 2
    fields = ('image', 'caption', 'order')


@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display        = ('name', 'slug', 'order', 'project_count')
    prepopulated_fields = {'slug': ('name',)}

    def project_count(self, obj):
        return obj.projects.count()
    project_count.short_description = 'Projects'


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display        = ('title', 'category', 'location', 'year',
                           'status', 'is_featured', 'is_published')
    list_filter         = ('status', 'is_featured', 'is_published', 'category', 'year')
    search_fields       = ('title', 'location', 'short_desc', 'tags')
    prepopulated_fields = {'slug': ('title',)}
    list_editable       = ('is_featured', 'is_published', 'status')
    ordering            = ('-year', '-is_featured')
    inlines             = [ProjectImageInline]
    fieldsets = (
        ('Identity',  {'fields': ('title', 'slug', 'category', 'status', 'is_featured', 'is_published')}),
        ('Details',   {'fields': ('location', 'year', 'area_sqm', 'tags')}),
        ('Content',   {'fields': ('short_desc', 'long_desc')}),
        ('Media',     {'fields': ('cover_image', 'accent_color')}),
        ('3D Model',  {'fields': ('sketchfab_id', 'sketchfab_title'),
                       'description': 'Paste the Sketchfab model ID to show this project in the 3D section.'}),
    )


@admin.register(LeadEnquiry)
class LeadEnquiryAdmin(admin.ModelAdmin):
    list_display  = ('full_name', 'email', 'phone', 'project_type',
                     'location', 'submitted_at', 'is_read')
    list_filter   = ('project_type', 'is_read', 'submitted_at')
    search_fields = ('full_name', 'email', 'phone', 'location', 'message')
    list_editable = ('is_read',)
    readonly_fields = ('submitted_at', 'ip_address')
    ordering      = ('-submitted_at',)
    fieldsets = (
        ('Contact',  {'fields': ('full_name', 'email', 'phone')}),
        ('Project',  {'fields': ('project_type', 'location', 'message')}),
        ('Meta',     {'fields': ('submitted_at', 'ip_address', 'is_read')}),
    )
