import os

import pytest
import join as j


def test_load_csv():
    name = 'tests/address.csv'
    pk = 'Id'
    h, d = j.loadCSV(name, pk)
    assert (h == ['Id,PersonId,Name'])
    expected_data = [['1,    20, "Las Vegas"'], ['2, 200, "Jerusalem"']]
    assert (d == expected_data)


def test_load_csv_with_mets():
    address_file = 'tests/address.csv'
    addressPk = 'PersonId'
    header, data, addressPkIndex = j.metaLoadCSVFile(address_file, addressPk)

    address_file = 'tests/names.csv'
    addressPk = 'PersonId'
    header, data, addressPkIndex = j.metaLoadCSVFile(address_file, addressPk)


def test_csv_with_meta_address():
    name = 'tests/address.csv'
    pk = 'PersonId'
    header, data, pkIndex = j.metaLoadCSVFile(name, pk)
    assert (header == ['Id', 'PersonId', 'Name'])
    expected_data = [['1', '20', 'Las Vegas'],
                     ['2', '200', 'Jerusalem']
                     ]
    assert (data == expected_data)
    assert (pkIndex == 1)
    return header, data, pkIndex


def test_csv_with_meta_names():
    name = 'tests/names.csv'
    pk = 'Id'
    header, data, pkIndex = j.metaLoadCSVFile(name, pk)
    assert (header == ['Id', 'Name', 'Lastname'])

    expected_data = [['1', 'Joe', 'Shmoe'],
                     ['200', 'Garry', 'Goldenberg'],
                     ['22', 'Andy', 'Kopper']]
    assert (data == expected_data)
    assert (pkIndex == 0)
    return header, data, pkIndex


def test_csv_with_meta_names_bad_pk_raises_ValueException():
    with pytest.raises(ValueError):
        name = 'tests/names.csv'
        pk = 'PersonId'
        header, data, pkIndex = j.metaLoadCSVFile(name, pk)


def test_inner_join():
    addr_header, addr_data, addr_pkIndex = test_csv_with_meta_address()
    names_header, names_data, names_pkIndex = test_csv_with_meta_names()

    output ='temp.csv'

    j.doJoin(j.INNER_JOIN,
             addr_data,
             addr_header,
             addr_pkIndex,
             names_data,
             names_header,
             names_pkIndex,
             output)

    header_actual, data_actual, pkindex  = j.metaLoadCSVFile(output, 'PersonId')
    assert (header_actual ==['Id', 'PersonId', 'Name', 'Id', 'Name', 'Lastname'])
    assert (data_actual == [['2', '200', 'Jerusalem', '200', 'Garry', 'Goldenberg']])
    assert (pkindex == 1)


def test_full_join():
    addr_header, addr_data, addr_pkIndex = test_csv_with_meta_address()
    names_header, names_data, names_pkIndex = test_csv_with_meta_names()
    output ='temp.csv'
    if os.path.exists(output):
        os.remove(output)

    j.doJoin(j.FULL_JOIN,
             addr_data,
             addr_header,
             addr_pkIndex,
             names_data,
             names_header,
             names_pkIndex,
             output)

    data_actual = j.loadCSV(output)
    expected = [['Id,PersonId,Name,Id,Name,Lastname'],
 ['2,200,Jerusalem,200,Garry,Goldenberg'],
 ['1,20,Las Vegas,null,null,null'],
 ['null,null,null,22,Andy,Kopper'],
 ['null,null,null,1,Joe,Shmoe']]
    s = set()
    for row in expected:
        s.add(str(row))

    assert(len(s) == len(expected))

    for row in data_actual:
        assert (str(row) in s)


def test_left_join():
    addr_header, addr_data, addr_pkIndex = test_csv_with_meta_address()
    names_header, names_data, names_pkIndex = test_csv_with_meta_names()
    output = 'temp.csv'
    if os.path.exists(output):
        os.remove(output)

    j.doJoin(j.LEFT_JOIN,
             addr_data,
             addr_header,
             addr_pkIndex,
             names_data,
             names_header,
             names_pkIndex,
             output)

    data_actual = j.loadCSV(output)
    expected = [['Id,PersonId,Name,Id,Name,Lastname'],
 ['1,20,Las Vegas,null,null,null'],
 ['2,200,Jerusalem,200,Garry,Goldenberg']]
    assert (  data_actual == expected)



def test_right_join():
    addr_header, addr_data, addr_pkIndex = test_csv_with_meta_address()
    names_header, names_data, names_pkIndex = test_csv_with_meta_names()
    output = 'temp.csv'
    if os.path.exists(output):
        os.remove(output)

    j.doJoin(j.RIGHT_JOIN,
             addr_data,
             addr_header,
             addr_pkIndex,
             names_data,
             names_header,
             names_pkIndex,
             output)

    data_actual = j.loadCSV(output)
    expected = [['Id,PersonId,Name,Id,Name,Lastname'],
 ['null,null,null,1,Joe,Shmoe'],
 ['2,200,Jerusalem,200,Garry,Goldenberg'],
 ['null,null,null,22,Andy,Kopper']]

    assert (expected == data_actual)