from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        # Add Sketchfab fields to Project
        migrations.AddField(
            model_name='project',
            name='sketchfab_id',
            field=models.CharField(
                blank=True, max_length=200,
                help_text='Sketchfab model ID'
            ),
        ),
        migrations.AddField(
            model_name='project',
            name='sketchfab_title',
            field=models.CharField(blank=True, max_length=200),
        ),
        # Create LeadEnquiry model
        migrations.CreateModel(
            name='LeadEnquiry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name',    models.CharField(max_length=200)),
                ('email',        models.EmailField()),
                ('phone',        models.CharField(blank=True, max_length=30)),
                ('project_type', models.CharField(blank=True, max_length=50,
                    choices=[
                        ('residential', 'Residential Design'),
                        ('commercial',  'Commercial Project'),
                        ('interior',    'Interior Design'),
                        ('landscape',   'Landscape Design'),
                        ('renovation',  'Renovation'),
                        ('consultation','Consultation'),
                        ('other',       'Other'),
                    ])),
                ('location',     models.CharField(blank=True, max_length=200)),
                ('message',      models.TextField()),
                ('submitted_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_read',      models.BooleanField(default=False)),
                ('ip_address',   models.GenericIPAddressField(blank=True, null=True)),
            ],
            options={'ordering': ['-submitted_at'], 'verbose_name': 'Lead Enquiry', 'verbose_name_plural': 'Lead Enquiries'},
        ),
    ]
