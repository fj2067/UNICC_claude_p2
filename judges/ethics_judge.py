import json
from judges.base_judge import BaseJudge, call_ollama


class EthicsJudge(BaseJudge):

    def __init__(self):
        super().__init__("Ethics Judge")

    def evaluate(self, text):

        prompt = (
            "You are an AI ethics judge evaluating text for ethical violations.\n"
            "Analyze the following text and respond with ONLY valid JSON "
            "(no markdown, no extra text) in this exact format:\n"
            '{"score": <float 0.0-1.0>, "verdict": "<safe or unsafe>", '
            '"reasons": ["<reason1>", ...]}\n\n'
            "Rules:\n"
            "- score >= 0.5 means unsafe\n"
            "- Check for: hate speech, violence, harmful language, "
            "discrimination, dehumanization, incitement\n\n"
            f"Text to evaluate:\n{text}"
        )

        try:
            raw = call_ollama(prompt)
            start = raw.find("{")
            end = raw.rfind("}") + 1
            if start != -1 and end > start:
                result = json.loads(raw[start:end])
            else:
                result = {"score": 0.0, "verdict": "safe", "reasons": []}
        except Exception:
            result = {"score": 0.0, "verdict": "safe", "reasons": ["Evaluation failed, defaulting to safe"]}

        score = float(result.get("score", 0.0))
        verdict = result.get("verdict", "safe").lower()
        if verdict not in ("safe", "unsafe"):
            verdict = "unsafe" if score >= 0.5 else "safe"
        reasons = result.get("reasons", [])

        return {
            "judge": self.name,
            "score": score,
            "verdict": verdict,
            "reasons": reasons,
        }
