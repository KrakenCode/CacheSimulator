class WriteBack:
    
    def __init__(self):
        self.cache = None

    def write(address):
        tag, set_id, offset = address
        for cache_line in cache.sets[set_id].ways:
            if tag == cache_line["tag"]:
                cache_line["dirty"] = 1
                return 0

        cache.read(address)


    def upon_eviction(address):
        print("Writing to memory")
