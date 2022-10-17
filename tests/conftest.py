from pathlib import Path

import pytest

from join import Main
from arguments import Arguments


@pytest.fixture
def resources():
    return Path(__file__).parent / 'resources'


@pytest.fixture
def csv_path(resources):

    def wrapper(csv_name):
        return str(resources / f'{csv_name}.csv')

    return wrapper


@pytest.fixture
def arguments(csv_path):

    def wrapper(join_strategy):
        class ArgumentsMock:
            def __init__(self):
                self.verbose = False
                self.left_file_name = csv_path('left')
                self.left_primary_key = 'a'
                self.right_file_name = csv_path('right')
                self.right_primary_key = 'm'
                self.output_file_name = 'output.csv'
                self.join_strategy = join_strategy

        return Arguments(ArgumentsMock())
    
    return wrapper


@pytest.fixture
def main():
    return Main()
