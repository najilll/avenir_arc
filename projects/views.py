import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.paginator import Paginator
from .models import Project, ProjectCategory, LeadEnquiry


# ── Main page ────────────────────────────────────────────────
@ensure_csrf_cookie
def index(request):
    categories = ProjectCategory.objects.all()
    # Fetch the active 3D model from DB (most-featured project with sketchfab_id)
    model_3d = (
        Project.objects
        .filter(is_published=True, sketchfab_id__isnull=False)
        .exclude(sketchfab_id='')
        .order_by('-is_featured', '-year')
        .first()
    )
    return render(request, 'projects/index.html', {
        'categories': categories,
        'model_3d':   model_3d,
    })


# ── Projects list API ────────────────────────────────────────
@require_GET
def api_projects(request):
    qs = Project.objects.filter(is_published=True).select_related('category')
    category_slug = request.GET.get('category', '').strip()
    status        = request.GET.get('status',   '').strip()
    featured      = request.GET.get('featured', '').strip()
    query         = request.GET.get('q',        '').strip()

    if category_slug: qs = qs.filter(category__slug=category_slug)
    if status:        qs = qs.filter(status=status)
    if featured == '1': qs = qs.filter(is_featured=True)
    if query:
        from django.db.models import Q
        qs = qs.filter(
            Q(title__icontains=query) |
            Q(location__icontains=query) |
            Q(short_desc__icontains=query) |
            Q(tags__icontains=query)
        )

    per_page = min(int(request.GET.get('per_page', 12)), 50)
    page_num = int(request.GET.get('page', 1))
    paginator = Paginator(qs, per_page)
    page = paginator.get_page(page_num)

    return JsonResponse({
        'projects': [{
            'id':          p.pk,
            'title':       p.title,
            'slug':        p.slug,
            'category':    p.category.name if p.category else '',
            'cat_slug':    p.category.slug if p.category else '',
            'location':    p.location,
            'year':        p.year,
            'area_sqm':    p.area_sqm,
            'status':      p.status,
            'is_featured': p.is_featured,
            'short_desc':  p.short_desc,
            'tags':        p.get_tags_list(),
            'cover_url':   p.cover_url(),
            'accent':      p.accent_color,
            'has_3d':      bool(p.sketchfab_id),
        } for p in page.object_list],
        'total':    paginator.count,
        'pages':    paginator.num_pages,
        'current':  page.number,
        'has_next': page.has_next(),
        'has_prev': page.has_previous(),
    })


# ── Project detail API ───────────────────────────────────────
@require_GET
def api_project_detail(request, slug):
    p = get_object_or_404(Project, slug=slug, is_published=True)
    return JsonResponse({
        'id':          p.pk,
        'title':       p.title,
        'slug':        p.slug,
        'category':    p.category.name if p.category else '',
        'location':    p.location,
        'year':        p.year,
        'area_sqm':    p.area_sqm,
        'status':      p.status,
        'is_featured': p.is_featured,
        'short_desc':  p.short_desc,
        'long_desc':   p.long_desc,
        'tags':        p.get_tags_list(),
        'cover_url':   p.cover_url(),
        'accent':      p.accent_color,
        'sketchfab_embed': p.sketchfab_embed_url(),
        'sketchfab_title': p.sketchfab_title,
        'gallery': [
            {'url': img.image.url, 'caption': img.caption}
            for img in p.gallery.all()
        ],
    })


# ── Categories API ───────────────────────────────────────────
@require_GET
def api_categories(request):
    return JsonResponse({'categories': [{
        'id':    c.pk,
        'name':  c.name,
        'slug':  c.slug,
        'count': c.projects.filter(is_published=True).count(),
    } for c in ProjectCategory.objects.all()]})


# ── Stats API ────────────────────────────────────────────────
@require_GET
def api_stats(request):
    qs = Project.objects.filter(is_published=True)
    years = list(qs.values_list('year', flat=True))
    return JsonResponse({
        'total':      qs.count(),
        'completed':  qs.filter(status='completed').count(),
        'ongoing':    qs.filter(status='ongoing').count(),
        'year_range': f"{min(years)} – {max(years)}" if years else "—",
    })


# ── Active 3D model API ──────────────────────────────────────
@require_GET
def api_active_3d(request):
    """Returns the currently active Sketchfab model for the 3D section."""
    p = (
        Project.objects
        .filter(is_published=True, sketchfab_id__isnull=False)
        .exclude(sketchfab_id='')
        .order_by('-is_featured', '-year')
        .first()
    )
    if not p:
        # Fallback to hardcoded Duplex model
        return JsonResponse({
            'found': False,
            'embed_url': (
                'https://sketchfab.com/models/70ab4f4164b54afbad87f174f8b285c1/embed'
                '?autostart=1&ui_hint=0&ui_infos=0&ui_stop=0&ui_inspector=0'
                '&ui_watermark=0&ui_ar=0&ui_help=0&ui_settings=0&ui_vr=0'
                '&ui_fullscreen=1&preload=1&dnt=1'
            ),
            'title':    'Duplex House',
            'location': 'Sample Model',
            'year':     2024,
            'area_sqm': None,
            'category': '',
            'slug':     '',
        })
    return JsonResponse({
        'found':     True,
        'embed_url': p.sketchfab_embed_url(),
        'title':     p.sketchfab_title or p.title,
        'location':  p.location,
        'year':      p.year,
        'area_sqm':  p.area_sqm,
        'category':  p.category.name if p.category else '',
        'slug':      p.slug,
    })


# ── Lead Enquiry API ─────────────────────────────────────────
@require_POST
def api_submit_enquiry(request):
    """
    POST /api/enquiry/
    Accepts JSON body. Returns JSON success/error.
    """
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, Exception):
        return JsonResponse({'ok': False, 'error': 'Invalid request.'}, status=400)

    # Validate required fields
    errors = {}
    full_name = (data.get('full_name') or '').strip()
    email     = (data.get('email')     or '').strip()
    message   = (data.get('message')   or '').strip()

    if not full_name:
        errors['full_name'] = 'Your name is required.'
    if not email or '@' not in email:
        errors['email'] = 'A valid email address is required.'
    if not message:
        errors['message'] = 'Please tell us about your project.'

    if errors:
        return JsonResponse({'ok': False, 'errors': errors}, status=422)

    # Get IP address
    ip = request.META.get('HTTP_X_FORWARDED_FOR')
    if ip:
        ip = ip.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')

    lead = LeadEnquiry.objects.create(
        full_name    = full_name,
        email        = email,
        phone        = (data.get('phone')        or '').strip(),
        project_type = (data.get('project_type') or '').strip(),
        location     = (data.get('location')     or '').strip(),
        message      = message,
        ip_address   = ip,
    )

    return JsonResponse({
        'ok':      True,
        'id':      lead.pk,
        'message': f"Thank you, {lead.full_name.split()[0]}! We've received your brief and will be in touch within 24 hours.",
    }, status=201)
