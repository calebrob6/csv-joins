import abc


class BaseJoin(abc.ABC):
    """An interface for all join strategies."""

    @abc.abstractmethod
    def join(self, left_csv, right_csv):
        pass


class LeftJoin(BaseJoin):
    """Iterate through each row in the left table, try to find the matching row
    in the right table if the matching row doesn't exist, then fill with
    'null's, if it does, then copy it over.
    """

    def join(self, left_csv, right_csv):
        output_rows = []
        for left_row in left_csv.body:
            left_row_pk = left_row[left_csv.primary_key_index]
            right_row = None
            if left_row_pk in right_csv.map_primary_key:
                right_row = right_csv.body[
                    right_csv.map_primary_key[left_row_pk]
                ]
            else:
                right_row = ["null"] * len(right_csv.header)

            output_rows.append(left_row + right_row)
        return output_rows


class RightJoin(BaseJoin):
    """Similar to 'left' case."""

    def join(self, left_csv, right_csv):
        output_rows = []
        for right_row in right_csv.body:
            right_row_pk = right_row[right_csv.primary_key_index]
            left_row = None
            if right_row_pk in left_csv.map_primary_key:
                left_row = left_csv.body[left_csv.map_primary_key[right_row_pk]]
            else:
                left_row = ["null"] * len(left_csv.header)

            output_rows.append(left_row + right_row)
        return output_rows


class InnerJoin(BaseJoin):
    """This join will only write rows for primary keys in the intersection of
    the two primary key sets.
    """

    def join(self, left_csv, right_csv):
        left_key_set = set(left_csv.map_primary_key.keys())
        right_key_set = set(right_csv.map_primary_key.keys())

        new_keys = left_key_set & right_key_set

        output_rows = []
        for key_val in new_keys:
            left_row = left_csv.body[left_csv.map_primary_key[key_val]]
            right_row = right_csv.body[right_csv.map_primary_key[key_val]]

            output_rows.append(left_row + right_row)
        return output_rows


class FullJoin(BaseJoin):
    """This join will only write rows for primary keys in the union of the two
    primary key sets.
    """

    def join(self, left_csv, right_csv):
        left_key_set = set(left_csv.map_primary_key.keys())
        right_key_set = set(right_csv.map_primary_key.keys())

        new_keys = left_key_set | right_key_set

        output_rows = []
        for key_val in new_keys:
            left_row = None
            if key_val in left_csv.map_primary_key:
                left_row = left_csv.body[left_csv.map_primary_key[key_val]]
            else:
                left_row = ["null"] * len(left_csv.header)

            right_row = None
            if key_val in right_csv.map_primary_key:
                right_row = right_csv.body[right_csv.map_primary_key[key_val]]
            else:
                right_row = ["null"] * len(right_csv.header)

            output_rows.append(left_row + right_row)

        return output_rows


class JoinFactory:
    def join_strategy(self, strategy):
        match strategy:
            case "left":
                return LeftJoin()
            case "right":
                return RightJoin()
            case "inner":
                return InnerJoin()
            case "full":
                return FullJoin()
            case _:
                raise Exception("This shouldn't happen")
