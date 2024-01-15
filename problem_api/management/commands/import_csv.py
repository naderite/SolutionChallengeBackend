import csv
from django.core.management.base import BaseCommand
from problem_api.models import Question


class Command(BaseCommand):
    help = "Import data from a CSV file"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str, help="Path to the CSV file")

    def handle(self, *args, **options):
        csv_file = options["csv_file"]

        with open(csv_file, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                Question.objects.create(
                    problem=row["Problem"],
                    rationale=row["Rationale"],
                    options=row["options"],
                    correct=row["correct"],
                    annotated_formula=row["annotated_formula"],
                    linear_formula=row["linear_formula"],
                    category=row["category"],
                    difficulty_score=row["difficulty_score"],
                )

        self.stdout.write(self.style.SUCCESS("Data imported successfully"))
