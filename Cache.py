import math
'''
CacheLine

    valid bit
    dirty bit
    data
'''

class CacheSet:

    def __init__(self, way_count):
        self.ways = [
            {
                'tag': None,
                'valid': 0,
                'dirty': 0,
                'data': 0,
                'last_access': 0,
                'entry_time': 0
            } for i in range(way_count)
        ]
        self.timer = 0
    
    def read(self, tag):
        self.timer += 1

        for way in self.ways:
            if tag == way['tag']:
                way['last_access'] = self.timer 
                return True 
        return False 
    
    def write(self, tag):
        self.timer += 1




class Cache:

    def __init__(self, cache_size, way_count, cache_line_size, replacement_policy, write_policy, parent, inclusive=True, hit_cost=0):
        
        self.set_count = int(cache_size / way_count / cache_line_size)

        self.cache_size = cache_size
        self.way_count = way_count
        self.eviction_policy = replacement_policy
        self.write_policy = write_policy
        self.cache_line_size = cache_line_size
        self.parent = parent
        self.hit_cost = hit_cost

        self.write_policy.cache = self

        self.sets = [CacheSet(way_count) for i in range(self.set_count)]

        print('Cache Size: {}, way_count: {}, cachelinesize: {}, set count: {}, actual set count: {}'.format(cache_size, way_count, cache_line_size, self.set_count, cache_size / way_count / cache_line_size))

    def _parse_addr(self, addr):

        '''
        tag
        set_id
        offset

        address is binary
        '''

        offset = addr & self.cache_line_size - 1
        set_id = addr & ((self.set_count - 1) << int(math.log(self.cache_line_size, 2)))
        tag = addr >> (int(math.log(self.set_count, 2))  + int(math.log(self.cache_line_size, 2)))

        return tag, set_id, offset



    def read(self, addr):

        if type(addr) == tuple:
            tag, set_id, offset = addr
        else:
            tag, set_id, offset = self._parse_addr(addr)

        potential_set = self.sets[set_id]

        if potential_set.read(tag):
            return self.hit_cost 
        else:
            
            evictable_idx = self.eviction_policy(potential_set)
            
            miss_time = self.parent.read(addr)

            if miss_time == 0:
                return miss_time + self.hit_cost
            
            evicted = potential_set.ways[evictable_idx]

            self.write_policy.upon_eviction((tag, set_id, offset))

            evicted['valid'] = 1
            evicted['tag'] = tag
            evicted['entry_time'] = potential_set.timer
            evicted['last_access'] = potential_set.timer
            evicted['dirty'] = 0

            return miss_time + self.hit_cost
        

    def write(self, addr):
        return self.hit_cost + self.write_policy(self._parse_addr(addr))

class Memory:

    def __init__(self):
        pass 
    
    def read(self, addr):
        return 1 
    def write(self, addr):
        return 1

    