class WriteThrough:

    def __init__(self):
        self.cache = None

    def write(self, address):
        tag, set_id, offset = address
        for cache_line in cache.sets[set_id].ways:
            if tag == cache_line["tag"]:
                cache_line["valid"] = 0 

    def upon_eviction(self, address):
        print("Write to memory")   