from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.apps import apps

class Command(BaseCommand):
    help = 'Sets up default groups and permissions for the application'

    def handle(self, *args, **options):
        groups_permissions = {
            'Viewers': [
                'can_view_book',
                'can_view_author',
                'can_view_library',
                'can_view_user',
            ],
            'Editors': [
                'can_view_book', 'can_create_book', 'can_edit_book',
                'can_view_author', 'can_create_author', 'can_edit_author',
                'can_view_library', 'can_edit_library',
                'can_view_user',
            ],
            'Admins': [
                'can_view_book', 'can_create_book', 'can_edit_book', 'can_delete_book',
                'can_view_author', 'can_create_author', 'can_edit_author', 'can_delete_author',
                'can_view_library', 'can_create_library', 'can_edit_library', 'can_delete_library',
                'can_view_librarian', 'can_create_librarian', 'can_edit_librarian', 'can_delete_librarian',
                'can_view_user', 'can_manage_user',
            ],
        }

        app_models = apps.get_app_config('users').get_models()
        
        created_groups = []
        assigned_permissions = 0

        for group_name, permission_codenames in groups_permissions.items():
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created group: {group_name}')
                )
            created_groups.append(group_name)

            group.permissions.clear()

            for codename in permission_codenames:
                try:
                    permission = None
                    for model in app_models:
                        content_type = ContentType.objects.get_for_model(model)
                        try:
                            permission = Permission.objects.get(
                                codename=codename,
                                content_type=content_type
                            )
                            break
                        except Permission.DoesNotExist:
                            continue
                    
                    if permission:
                        group.permissions.add(permission)
                        assigned_permissions += 1
                        self.stdout.write(
                            self.style.SUCCESS(f'  - Added {codename} to {group_name}')
                        )
                    else:
                        self.stdout.write(
                            self.style.WARNING(f'  - Permission not found: {codename}')
                        )
                        
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'  - Error adding {codename}: {str(e)}')
                    )

        self.stdout.write(
            self.style.SUCCESS(
                f'\nSuccessfully set up {len(created_groups)} groups '
                f'with {assigned_permissions} total permissions assigned.'
            )
        )
        
        self.stdout.write('\nGroup Permissions Summary:')
        self.stdout.write('=' * 50)
        
        for group in Group.objects.all():
            self.stdout.write(f'\n{group.name}:')
            permissions = group.permissions.all()
            if permissions:
                for perm in permissions:
                    self.stdout.write(f'  - {perm.codename}')
            else:
                self.stdout.write('  - No permissions assigned')
