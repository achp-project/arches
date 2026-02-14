from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from arches.app.utils.bulkupload import (
    user_has_provisional_edits,
    approve_all_provisional_edits_for_user,
)


class Command(BaseCommand):
    """
    Approves all provisional edits for specified users.

    This command can process users by either user IDs or usernames, with comprehensive
    validation and graceful handling of non-existent users.

    Arguments:
        --user_ids: One or more user IDs to approve edits for (separate by space)
        --user_names: One or more usernames to approve edits for (separate by space)

    Examples:
        python manage.py bulk_approve --user_ids 1 2 3
        python manage.py bulk_approve --user_names john_doe jane_smith admin
    """

    def add_arguments(self, parser):
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument(
            "-u",
            "--user_ids",
            type=int,
            nargs="+",
            metavar="USER_ID",
            default=[],
            help="One or more user IDs to approve edits for (separate by space)",
        )
        group.add_argument(
            "-n",
            "--user_names",
            type=str,
            nargs="+",
            metavar="USER_NAME",
            default=[],
            help="One or more user names to approve edits for (separate by space)",
        )

    def handle(self, *args, **options):
        user_ids = options.get("user_ids")
        user_names = options.get("user_names")

        User = get_user_model()
        if user_ids:
            existing_users = User.objects.filter(pk__in=user_ids).values_list(
                "id", flat=True
            )
            if not existing_users:
                raise CommandError(f"User(s) with ID(s) {user_ids} do(es) not exist.")
            missing_user_ids = set(user_ids) - set(existing_users)
            if missing_user_ids:
                self.stdout.write(
                    self.style.WARNING(
                        f"User(s) with ID(s) {missing_user_ids} do(es) not exist and will be skipped."
                    )
                )
            user_ids = list(existing_users)

        if user_names:
            existing_user_names_and_ids = User.objects.filter(
                username__in=user_names
            ).values("id", "username")
            if not existing_user_names_and_ids:
                raise CommandError(
                    f"User(s) with name(s) {user_names} do(es) not exist."
                )
            found_usernames = {user["username"] for user in existing_user_names_and_ids}
            missing_usernames = set(user_names) - found_usernames

            if missing_usernames:
                self.stdout.write(
                    self.style.WARNING(
                        f"User(s) with name(s) {missing_usernames} do(es) not exist and will be skipped."
                    )
                )
            user_ids = [user["id"] for user in existing_user_names_and_ids]

        for user_id in user_ids:
            if not user_has_provisional_edits(user_id):
                self.stdout.write(
                    self.style.WARNING(
                        f"No provisional edits found for user ID {user_id} or username {User.objects.filter(pk=user_id).first().username}"
                    )
                )
                continue

            approve_all_provisional_edits_for_user(user_id)
            self.stdout.write(
                self.style.SUCCESS(
                    f"All provisional edits for user ID {user_id} or username {User.objects.filter(pk=user_id).first().username} have been approved."
                )
            )
