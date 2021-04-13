import argparse
import json
import sys


def missing_levels(nesting_levels, sample_data):
    ''' Returns a list of dicts not in nesting levels '''
    return [{key: sample_data[key]} for key in sample_data if key not in nesting_levels]

def parse_json(input_data, nesting_levels):
    ''' Returns a list of dicts not in nesting levels '''

    if len(input_data) < 1:
        sys.stderr.write("The input json is empty")
        sys.stdout.write("\n")
        return False

    nlevels = [i.lower() for i in nesting_levels]   # convert nesting levels to lowercase

    dict_keys = [i.lower() for i in input_data[0]]  # convert input json keys to lowercase

    # check if the nesting values are present in the keys of input json
    result = all(x in dict_keys for x in nlevels)

    if result:
        output = {}
        temp = output

        # get unique nesting levels to prevent multiple identical values
        nlevels = list(dict.fromkeys(nlevels))

        for data in input_data:

            # convert the keys to lowercase
            data = {k.lower(): v for k, v in data.items()}
            for i,level in enumerate(nlevels):
                if i + 1 < len(nlevels):
                    if data[level] not in temp:
                        temp[data[level]] = {}
                    temp = temp[data[level]]
                else:
                    temp[data[level]] = missing_levels(nlevels, data)
            temp = output

        write_output(result, output)
        return output

def read_input():
    ''' Read input from stdin '''

    input_text = ''
    for line in sys.stdin.readlines():
        input_text += line

    # return a json array
    return json.loads(input_text)

def write_output(result, output):
    if result:
        sys.stdout.write(json.dumps(output))
        sys.stdout.write("\n")
        # return output
    else:
        sys.stderr.write("nlevels must be one of the keys in the json array")
        sys.stdout.write("\n")
        return False

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Json Parser Application')

    parser.add_argument("keys",
                        type=str,
                        nargs='+',
                        help="Enter one or space separated keys from input json ")
    args = parser.parse_args()

    parse_json(read_input(), args.keys)
