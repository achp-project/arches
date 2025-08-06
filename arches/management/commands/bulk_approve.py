from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    """
    Commands for managing the loading and running of packages in Arches

    """

    def add_arguments(self, parser):
        parser.add_argument(
            "-u", "--user_id", type=int, help="The ID of the user to approve edits for"
        )

    def handle(self, *args, **options):
        user_id = options.get("user_id")
