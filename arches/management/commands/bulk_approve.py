from django.core.management.base import BaseCommand, CommandError
from arches.app.utils.bulkupload import (
    user_has_provisional_edits,
    approve_all_provisional_edits_for_user,
)


class Command(BaseCommand):
    """
    Approves all provisional edits for a specified user.

    Provide the user ID with the --user_id argument to approve all their provisional edits.
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "-u", "--user_id", type=int, help="The ID of the user to approve edits for"
        )

    def handle(self, *args, **options):
        user_id = options.get("user_id")

        if not user_id:
            raise CommandError("You must provide a user_id argument.")

        if not user_has_provisional_edits(user_id):
            self.stdout.write(
                self.style.SUCCESS(f"No provisional edits found for user ID {user_id}.")
            )
            return

        approve_all_provisional_edits_for_user(user_id)
        self.stdout.write(
            self.style.SUCCESS(
                f"All provisional edits for user ID {user_id} have been approved."
            )
        )
