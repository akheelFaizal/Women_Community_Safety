from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from reports.models import Report
from awareness.models import Post
from accounts.models import User

class Command(BaseCommand):
    help = 'Setup RBAC Groups and Permissions'

    def handle(self, *args, **kwargs):
        # Create Groups
        mod_group, created = Group.objects.get_or_create(name='Moderators')
        admin_group, created = Group.objects.get_or_create(name='Admins')

        # Define Permissions
        report_ct = ContentType.objects.get_for_model(Report)
        post_ct = ContentType.objects.get_for_model(Post)
        user_ct = ContentType.objects.get_for_model(User)

        # Moderator Permissions
        mod_perms = [
            Permission.objects.get(codename='view_report', content_type=report_ct),
            Permission.objects.get(codename='change_report', content_type=report_ct),
            Permission.objects.get(codename='add_post', content_type=post_ct),
            Permission.objects.get(codename='view_post', content_type=post_ct),
        ]
        mod_group.permissions.set(mod_perms)
        self.stdout.write(self.style.SUCCESS('Moderator permissions assigned.'))

        # Admin Permissions
        admin_perms = [
            # Reports
            Permission.objects.get(codename='view_report', content_type=report_ct),
            Permission.objects.get(codename='change_report', content_type=report_ct),
            Permission.objects.get(codename='delete_report', content_type=report_ct),
            # Content
            Permission.objects.get(codename='add_post', content_type=post_ct),
            Permission.objects.get(codename='change_post', content_type=post_ct),
            Permission.objects.get(codename='delete_post', content_type=post_ct),
            Permission.objects.get(codename='view_post', content_type=post_ct),
            # Users
            Permission.objects.get(codename='view_user', content_type=user_ct),
            Permission.objects.get(codename='change_user', content_type=user_ct),
            Permission.objects.get(codename='delete_user', content_type=user_ct),
        ]
        admin_group.permissions.set(admin_perms)
        self.stdout.write(self.style.SUCCESS('Admin permissions assigned.'))
