class CSVRows:

    def __init__(self, header, rows, primary_key, file_name):
        self.__header = header
        self.__body = rows
        self.__primary_key = primary_key
        self.__file_name = file_name
        self.__map_primary_key = self.__create_map_primary_key()

    @property
    def header(self):
        return self.__header

    @property
    def body(self):
        return self.__body

    @property
    def primary_key(self):
        return self.__primary_key

    @property
    def primary_key_index(self):
        return self.header.index(self.primary_key)

    @property
    def file_name(self):
        return self.__file_name

    @property
    def map_primary_key(self):
        return self.__map_primary_key

    def check_if_header_has_primary_key_column(self):
        if self.__header_has_primary_key_column():
            raise ValueError(
                f"Error: primary key ({self.primary_key}) not in header "
                f"line of {self.file_name}"
            )

    def check_if_all_values_in_primary_key_column_are_unique(self):
        pk_set = set()
        for row in self.body:
            if row[self.primary_key_index] in pk_set:
                raise ValueError(
                    f"Error: primary key column is not unique in "
                    f"{self.file_name} (duplicate value found: "
                    f"{row[self.primary_key_index]})"
                )
            pk_set.add(row[self.primary_key_index])

    def __create_map_primary_key(self):
        return {r[self.primary_key_index]: i for i, r in enumerate(self.body)}

    def __header_has_primary_key_column(self):
        return self.primary_key not in self.header
