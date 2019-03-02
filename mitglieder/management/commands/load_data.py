from django.core.management.base import BaseCommand
from mitglieder.importfunctions import import_olddb, import_abodb


class Command(BaseCommand):
    help = 'Damit werden die Daten aus der alten Datenbank eingelesen.'

    def handle(self, *args, **kwargs):
        self.stdout.write('Daten werden eingelesen')
        import_olddb()
        import_abodb()
        self.stdout.write('Einlesen erfolgreich')