import csv
from pathlib import Path

from django.core.management import BaseCommand, CommandError

from users.models import Team


class Command(BaseCommand):

    fieldnames_mapping = {
        'название': 'name',
        'рекрут': 'recruit',
    }

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            action="store",
            help="Specify the path to the file",
        )

    def handle(self, *args, **options):
        input_file = options["file"]
        if not input_file:
            self.stderr.write('you must add a file: --file path_to_file')
            return

        input_file = Path(input_file)

        if not input_file.exists():
            self.stderr.write(f"Can't find file: {input_file}")
            return

        if not input_file.name.endswith('csv'):
            self.stderr.write(f'Expected csv file, got: {input_file}')
            return

        self.add_teams(input_file)
        self.stdout.write('Teams success added')

    def read_csv(self, input_file: Path):
        with open(input_file, 'r') as input_f:
            data = csv.DictReader(input_f)

            if data.fieldnames != list(self.fieldnames_mapping.keys()):
                raise CommandError(f'Expected headers {self.fieldnames_mapping.keys()}, got {data.fieldnames}')
            yield from data

    def change_fieldnames(self, data: dict) -> dict:
        result = {}
        for file_header, model_field in self.fieldnames_mapping.items():
            result[model_field] = data[file_header]

        return result

    def add_teams(self, input_file: Path) -> None:
        team_objs = []
        for row in self.read_csv(input_file):
            team_objs.append(Team(**self.change_fieldnames(row)))

        Team.objects.bulk_create(team_objs)
