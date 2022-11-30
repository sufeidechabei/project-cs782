import math

class ArithmeticCoder:
    def __init__(self, range_bytes=4, code=None):
        self.range_bytes = range_bytes
        self.low, self.high = 0, 1 << range_bytes * 8
        self.follows = []
        self.target = None if code is None else int.from_bytes(code[:range_bytes], byteorder='big', signed=False)

    def __copy__(self):
        copy = ArithmeticCoder(self.range_bytes)
        copy.low, copy.high = self.low, self.high
        copy.follows = self.follows[:]
        copy.target = self.target
        return copy

    def __str__(self):
        s = 'ArithmeticCoder state:\n  high=%.8X' % (self.high - 1)
        if self.target is not None: s += '\ntarget=%.8X' % self.target
        s += '\n   low=%.8X' % self.low
        return s + '\n  code=' + str(self.follows)

    def coding_range(self):
        return self.high - self.low

    def target_freq(self):
        return (self.target - self.low) / self.coding_range()

    def advance(self, F, f, buffer=None):
        self.contract(F, f)
        return self.expand(buffer)

    def contract(self, F, f):
        r = self.coding_range()
        self.high = self.low + math.floor((F + f) * r)
        self.low += math.floor(F * r)


    def expand(self, buffer=None):
        range_bits, code = self.range_bytes * 8, []

        # Resolve follows if the leading bits match
        msb = self.low >> range_bits - 1
        if len(self.follows) > 0 and msb == self.high - 1 >> range_bits - 1:
            code.append(self.follows[0] + msb)
            for n in self.follows[1:]: code.append(n + msb ^ 0x80)
            self.follows = []
            self.invert_range()

        max = 1 << range_bits
        while self.high - self.low <= max >> 9:
            # Output code byte and shift the coding range
            symbol = self.low >> range_bits - 8
            self.low, self.high = (self.low << 8) % max, (self.high << 8) % max
            if self.high == 0: self.high = max
            if self.target is not None:
                self.target = (self.target << 8) % max
                # If decoding, pull the next byte from the buffer
                if buffer is not None and not buffer.closed:
                    b = buffer.read(1)
                    if len(b) == 0:
                        buffer.close()
                    else: self.target += b[0]
            if self.low > self.high:
                self.follows.append(symbol)
                self.invert_range()
            else: code.append(symbol)

        return code

    def invert_range(self):
        mask = 1 << self.range_bytes * 8 - 1
        self.low, self.high = self.low ^ mask, self.high ^ mask
        if self.target is not None: self.target = self.target ^ mask

