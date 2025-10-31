from django.core.management.base import BaseCommand
from backend.mitgliederverwaltung.mitglieder.management.importfunctions import import_olddb, import_abodb
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Damit werden die Daten aus der alten Datenbank eingelesen.'

    def handle(self, *args, **kwargs):
        self.stdout.write('Daten werden eingelesen')
        # import_olddb()
        import_abodb()
        self.stdout.write('Einlesen erfolgreich')
        u,c = User.objects.get_or_create(username='bipo')
        u.save()
        u.is_superuser = True
        u.set_password('bipo')
        u.save()
        self.stdout.write('SuperUser bipo wurde angelegt')
