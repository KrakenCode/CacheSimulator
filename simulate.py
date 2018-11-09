#!/usr/bin/python3
import argparse
import re


# Parsing the command line

parser = argparse.ArgumentParser()
parser.add_argument('--cache_size', dest='cache_size',
                    type=int, default=8388608,
                    help='Size of the cache in bits, default is 8388608 (1MB)')

parser.add_argument('--line_size', dest='cache_line_size',
                    type=int, default=64,
                    help='Size of the cache line in bits, default is 64')

parser.add_argument('--way_count', dest='way_count',
                    type=int, default=16,
                    help='The number of ways in each set if using set associative cache, default is 16')

parser.add_argument('--replacement_policy', dest='replacement_policy',
                    type=str, default='LRU',
                    choices=['LRU', 'MRU', 'FIFO'],
                    help='Default is LRU')

parser.add_argument('--write_policy', dest='write_policy',
                    type=str, default='WRITE_BACK',
                    choices=['WRITE_BACK', 'WRITE_THROUGH', 'WRITE_BUFFER'],
                    help='Default is WRITE_BACK')

parser.add_argument('trace_file', type=str,
                    help='Name/path of trace file')


cmd_args = parser.parse_args()

print('Simulator running with arguments:')
print ('cache_size in bits\t=', cmd_args.cache_size)
print ('cache_line_size in bits\t=', cmd_args.cache_line_size)
print ('way_count\t\t=', cmd_args.way_count)
print ('replacement_policy\t=', cmd_args.replacement_policy)
print ('write_policy\t\t=', cmd_args.write_policy)
print ('trace_file\t\t=', cmd_args.trace_file, '\n\n')



# # Creating the cache with the provided specs
# cache = Cache(cmd_args.cache_size,
#               cmd_args.way_count,
#               cmd_args.cache_line_size,
#               cmd_args.replacement_policy,
#               cmd_args.write_policy)

line_count = 0
miss_count = 0


# regex to parse trace line
line_re = re.compile(r'^\s*.+:\s+(\w)\s+(\w+)')


# opening and reading the trace file
with open(cmd_args.trace_file, 'r') as infile:
    for line_num, line in enumerate(infile):

        miss = 0

        # line count starts at 1
        line_count += 1

        # prase line with regex
        line = line.strip()
        matchObj = line_re.search(line)
        if matchObj is None:
            print("Invalid Regex parse. Skipping line ", line_count, ": ", line, sep='')
            continue

        # the operation R or W (read or write)
        op_type = matchObj.group(1).capitalize()

        # memory address of data, converted str -> hex
        try:
            data_addr = int(matchObj.group(2), 16)
        except:
            print("Invalid Hex conversion. Skipping line ", line_count, ": ", line, sep='')
            continue


        # print('group 1:', op_type, 'group 2:', matchObj.group(2), "int_addr", data_addr)

        if op_type == 'R':
            # miss = cache.read(data_addr)
            miss = 1
        elif op_type == 'W':
            # miss = cache.write(data_addr)
            miss = 0
        else:
            print("Operation was neither read or write. Skipping Line ", line_count, ": ", line, sep='')

        if miss == 1:
            miss_count += 1




    print('Cache miss rate: {:.2%}'.format(float(miss_count)/line_count))
