import sys
import yaml
import math

from yamlcore import CoreLoader, CCoreLoader, CoreDumper, CCoreDumper


def check_bool(value, expected):
    if expected == 'false()' and value is False:
        return 1
    if expected == 'true()' and value is True:
        return 1
    print(value)
    print(expected)
    return 0


def check_int(value, expected):
    if (int(expected) == value):
        return 1
    print(value)
    print(expected)
    return 0


def check_float(value, expected):
    if expected == 'inf()':
        if value == math.inf:
            return 1
    elif expected == 'inf-neg()':
        if value == -math.inf:
            return 1
    elif expected == 'nan()':
        if math.isnan(value):
            return 1
    elif (float(expected) == value):
        return 1
    else:
        print(value)
        print(expected)
        return 0


def check_str(value, expected):
    if value == expected:
        return 1
    print(value)
    print(expected)
    return 0


def _fail(input, test):
    print("Input: >>" + input + "<<")
    print(test)


types = {
    'str':   [str,   check_str],
    'int':   [int,   check_int],
    'float': [float, check_float],
    'inf':   [float, check_float],
    'nan':   [float, check_float],
    'bool':  [bool,  check_bool],
}


def load_test_files(tagset):

    data_filename = "tests/data/"+tagset+".schema"
    with open(data_filename, 'rb') as file:
        tests = yaml.load(file, Loader=yaml.SafeLoader)
    return tests


def schema_test(tagset, loader, dumper):
    tests = load_test_files(tagset)

    i = 0
    fail = 0
    for i, (input, test) in enumerate(sorted(tests.items())):

        exp_type = test[0]
        data = test[1]
        exp_dump = test[2]

        # Test loading
        load_ok = 0
        try:
            doc_input = """---\n""" + input
            loaded = yaml.load(doc_input, Loader=loader)
            load_ok = 1
        except:
            print("Error:", sys.exc_info()[0], '(', sys.exc_info()[1], ')')
            fail += 1
            _fail(input, test)
        assert (load_ok)

        if exp_type == 'null':
            load_ok = 0
            if loaded is None:
                load_ok = 1
            else:
                fail += 1
                _fail(input, test)
            assert (load_ok)
        else:
            t = types[exp_type][0]
            code = types[exp_type][1]

            instance_ok = 0
            type_ok = 0
            if isinstance(loaded, t):
                instance_ok = 1
                if code(loaded, data):
                    type_ok = 1
                else:
                    fail += 1
                    print("Expected data: >>" + str(data) + "<< Got: >>" + str(loaded) + "<<")
                    _fail(input, test)
            else:
                fail += 1
                print("Expected type: >>" + exp_type + "<< Got: >>" + str(loaded) + "<<")
                _fail(input, test)
            assert (instance_ok)
            assert (type_ok)

        dump = yaml.dump(loaded, explicit_end=False, Dumper=dumper)
        # strip trailing newlines and footers
        if (dump == '...\n'):
            dump = ''
        if dump.endswith('\n...\n'):
            dump = dump[:-5]
        if dump.endswith('\n'):
            dump = dump[:-1]

        dump_ok = 0
        if dump == exp_dump:
            dump_ok = 1
        else:
            print("Compare: >>" + dump + "<< >>" + exp_dump + "<<")
            fail += 1
            _fail(input, test)
        assert (dump_ok)


def test_core_schema_py():
    schema_test('core', CoreLoader, CoreDumper)


def test_core_schema_c():
    schema_test('core', CCoreLoader, CCoreDumper)
