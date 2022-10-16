import csv


class CSVHandler:

    def load_rows_from_csv(self, file_name):
        with open(file_name, "r") as f:
            csv_reader = csv.reader(f)
            return [row for row in csv_reader]

    def save_in_csv(self, output_csv):
        with open(output_csv.file_name, "w") as fp:
            csvWriter = csv.writer(fp)
            csvWriter.writerow(output_csv.header)

            for row in output_csv.body:
                csvWriter.writerow(row)