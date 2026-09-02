# EIOS Market-Data Intake

The local provider accepts a JSON object keyed by ticker. Every record must include `current_price`, `consensus_eps`, and `approved`.

Example structure (values must come from an approved source):

```json
{
  "TICKER": {
    "current_price": 0,
    "volume": 0,
    "relative_performance_1y": 0,
    "consensus_eps": 0,
    "approved": false
  }
}
```

Set `approved` to `true` only after the source, timestamp and figures have been checked. Validate before import:

`python scripts/validate_market_data_file.py <file.json>`

Unapproved or incomplete records remain staged and cannot affect valuation or an EIOS verdict.
