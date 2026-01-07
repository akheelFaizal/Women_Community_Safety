from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Assign a user to Moderator or Admin group'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username to assign role')
        parser.add_argument('role', type=str, choices=['moderator', 'admin'], help='Role to assign')

    def handle(self, *args, **kwargs):
        username = kwargs['username']
        role = kwargs['role']
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User "{username}" does not exist.'))
            return
        
        if role == 'moderator':
            group = Group.objects.get(name='Moderators')
            user.groups.add(group)
            self.stdout.write(self.style.SUCCESS(f'User "{username}" added to Moderators group.'))
        elif role == 'admin':
            group = Group.objects.get(name='Admins')
            user.groups.add(group)
            self.stdout.write(self.style.SUCCESS(f'User "{username}" added to Admins group.'))
