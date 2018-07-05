from . import shared

class utils(object):
    def __init__(self):
        self._log = shared._log

        self._log.debug("utils: Init constructor.")
    
    def get_mem_total(self):
        self._log.debug("utils: get mem total")
        import gc
        
        mem_total = gc.mem_alloc() + gc.mem_free()
        
        return mem_total
    
    def get_mem_free(self):
        import gc
        
        gc.collect()
        mem_free = gc.mem_free()
        
        return mem_free	

    def get_mem_current(self):
        import micropython
        
        # these functions are not always available
        if not hasattr(micropython, 'mem_current'):
           mem_current = -1
        else:
           mem_current = micropython.mem_current()
        
        return mem_current