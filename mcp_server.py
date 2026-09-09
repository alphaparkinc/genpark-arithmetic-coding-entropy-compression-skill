"""MCP Server for Arithmetic Coding Skill."""
import json
import sys
from client import ArithmeticCoder
from collections import Counter

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            req_id = req.get("id")
            method = req.get("method")
            params = req.get("params", {})

            if method == "tools/list":
                res = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "tools": [{
                            "name": "compress_arithmetic",
                            "description": "Compress text using finite-precision Arithmetic Coding",
                            "inputSchema": {
                                "type": "object",
                                "properties": {"text": {"type": "string"}},
                                "required": ["text"]
                            }
                        }]
                    }
                }
            elif method == "tools/call":
                args = params.get("arguments", {})
                text = args["text"]
                symbols = list(text)
                freqs = Counter(symbols)
                coder = ArithmeticCoder(freqs)
                bits, count = coder.encode(symbols)
                res = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [{
                            "type": "text",
                            "text": json.dumps({
                                "bitstream": bits,
                                "bit_length": len(bits),
                                "original_length": len(text),
                                "frequencies": dict(freqs)
                            })
                        }]
                    }
                }
            else:
                res = {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}
            print(json.dumps(res), flush=True)
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32000, "message": str(e)}}
            print(json.dumps(err), flush=True)

if __name__ == "__main__":
    main()
