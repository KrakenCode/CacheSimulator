class WriteBack:
    
    def __init__(self):
        self.cache = None

    def write(self, address):
        tag, set_id, offset = address
        for cache_line in self.cache.sets[set_id].ways:
            if tag == cache_line["tag"]:
                cache_line["dirty"] = 1
                return 0

        return self.cache.read(address)


    def upon_eviction(self, address):
        tag, set_id, offset = address
        for cache_line in self.cache.sets[set_id].ways:
            if tag == cache_line["tag"]:
                if cache_line["dirty"] == 1:
                    return 1
        return 0
