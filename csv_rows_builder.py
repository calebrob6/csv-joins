from csv_rows import CSVRows
from csv_handler import CSVHandler


class CSVRowsBuilder:
    def __init__(self):
        self.__csv_handler = CSVHandler()

    def build_csv_rows(self, file_name, primary_key):
        headers, *rows = self.__csv_handler.load_rows_from_csv(file_name)
        csv_rows = self.__csv_rows_instance(
            headers,
            rows,
            primary_key,
            file_name
        )
        self.__validators(csv_rows)
        return csv_rows

    def __csv_rows_instance(self, headers, rows, primary_key, file_name):
        return CSVRows(headers, rows, primary_key, file_name)

    def __validators(self, csv_rows):
        csv_rows.check_if_header_has_primary_key_column()
        csv_rows.check_if_all_values_in_primary_key_column_are_unique()