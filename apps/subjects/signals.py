import csv
import os
from io import StringIO

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from apps.corecode.models import SubjectClass

from .models import Subject, SubjectBulkUpload


@receiver(post_save, sender=SubjectBulkUpload)
def create_bulk_subject(sender, created, instance, *args, **kwargs):
    if created:
        opened = StringIO(instance.csv_file.read().decode())
        reading = csv.DictReader(opened, delimiter=",")
        subjects = []
        for row in reading:
            if "credit" in row and row["credit"]:
                reg = row["credit"]
                surname = row["surname"] if "surname" in row and row["surname"] else ""
                firstname = (
                    row["firstname"] if "firstname" in row and row["firstname"] else ""
                )
                online_sources = (
                    row["online_sources"]
                    if "online_sources" in row and row["online_sources"]
                    else ""
                )
                gender = (
                    (row["gender"]).lower() if "gender" in row and row["gender"] else ""
                )
                phone = (
                    row["parent_number"]
                    if "parent_number" in row and row["parent_number"]
                    else ""
                )
                address = row["address"] if "address" in row and row["address"] else ""
                current_class = (
                    row["current_class"]
                    if "current_class" in row and row["current_class"]
                    else ""
                )
                if current_class:
                    theclass, kind = SubjectClass.objects.get_or_create(
                        name=current_class
                    )

                check = Subject.objects.filter(credit=reg).exists()
                if not check:
                    subjects.append(
                        Subject(
                            credit=reg,
                            surname=surname,
                            firstname=firstname,
                            online_source=online_sources,
                            gender=gender,
                            current_class=theclass,
                            parent_mobile_number=phone,
                            address=address,
                            current_status="active",
                        )
                    )

        Subject.objects.bulk_create(subjects)
        instance.csv_file.close()
        instance.delete()


def _delete_file(path):
    """Deletes file from filesystem."""
    if os.path.isfile(path):
        os.remove(path)


@receiver(post_delete, sender=SubjectBulkUpload)
def delete_csv_file(sender, instance, *args, **kwargs):
    if instance.csv_file:
        _delete_file(instance.csv_file.path)


@receiver(post_delete, sender=Subject)
def delete_passport_on_delete(sender, instance, *args, **kwargs):
    if instance.passport:
        _delete_file(instance.passport.path)
