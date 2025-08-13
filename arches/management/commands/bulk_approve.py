from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from arches.app.utils.bulkupload import (
    user_has_provisional_edits,
    approve_all_provisional_edits_for_user,
)


class Command(BaseCommand):
    """
    Approves all provisional edits for a specified user.

    Provide the user IDs with the --user_ids argument to approve all their provisional edits.
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "-u",
            "--user_ids",
            type=int,
            nargs="+",
            help="One or more user IDs to approve edits for (separate by space)",
        )

    def handle(self, *args, **options):
        user_ids = options.get("user_ids")

        if not user_ids:
            raise CommandError("You must provide at least one user_id argument.")

        User = get_user_model()
        for user_id in user_ids:
            if not User.objects.filter(pk=user_id).exists():
                self.stdout.write(
                    self.style.ERROR(f"User with ID {user_id} does not exist.")
                )
                continue
            if not user_has_provisional_edits(user_id):
                self.stdout.write(
                    self.style.NOTICE(
                        f"No provisional edits found for user ID {user_id}."
                    )
                )
                continue

            approve_all_provisional_edits_for_user(user_id)
            self.stdout.write(
                self.style.SUCCESS(
                    f"All provisional edits for user ID {user_id} have been approved."
                )
            )
