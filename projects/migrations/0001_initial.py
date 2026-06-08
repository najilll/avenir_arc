# Generated migration for Avenir projects app

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
                ('order', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'Categories',
                'ordering': ['order', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True)),
                ('location', models.CharField(max_length=200)),
                ('year', models.PositiveIntegerField()),
                ('area_sqm', models.PositiveIntegerField(blank=True, help_text='Total floor area in m²', null=True)),
                ('status', models.CharField(choices=[('completed', 'Completed'), ('ongoing', 'Ongoing'), ('concept', 'Concept')], default='completed', max_length=20)),
                ('is_featured', models.BooleanField(default=False)),
                ('is_published', models.BooleanField(default=True)),
                ('short_desc', models.CharField(help_text='One-line description for cards', max_length=300)),
                ('long_desc', models.TextField(blank=True, help_text='Full project description')),
                ('tags', models.CharField(blank=True, help_text='Comma-separated: laterite, concrete, …', max_length=300)),
                ('cover_image', models.ImageField(blank=True, null=True, upload_to='projects/covers/')),
                ('accent_color', models.CharField(default='#c42e28', help_text='Hex colour for SVG placeholder', max_length=7)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='projects', to='projects.projectcategory')),
            ],
            options={
                'ordering': ['-year', '-is_featured', 'title'],
            },
        ),
        migrations.CreateModel(
            name='ProjectImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='projects/gallery/')),
                ('caption', models.CharField(blank=True, max_length=200)),
                ('order', models.PositiveIntegerField(default=0)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gallery', to='projects.project')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
    ]
