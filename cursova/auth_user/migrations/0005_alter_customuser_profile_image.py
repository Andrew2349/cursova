# Generated by Django 5.1.3 on 2024-12-11 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_user', '0004_alter_customuser_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile_image',
            field=models.ImageField(default='profile_images/user.png', upload_to='profile_images/'),
        ),
    ]
