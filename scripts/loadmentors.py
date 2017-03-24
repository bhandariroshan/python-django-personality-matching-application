from django.core.management.base import BaseCommand
from sciencerunway.views import load_mentors


class Command(BaseCommand):
    args = ''
    help = 'Update fee report of students'

    def handle(self, *args, **options):
        # do something here
        load_mentors()
        print('Success')