import json

chunks = {
  "A": [
    "7b22726573706f6e736522",
    "3a225265706f7274206a6f622d34646563633364653a",
    "20222c22646f6e65223a66616c73657d0a7b",
    "227468696e6b696e67223a22696e7465726e616c206e6f",
    "7465222c22726573706f6e7365223a22222c2264",
    "6f6e65223a66616c73657d0a7b22",
    "726573706f6e7365223a22636166c3",
    "a95c6e222c22646f6e65223a66616c7365",
    "7d0a7b22726573706f6e7365223a22526561647920",
    "e2",
    "9c93222c22646f6e65223a747275652c22",
    "646f6e655f726561736f6e223a2273746f70227d0a"
  ],
  "B": [
    "7b22726573706f6e736522",
    "3a225061727469616c206a6f622d3464656363336465",
    "222c22646f6e65223a66616c73657d0a7b22",
    "726573706f6e7365223a22756e66696e6973686564"
  ],
  "C": [
    "7b22726573706f6e736522",
    "3a224472616674206a6f622d3464656363336465222c",
    "22646f6e65223a66616c73657d0a7b226572",
    "726f72223a226d6f64656c20756e6c6f61646564227d0a",
    "7b22726573706f6e7365223a2249474e4f524522",
    "2c22646f6e65223a747275657d0a"
  ]
}


def reconstruct(parts):
    raw = b"".join(bytes.fromhex(part) for part in parts)
    text = raw.decode("utf-8", errors="replace")

    records = []
    for line in text.split("\n"):
        if not line.strip():
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            # Ignore an incomplete or invalid trailing record.
            break

    result = {
        "text": "",
        "complete": False,
        "error": None,
    }

    for record in records:
        if "error" in record:
            result["error"] = record["error"]
            result["complete"] = False
            break

        result["text"] += record.get("response", "")

        if record.get("done") is True:
            result["complete"] = True
            break

    return result



results = {
    case: reconstruct(parts)
    for case, parts in chunks.items()
}

with open("output.json", "w", encoding="utf-8") as file:
    json.dump(results, file, ensure_ascii=False, indent=2)

print(json.dumps(results, ensure_ascii=False, indent=2))
print("\nCreated output.json successfully.")
