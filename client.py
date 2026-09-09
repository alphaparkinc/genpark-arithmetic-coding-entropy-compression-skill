"""
Autonomous Agent Arithmetic Coding Compression Skill
Pure Python Standard Library implementation with 32-bit integer arithmetic.
"""
from typing import List, Dict, Any, Tuple
from collections import Counter

class ArithmeticCoder:
    """
    Finite-precision (32-bit) Arithmetic Coding lossless encoder & decoder.
    """
    PRECISION = 32
    TOP_VALUE = (1 << PRECISION) - 1
    FIRST_QTR = (TOP_VALUE // 4) + 1
    HALF = 2 * FIRST_QTR
    THIRD_QTR = 3 * FIRST_QTR

    def __init__(self, frequencies: Dict[str, int]):
        self.freqs = dict(frequencies)
        self.total = sum(frequencies.values())
        self.cum_freq = {}
        cum = 0
        for symbol, freq in sorted(self.freqs.items()):
            self.cum_freq[symbol] = (cum, cum + freq)
            cum += freq

    def encode(self, symbols: List[str]) -> Tuple[str, int]:
        low = 0
        high = self.TOP_VALUE
        underflow_bits = 0
        bitstream = []

        for sym in symbols:
            cum_low, cum_high = self.cum_freq[sym]
            rng = high - low + 1
            high = low + (rng * cum_high) // self.total - 1
            low = low + (rng * cum_low) // self.total

            while True:
                if high < self.HALF:
                    bitstream.append("0")
                    bitstream.extend(["1"] * underflow_bits)
                    underflow_bits = 0
                    low = low << 1
                    high = (high << 1) | 1
                elif low >= self.HALF:
                    bitstream.append("1")
                    bitstream.extend(["0"] * underflow_bits)
                    underflow_bits = 0
                    low = (low - self.HALF) << 1
                    high = ((high - self.HALF) << 1) | 1
                elif low >= self.FIRST_QTR and high < self.THIRD_QTR:
                    underflow_bits += 1
                    low = (low - self.FIRST_QTR) << 1
                    high = ((high - self.FIRST_QTR) << 1) | 1
                else:
                    break

        underflow_bits += 1
        if low < self.FIRST_QTR:
            bitstream.append("0")
            bitstream.extend(["1"] * underflow_bits)
        else:
            bitstream.append("1")
            bitstream.extend(["0"] * underflow_bits)

        return "".join(bitstream), len(symbols)

    def decode(self, bitstring: str, num_symbols: int) -> List[str]:
        low = 0
        high = self.TOP_VALUE
        val = 0
        bits = [int(b) for b in bitstring] + [0] * self.PRECISION

        for i in range(self.PRECISION):
            val = (val << 1) | bits[i]
        bit_idx = self.PRECISION

        decoded = []
        for _ in range(num_symbols):
            rng = high - low + 1
            scaled = ((val - low + 1) * self.total - 1) // rng

            match_sym = None
            for sym, (c_low, c_high) in self.cum_freq.items():
                if c_low <= scaled < c_high:
                    match_sym = sym
                    break

            decoded.append(match_sym)
            c_low, c_high = self.cum_freq[match_sym]
            high = low + (rng * c_high) // self.total - 1
            low = low + (rng * c_low) // self.total

            while True:
                if high < self.HALF:
                    low = low << 1
                    high = (high << 1) | 1
                    val = (val << 1) | (bits[bit_idx] if bit_idx < len(bits) else 0)
                    bit_idx += 1
                elif low >= self.HALF:
                    low = (low - self.HALF) << 1
                    high = ((high - self.HALF) << 1) | 1
                    val = ((val - self.HALF) << 1) | (bits[bit_idx] if bit_idx < len(bits) else 0)
                    bit_idx += 1
                elif low >= self.FIRST_QTR and high < self.THIRD_QTR:
                    low = (low - self.FIRST_QTR) << 1
                    high = ((high - self.FIRST_QTR) << 1) | 1
                    val = ((val - self.FIRST_QTR) << 1) | (bits[bit_idx] if bit_idx < len(bits) else 0)
                    bit_idx += 1
                else:
                    break

        return decoded
