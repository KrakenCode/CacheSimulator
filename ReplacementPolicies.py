def pick_LRU(cache):
    idx = find_open_idx(cache)
    if idx:
        return idx

    LRU = cache.ways[0]
    LRU_idx = 0
    for i, cache_line in enumerate(cache.ways[1:]):
        if cache_line["last_access"] < LRU["last_access"]:
            LRU = cache_line
            LRU_idx = i+1
    return LRU_idx

def pick_FIFO(cache):
    idx = find_open_idx(cache)
    if idx:
        return idx

    FI = cache.ways[0]
    FI_idx = 0
    for i, cache_line in enumerate(cache.ways[1:]):
        if cache_line["entry_time"] < FI["entry_time"]:
            FI = cache_line
            FI_idx = i+1
    return FI_idx

def pick_MRU(cache):
    idx = find_open_idx(cache)
    if idx:
        return idx

    MRU = cache.ways[0]
    MRU_idx = 0
    for i, cache_line in enumerate(cache.ways[1:]):
        if cache_line["last_access"] > MRU["last_access"]:
            MRU = cache_line
            MRU_idx = i+1
    return MRU_idx

def find_open_idx(cache):
    for i, cache_line in enumerate(cache.ways):
        if not cache_line["valid"]:
            return i
    return None



