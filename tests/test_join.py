import pytest


def test_left_join(main, arguments):
    args = arguments('left')

    left_csv, right_csv = main.create_left_and_right_instances(args)
    output_csv = main.join_csvs(args, left_csv, right_csv)

    header = ['a', 'b', 'c', 'd', 'e', 'l', 'm', 'n', 'o', 'p']
    body = [
        ['97', '38', '15', '7', '23', 'null', 'null', 'null', 'null', 'null'],
        ['8', '41', '15', '85', '50', 'null', 'null', 'null', 'null', 'null'],
        ['83', '94', '10', '84', '21', '16', '83', '53', '41', '75'],
        ['43', '29', '68', '87', '4', 'null', 'null', 'null', 'null', 'null'],
        ['85', '54', '37', '7', '24', 'null', 'null', 'null', 'null', 'null'],
    ]
    assert output_csv.header == header
    assert output_csv.body == body
    assert output_csv.file_name == args.output_file_name


def test_right_join(main, arguments):
    args = arguments('right')

    left_csv, right_csv = main.create_left_and_right_instances(args)
    output_csv = main.join_csvs(args, left_csv, right_csv)

    header = ['a', 'b', 'c', 'd', 'e', 'l', 'm', 'n', 'o', 'p']
    body = [
        ['null', 'null', 'null', 'null', 'null', '12', '18', '9', '54', '76'],
        ['null', 'null', 'null', 'null', 'null', '24', '92', '61', '42', '9'],
        ['null', 'null', 'null', 'null', 'null', '26', '72', '62', '14', '23'],
        ['null', 'null', 'null', 'null', 'null', '53', '61', '49', '92', '26'],
        ['83', '94', '10','84', '21', '16', '83', '53', '41', '75'],
    ]
    assert output_csv.header == header
    assert output_csv.body == body
    assert output_csv.file_name == args.output_file_name


def test_inner_join(main, arguments):
    args = arguments('inner')

    left_csv, right_csv = main.create_left_and_right_instances(args)
    output_csv = main.join_csvs(args, left_csv, right_csv)

    header = ['a', 'b', 'c', 'd', 'e', 'l', 'm', 'n', 'o', 'p']
    body = [
        ['83', '94', '10', '84', '21', '16', '83', '53', '41', '75'],
    ]
    assert output_csv.header == header
    assert output_csv.body == body
    assert output_csv.file_name == args.output_file_name


@pytest.mark.skip(
    "Join return the same elements with a different order each time"
)
def test_full_join(main, arguments):
    args = arguments('full')

    left_csv, right_csv = main.create_left_and_right_instances(args)
    output_csv = main.join_csvs(args, left_csv, right_csv)

    header = ['a', 'b', 'c', 'd', 'e', 'l', 'm', 'n', 'o', 'p']
    body = [
        ['null', 'null', 'null', 'null', 'null', '12', '18', '9', '54', '76'],
        ['43', '29', '68', '87', '4', 'null', 'null', 'null', 'null', 'null'],
        ['null', 'null', 'null', 'null', 'null', '53', '61', '49', '92', '26'],
        ['null', 'null', 'null', 'null', 'null', '26', '72', '62', '14', '23'],
        ['8', '41', '15', '85', '50', 'null', 'null', 'null', 'null', 'null'],
        ['83', '94', '10', '84', '21', '16', '83', '53', '41', '75'],
        ['null', 'null', 'null', 'null', 'null', '24', '92', '61', '42', '9'],
        ['97', '38', '15', '7', '23', 'null', 'null', 'null', 'null', 'null'],
        ['85', '54', '37', '7', '24', 'null', 'null', 'null', 'null', 'null'],
    ]
    assert output_csv.header == header
    assert output_csv.body == body
    assert output_csv.file_name == args.output_file_name


