# First financial source check

Status: assistant source check completed; independent review still required.

Two original PDF spreads were visually inspected. Their file fingerprints match the saved extraction provenance. The selected standalone cash-flow figures match the source year columns and lakh units.

| Selected period | Report / PDF page | Operating cash (crore) | Fixed-asset cash spending (crore) | Calculated free cash flow (crore) |
| --- | --- | ---: | ---: | ---: |
| FY2024-25 | 2024-25 / 141 (printed 278-279), column 1 | 2,545.70 | 829.64 | 1,716.06 |
| FY2022-23 | 2023-24 / 137 (printed 270-271), column 2 | 560.47 | 605.48 | -45.01 |

The source shows spending as a negative outflow. EIOS stores its positive magnitude and subtracts it from operating cash. Neither selected pair requires a numeric correction based on this check.

## What this does and does not establish

- The original rows, year columns, units and calculations for these two examples match.
- The negative calculation means these fixed-asset purchases exceeded operating cash; it does not alone establish that the company is a poor investment.
- This free-cash-flow definition excludes separately reported acquisition and leasehold-land payments. It is not a quoted financial statement row or money necessarily available to shareholders.
- This is not an audit of all statement components, later restatements or the full eight-year series.
- No human approval, META approval, governed evidence or investment verdict was created. The human learning-feedback count remains zero.
- Machine-readable assistant observations are preserved separately in `data/runtime/financial_source_assistant_review.json`, tied to the worksheet example fingerprints. They are not imported as trusted human training labels.

## Next review step

An independent reviewer should verify the selected source pages and the definition. Any corrections must be recorded with their source and reviewer identity. Do not grant blanket approval to the remaining years based on these two checks.
