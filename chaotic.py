import utime

class LogMapSimple():
    
    def __init__(self, x, n = 8):
        self._x = x
        self._u = 2**n
        
    def __call__(self):
        x = (self._x * (1 + self._x)) % self._u + 1
        if x == 0:
            x = 1
        self._x = x
        return self._x
    
    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, x):
        self._x = x
    
class LogMap():
    
    def __init__(self, x, u = 3.97):
        self._x = x
        self._u = u
        
    def __call__(self):
        self._x = self._x * self._u * (1.0 -  self._x)
        return self._x 
    
    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, x):
        self._x = x
        
    @property
    def u(self):
        return self._u
    
    @u.setter
    def u(self, u):
        self._u = u
        
    
if __name__ == "__main__":
    log_map = LogMap(0.4)
    start = utime.ticks_us()
    for _ in range(10000):
        log_map()
    end = utime.ticks_us()
    print("Elapsed time:", (end - start) / 1000, "ms")
    
    
    log_map_simple = LogMapSimple(1)
    start = utime.ticks_us()
    for _ in range(10000):
        log_map_simple()
    end = utime.ticks_us()
    print("Elapsed time:", (end - start) / 1000, "ms")