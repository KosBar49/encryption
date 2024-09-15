import struct
import utime

def get_mantissa(f: float) -> int:
    # Pack the float into 4 bytes (as in C++), then unpack the first byte
    bytes_ = struct.pack('f', f)
    return bytes_[0]

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

class Xor():
    
    def __init__(self, log_map: LogMap):
        self.chaotic = log_map
        
    def cipher_data_simple(self, data_: bytearray):
        
        for i in range(len(data_)):
            data_[i] ^= self.chaotic()
            
    def cipher_data_mantissa(self, data_: bytearray):
        
        for i in range(len(data_)):
            seq_elem = get_mantissa(self.chaotic())
            data_[i] ^= seq_elem
            
    def cipher_data_norm(self, data_: bytearray):
        chaotic_ = []
        for _ in range(len(data_)):
            chaotic_.append(self.chaotic())
            
        for i in range(len(data_)):
            seq_elem = self.norm_elem(self.chaotic(), chaotic_)
            data_[i] ^= seq_elem
    
    def norm_elem(self, chaotic_elem: float, chaotic_: list):
        return int(abs((chaotic_elem - min(chaotic_))  / max(chaotic_) * 255 ) )

class NN:
    def __init__(self, log_map: LogMap):
        self._weights = [[0 for _ in range(8)] for _ in range(8)]
        self._biases = [0 for _ in range(8)]
        self.chaotic = log_map

    def get_mantissa(self, f: float) -> int:
        # Pack the float into 4 bytes (as in C++), then unpack the first byte
        bytes_ = struct.pack('f', f)
        return bytes_[0]

    def set_weights(self, elem: int):
        for i in range(8):
            for j in range(8):
                self._weights[i][j] = 0
                if elem & (1 << i):
                    self._biases[i] = 0.5
                    if j == i:
                        self._weights[i][j] = -1
                else:
                    self._biases[i] = -0.5
                    if j == i:
                        self._weights[i][j] = 1

    def calc_cipher(self, data_: int) -> int:
        for i in range(8):
            sum_ = 0
            for j in range(8):
                if data_ & (1 << j):  # Bitwise check for the jth bit in data_
                    sum_ += self._weights[i][j]

            sum_ += self._biases[i]
            if sum_ >= 0:
                data_ |= (1 << i)  # Set the ith bit in data_
            else:
                data_ &= ~(1 << i)  # Clear the ith bit in data_
        return data_

    def norm_elem(self, chaotic_elem: float, chaotic_: list):
        return int(abs((chaotic_elem - min(chaotic_))  / max(chaotic_) * 255 ) )

    def cipher_data_norm(self, data_: bytearray):
        chaotic_ = []
        for _ in range(len(data_)):
            chaotic_.append(self.chaotic())
            
        for i in range(len(data_)):
            seq_elem = self.norm_elem(chaotic_[i], chaotic_)
            self.set_weights(seq_elem)
            data_[i] = self.calc_cipher(data_[i])
        
    def cipher_data_mantissa(self, data_: bytearray):
        for i in range(len(data_)):
            seq_elem = get_mantissa(self.chaotic())  # Get chaotic sequence element
            self.set_weights(seq_elem)
            data_[i] = self.calc_cipher(data_[i])
    
    @property
    def weights(self):
        weights_ = ''
        for i in range(8):
            weights_ += str(self._weights[i]) + '\n'
        return weights_


if __name__ == "__main__":
    
    log_map = LogMapSimple(1)

    # Initialize NN with log_map
    nn = Xor(log_map)

    # Get the mantissa of the first chaotic sequence value
    string_data = "Hello, World!"

    # Convert string to bytearray
    test_data = bytearray(string_data, 'utf-8')

    start = utime.ticks_us()
    nn.cipher_data_simple(test_data)
    end = utime.ticks_us()
    
    # Print the ciphered data
    print("Elapsed time:", (end - start) / 1000, "ms")
    print("Ciphered data:", test_data)
    
    nn.chaotic.x = 1
    
    start = utime.ticks_us()
    nn.cipher_data_simple(test_data)
    end = utime.ticks_us()
    print("Elapsed time:", (end - start) / 1000, "ms")
    print("Decrypted data:", test_data)
    
    log_map = LogMap(0.2)
    
    nn = Xor(log_map)
    
    start = utime.ticks_us()
    nn.cipher_data_norm(test_data)
    end = utime.ticks_us()
    
    print("Elapsed time:", (end - start) / 1000, "ms")
    print("Encrypted data:", test_data)
    
    nn.chaotic.x = 0.2
    start= utime.ticks_us()
    nn.cipher_data_norm(test_data)
    end = utime.ticks_us()
    print("Elapsed time:", (end - start) / 1000, "ms")
    
    print("Decrypted data:", test_data)

