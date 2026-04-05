from judges.technical_judge import SecurityJudge
from judges.governance_judge import GovernanceJudge
from judges.ethics_judge import EthicsJudge
from council.moe_council import SafetyCouncil
from council.arbitration import council_decision
from output.report import generate_report
import json
import sys


def main():

    text = input("Enter prompt to evaluate:\n") if sys.stdin.isatty() else "This AI agent answers questions about UN humanitarian policy and assists with refugee case management."

    judges = [
        SecurityJudge(),
        GovernanceJudge(),
        EthicsJudge()
    ]

    council = SafetyCouncil(judges)

    results = council.evaluate(text)

    decision = council_decision(results)

    report = generate_report(text, results, decision)

    print("\nSAFETY REPORT")
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
