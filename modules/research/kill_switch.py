from dataclasses import dataclass


@dataclass
class KillSwitchResult:
    passed: bool
    failed_checks: list
    message: str


class KillSwitchEngine:

    def evaluate(
        self,
        tam: bool,
        moat: bool,
        management: bool,
        financial_quality: bool,
        customer_concentration: bool
    ):

        failures = []

        if not tam:
            failures.append("Total Addressable Market")

        if not moat:
            failures.append("Economic Moat")

        if not management:
            failures.append("Management Quality")

        if not financial_quality:
            failures.append("Financial Quality")

        if not customer_concentration:
            failures.append("Customer Concentration")

        if failures:

            return KillSwitchResult(
                passed=False,
                failed_checks=failures,
                message="Research Terminated"
            )

        return KillSwitchResult(
            passed=True,
            failed_checks=[],
            message="Research Approved"
        )