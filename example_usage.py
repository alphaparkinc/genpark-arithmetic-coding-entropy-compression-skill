"""Example usage for Arithmetic Coding Skill."""
from client import ArithmeticCoder
from collections import Counter

def main():
    print("Executing Arithmetic Coding Compression...")
    msg = list("ABRACADABRA")
    freqs = Counter(msg)
    coder = ArithmeticCoder(freqs)

    bits, count = coder.encode(msg)
    print(f"Encoded bits ({len(bits)} bits): {bits}")

    decoded = coder.decode(bits, count)
    reconstructed = "".join(decoded)
    print("Decoded string:", reconstructed)
    assert reconstructed == "ABRACADABRA", "Decoded string does not match original"
    print("Arithmetic Coding verified successfully!")

if __name__ == "__main__":
    main()
