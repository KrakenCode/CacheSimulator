#!/usr/bin/python3
import argparse
import re
import ReplacementPolicies
from WriteBack import WriteBack
from WriteThrough import WriteThrough
from Cache import Cache
from Cache import Memory

# Parsing the command line

parser = argparse.ArgumentParser()
parser.add_argument('--cache_size', dest='cache_size',
                    type=int, default=1048576,
                    help='Size of the cache in bytes, default is 1048576 (1MB)')

parser.add_argument('--line_size', dest='cache_line_size',
                    type=int, default=64,
                    help='Size of the cache line in bytes, default is 64')

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
print ('cache_size in bytes\t\t=', cmd_args.cache_size)
print ('cache_line_size in bytes\t=', cmd_args.cache_line_size)
print ('way_count\t\t\t=', cmd_args.way_count)
print ('replacement_policy\t\t=', cmd_args.replacement_policy)
print ('write_policy\t\t\t=', cmd_args.write_policy)
print ('trace_file\t\t\t=', cmd_args.trace_file, '\n\n')


# Get the correct replacement_policy function to pass to cache
if cmd_args.replacement_policy == 'FIFO':
    replacement_policy = ReplacementPolicies.pick_FIFO
elif cmd_args.replacement_policy == 'MRU':
    replacement_policy = ReplacementPolicies.pick_MRU
else:
    replacement_policy = ReplacementPolicies.pick_LRU



# Get the correct write policy class to pass to cache
if cmd_args.write_policy == 'WRITE_BUFFER':
    # TODO: change to write buffer once implemented
    write_policy = WriteBack()
elif cmd_args.write_policy == 'WRITE_THROUGH':
    write_policy = WriteThrough()
else:
    write_policy = WriteBack()



# Creating the cache with the provided specs
cache = Cache(cmd_args.cache_size,
              cmd_args.way_count,
              cmd_args.cache_line_size,
              replacement_policy,
              write_policy,
              Memory())

line_count = 0
miss_count = 0


# regex to parse trace line
line_re = re.compile(r'^\s*.+:\s+(\w)\s+(\w+)')


# opening and reading the trace file
with open(cmd_args.trace_file, 'r') as infile:
    for line in infile:

        miss = 0

        # line count starts at 1
        line_count += 1

        # prase line with regex
        line = line.strip()
        matchObj = line_re.search(line)
        if matchObj is None:
            print("Invalid Regex parse. Skipping line ", line_count, ": ", line, sep='')
            line_count -= 1
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
            miss = cache.read(data_addr)
            # print(miss)
            # miss = 1
        elif op_type == 'W':
            miss = cache.write(data_addr)
            # print(miss)
            # miss = 0
        else:
            print("Operation was neither read or write. Skipping Line ", line_count, ": ", line, sep='')

        if miss == 1:
            miss_count += 1




    print('Cache miss rate: {:.2%}'.format(float(miss_count)/line_count))
