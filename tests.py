command = './simulate.py --cache_size 1024 --way_count {} ./ls.trace.txt --replacement_policy=LRU --write_policy=WRITE_THROUGH'

max_ways = 16
way_count = 1

import subprocess

while way_count <= max_ways:
    subprocess.call(command.format(way_count).split(' '))
    way_count *= 2