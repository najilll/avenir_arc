"""
python manage.py seed_projects
Seeds the database with 13 sample Avenir projects.
"""
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from projects.models import Project, ProjectCategory

SAMPLE = [
    {
        'title':'The Laterite House','category':'Residential','location':'Thiruvananthapuram, Kerala',
        'year':2024,'area_sqm':380,'status':'completed','is_featured':True,
        'short_desc':'Kerala contemporary — laterite screen, pitched tile roof, timber entry, shaded carport.',
        'long_desc':'A 380 m² residence responding to the backwaters through a full-height glazed living façade. Locally quarried laterite, terracotta roof tiles and reclaimed teak frame a series of pavilion-like volumes around a central courtyard.',
        'tags':'laterite,pitched roof,courtyard,timber,Kerala vernacular',
        'accent_color':'#9c4a28',
        'sketchfab_id':'70ab4f4164b54afbad87f174f8b285c1',
        'sketchfab_title':'Duplex House',
    },
    {
        'title':'Skyline Villa','category':'Residential','location':'Kochi, Kerala',
        'year':2023,'area_sqm':520,'status':'completed','is_featured':True,
        'short_desc':'Contemporary hilltop villa with panoramic harbour views and cantilevered infinity pool.',
        'tags':'concrete,glass,pool,contemporary,waterfront','accent_color':'#2c6e8a',
    },
    {
        'title':'Garden Bungalow','category':'Residential','location':'Thrissur, Kerala',
        'year':2023,'area_sqm':260,'status':'completed','is_featured':False,
        'short_desc':'Low-rise bungalow weaving landscape into every room through a series of pocket gardens.',
        'tags':'landscape,low-rise,natural ventilation','accent_color':'#4a7838',
    },
    {
        'title':'Cascade House','category':'Residential','location':'Munnar, Kerala',
        'year':2024,'area_sqm':310,'status':'ongoing','is_featured':False,
        'short_desc':'A terraced residence stepping down a 30° hillside in the tea estates.',
        'tags':'hillside,terraced,stone,tea estate','accent_color':'#5a6e50',
    },
    {
        'title':'Loft Office Campus','category':'Commercial','location':'Kozhikode, Kerala',
        'year':2024,'area_sqm':1200,'status':'completed','is_featured':True,
        'short_desc':'1200 m² creative campus — exposed rib-concrete and reclaimed teak for a tech start-up cluster.',
        'tags':'exposed concrete,teak,loft,creative campus','accent_color':'#3d3028',
    },
    {
        'title':'Harbor View Hotel','category':'Commercial','location':'Kochi, Kerala',
        'year':2023,'area_sqm':3400,'status':'completed','is_featured':False,
        'short_desc':'48-room boutique hotel on Mattancherry Waterfront. Heritage warehouse adaptive reuse.',
        'tags':'adaptive reuse,heritage,hospitality,waterfront','accent_color':'#8a6a28',
    },
    {
        'title':'Tech Park Phase II','category':'Commercial','location':'Technopark, Trivandrum',
        'year':2025,'area_sqm':8600,'status':'ongoing','is_featured':False,
        'short_desc':'Sustainable IT campus targeting LEED Platinum — passive cooling, solar canopy and bioswales.',
        'tags':'LEED,passive cooling,solar,sustainable,IT campus','accent_color':'#286e8a',
    },
    {
        'title':'Arts Pavilion','category':'Cultural','location':'Munnar, Kerala',
        'year':2023,'area_sqm':420,'status':'completed','is_featured':True,
        'short_desc':'Open-air cultural pavilion — steel and bamboo hybrid in the Munnar tea estates.',
        'tags':'bamboo,steel,pavilion,open-air,cultural','accent_color':'#4a7060',
    },
    {
        'title':'Community Library','category':'Cultural','location':'Alappuzha, Kerala',
        'year':2022,'area_sqm':680,'status':'completed','is_featured':False,
        'short_desc':'A lakeside reading room with floating shelves and a roof that dissolves into the backwater sky.',
        'tags':'library,lakeside,timber,community,backwaters','accent_color':'#5a4838',
    },
    {
        'title':'Net-Zero Farmhouse','category':'Sustainable','location':'Wayanad, Kerala',
        'year':2024,'area_sqm':190,'status':'completed','is_featured':True,
        'short_desc':'Fully off-grid farmhouse — rammed earth walls, rainwater harvesting, solar and grey-water recycling.',
        'tags':'rammed earth,off-grid,solar,rainwater,net-zero','accent_color':'#7a6838',
    },
    {
        'title':'Passive School','category':'Sustainable','location':'Palakkad, Kerala',
        'year':2023,'area_sqm':1800,'status':'completed','is_featured':False,
        'short_desc':'Passive-house primary school with natural cross-ventilation and photovoltaic shading canopy.',
        'tags':'passive house,school,PV,ventilation,education','accent_color':'#4a7848',
    },
    {
        'title':'Studio Loft Interior','category':'Interior','location':'Kochi, Kerala',
        'year':2024,'area_sqm':140,'status':'completed','is_featured':False,
        'short_desc':'Photographer\'s live-work loft — polished concrete, birch ply modules and darkroom feature wall.',
        'tags':'loft,concrete,birch ply,live-work,photography','accent_color':'#5a5048',
    },
    {
        'title':'Restaurant Interiors','category':'Interior','location':'Thrissur, Kerala',
        'year':2023,'area_sqm':320,'status':'completed','is_featured':False,
        'short_desc':'Fine-dining restaurant celebrating Kerala materials — woven cane screens, jackwood tables, clay finishes.',
        'tags':'cane,jackwood,clay,restaurant,hospitality interior','accent_color':'#9c6028',
    },
]

CATS = [
    ('Residential','residential',1),('Commercial','commercial',2),
    ('Cultural','cultural',3),('Sustainable','sustainable',4),
    ('Interior','interior',5),('Landscape','landscape',6),
]

class Command(BaseCommand):
    help = 'Seed sample Avenir projects'

    def handle(self, *args, **options):
        cats = {}
        for name, slug, order in CATS:
            cat, _ = ProjectCategory.objects.get_or_create(slug=slug, defaults={'name':name,'order':order})
            cats[name] = cat
            self.stdout.write(f'  Category: {name}')

        created = 0
        for data in SAMPLE:
            cat_name = data.pop('category')
            slug = slugify(data['title'])
            if not Project.objects.filter(slug=slug).exists():
                Project.objects.create(
                    slug=slug,
                    category=cats.get(cat_name),
                    long_desc=data.pop('long_desc',''),
                    sketchfab_id=data.pop('sketchfab_id',''),
                    sketchfab_title=data.pop('sketchfab_title',''),
                    **data
                )
                created += 1
                self.stdout.write(self.style.SUCCESS(f'  Created: {data["title"]}'))
            else:
                # pop extras to avoid duplicate error
                data.pop('long_desc',''); data.pop('sketchfab_id',''); data.pop('sketchfab_title','')
                self.stdout.write(f'  Exists:  {data["title"]}')

        self.stdout.write(self.style.SUCCESS(f'\nDone — {created} new projects created.'))
