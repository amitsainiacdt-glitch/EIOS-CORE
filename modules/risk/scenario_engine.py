class ScenarioEngine:

    def evaluate(self, risk_data: dict):

        return {
            "Bull Case": {
                "Probability": 25,
                "Description": "Strong execution with favorable market conditions."
            },
            "Base Case": {
                "Probability": 50,
                "Description": "Business performs in line with current expectations."
            },
            "Bear Case": {
                "Probability": 25,
                "Description": "Execution challenges and adverse macro conditions."
            },
            "Expected Outcome": "Base Case",
            "Score": 83,
            "Confidence": 40
        }