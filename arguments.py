class Arguments:

    def __init__(self, args):
        self.__verbose = args.verbose
        self.__left_file_name = args.left_file_name
        self.__left_primary_key = args.left_primary_key
        self.__right_file_name = args.right_file_name
        self.__right_primary_key = args.right_primary_key
        self.__output_file_name = args.output_file_name
        self.__join_type = args.join_type

    @property
    def verbose(self):
        return self.__verbose

    @property
    def left_file_name(self):
        return self.__left_file_name

    @property
    def left_primary_key(self):
        return self.__left_primary_key

    @property
    def right_file_name(self):
        return self.__right_file_name

    @property
    def right_primary_key(self):
        return self.__right_primary_key

    @property
    def output_file_name(self):
        return self.__output_file_name

    @property
    def join_type(self):
        return self.__join_type