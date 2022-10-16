import abc


class BaseJoin(abc.ABC):
    @abc.abstractmethod
    def join(self, left_csv, right_csv):
        pass


class LeftJoin(BaseJoin):
    def join(self, left_csv, right_csv):
        output_rows = []
        for leftRow in left_csv.body:
            leftRowPK = leftRow[left_csv.primary_key_index]
            rightRow = None
            if leftRowPK in right_csv.map_primary_key:
                rightRow = right_csv.body[right_csv.map_primary_key[leftRowPK]]
            else:
                rightRow = ["null"] * len(right_csv.header)

            output_rows.append(leftRow + rightRow)
        return output_rows


class RightJoin(BaseJoin):
    def join(self, left_csv, right_csv):
        output_rows = []
        for rightRow in right_csv.body:
            rightRowPK = rightRow[right_csv.primary_key_index]
            leftRow = None
            if rightRowPK in left_csv.map_primary_key:
                leftRow = left_csv.body[left_csv.map_primary_key[rightRowPK]]
            else:
                leftRow = ["null"] * len(left_csv.header)

            output_rows.append(leftRow + rightRow)
        return output_rows


class InnerJoin(BaseJoin):
    def join(self, left_csv, right_csv):
        leftKeySet = set(left_csv.map_primary_key.keys())
        rightKeySet = set(right_csv.map_primary_key.keys())

        newKeys = leftKeySet & rightKeySet

        output_rows = []
        for keyVal in newKeys:
            leftRow = left_csv.body[left_csv.map_primary_key[keyVal]]
            rightRow = right_csv.body[right_csv.map_primary_key[keyVal]]

            output_rows.append(leftRow + rightRow)
        return output_rows


class FullJoin(BaseJoin):
    def join(self, left_csv, right_csv):
        
        leftKeySet = set(left_csv.map_primary_key.keys())
        rightKeySet = set(right_csv.map_primary_key.keys())

        newKeys = leftKeySet | rightKeySet

        output_rows = []
        for keyVal in newKeys:
            leftRow = None
            if keyVal in left_csv.map_primary_key:
                leftRow = left_csv.body[left_csv.map_primary_key[keyVal]]
            else:
                leftRow = ["null"] * len(left_csv.header)

            rightRow = None
            if keyVal in right_csv.map_primary_key:
                rightRow = right_csv.body[right_csv.map_primary_key[keyVal]]
            else:
                rightRow = ["null"] * len(right_csv.header)

            output_rows.append(leftRow + rightRow)

        return output_rows


class JoinFactory:

    def join_strategy(self):
        



