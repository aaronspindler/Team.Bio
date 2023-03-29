# Generated by Django 4.1.7 on 2023-03-26 16:43

from django.db import migrations


def reverse(apps, schema_editor):
    PetType = apps.get_model("accounts", "PetType")
    PetType.objects.all().delete()


def add_pet_types(apps, schema_editor):
    PetType = apps.get_model("accounts", "PetType")
    types = [
        "affenpinscher",
        "Afghan hound",
        "Airedale terrier",
        "Akita",
        "Alaskan Malamute",
        "American Staffordshire terrier",
        "American water spaniel",
        "Australian cattle dog",
        "Australian shepherd",
        "Australian terrier",
        "basenji",
        "basset hound",
        "beagle",
        "bearded collie",
        "Bedlington terrier",
        "Bernese mountain dog",
        "bichon frise",
        "black and tan coonhound",
        "bloodhound",
        "border collie",
        "border terrier",
        "borzoi",
        "Boston terrier",
        "bouvier des Flandres",
        "boxer",
        "briard",
        "Brittany",
        "Brussels griffon",
        "bull terrier",
        "bulldog",
        "bullmastiff",
        "cairn terrier",
        "Canaan dog",
        "Chesapeake Bay retriever",
        "Chihuahua",
        "Chinese crested",
        "Chinese shar-pei",
        "chow chow",
        "Clumber spaniel",
        "cocker spaniel",
        "collie",
        "curly-coated retriever",
        "dachshund",
        "Dalmatian",
        "Doberman pinscher",
        "English cocker spaniel",
        "English setter",
        "English springer spaniel",
        "English toy spaniel",
        "Eskimo dog",
        "Finnish spitz",
        "flat-coated retriever",
        "fox terrier",
        "foxhound",
        "French bulldog",
        "German shepherd",
        "German shorthaired pointer",
        "German wirehaired pointer",
        "golden retriever",
        "Gordon setter",
        "Great Dane",
        "greyhound",
        "Irish setter",
        "Irish water spaniel",
        "Irish wolfhound",
        "Jack Russell terrier",
        "Japanese spaniel",
        "keeshond",
        "Kerry blue terrier",
        "komondor",
        "kuvasz",
        "Labrador retriever",
        "Lakeland terrier",
        "Lhasa apso",
        "Maltese",
        "Manchester terrier",
        "mastiff",
        "Mexican hairless",
        "Newfoundland",
        "Norwegian elkhound",
        "Norwich terrier",
        "otterhound",
        "papillon",
        "Pekingese",
        "pointer",
        "Pomeranian",
        "poodle",
        "pug",
        "puli",
        "Rhodesian ridgeback",
        "Rottweiler",
        "Saint Bernard",
        "saluki",
        "Samoyed",
        "schipperke",
        "schnauzer",
        "Scottish deerhound",
        "Scottish terrier",
        "Sealyham terrier",
        "Shetland sheepdog",
        "shih tzu",
        "Siberian husky",
        "silky terrier",
        "Skye terrier",
        "Staffordshire bull terrier",
        "soft-coated wheaten terrier",
        "Sussex spaniel",
        "spitz",
        "Tibetan terrier",
        "vizsla",
        "Weimaraner",
        "Welsh terrier",
        "West Highland white terrier",
        "whippet",
        "Yorkshire terrier",
        "Mix Breed Dog",
        "Cat",
        "Fish",
        "Bird",
        "Reptile",
        "Rodent",
        "Horse",
        "Other",
        "Pomsky"
    ]

    types_to_create = []
    for t in types:
        types_to_create.append(PetType(name=t.title()))

    PetType.objects.bulk_create(types_to_create)


class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0018_alter_pettype_options'),
    ]

    operations = [
        migrations.RunPython(add_pet_types, reverse),
    ]
