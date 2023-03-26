# Generated by Django 4.1.7 on 2023-03-26 17:03

from django.db import migrations


def add_more_pet_types(apps, schema_editor):
    PetType = apps.get_model("accounts", "PetType")
    types = [
        "Mix Breed Dog",
        "Cat",
        "Fish",
        "Bird",
        "Reptile",
        "Rodent",
        "Horse",
        "Other",
    ]

    types_to_create = []
    for t in types:
        types_to_create.append(PetType(name=t.title()))

    PetType.objects.bulk_create(types_to_create)


class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0020_pet'),
    ]

    operations = [
        migrations.RunPython(add_more_pet_types),
    ]