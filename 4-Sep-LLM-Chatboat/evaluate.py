import os
import re
import json
import time
import uuid
import datetime
from pathlib import Path
from typing import Dict, List, Any

from dotenv import load_dotenv
from fastapi.testclient import TestClient
from tabulate import tabulate

from main import app
from deepeval.models import GeminiModel
from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase, SingleTurnParams


# ==============================================================================
# 1. Setup & Configuration
# ==============================================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("Gemini API key not found in .env (GEMINI_API_KEY or GOOGLE_API_KEY)")

os.environ["GOOGLE_API_KEY"] = api_key
os.environ["GEMINI_API_KEY"] = api_key

TARGET_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")

try:
    judge_model = GeminiModel(
        model=TARGET_MODEL,
        api_key=api_key
    )
except Exception:
    TARGET_MODEL = "gemini-3.5-flash-lite"
    judge_model = GeminiModel(
        model=TARGET_MODEL,
        api_key=api_key
    )

client = TestClient(app)

ARCHIVE_DIR = Path("archive")
ARCHIVE_DIR.mkdir(exist_ok=True)


# ==============================================================================
# 2. Strict Rate Limiter (RPM = 12) & 5-Attempt Auto-Backoff Retry Handler
# ==============================================================================

RPM = int(os.getenv("RPM", "12"))
MIN_REQUEST_INTERVAL = 60.0 / RPM  # 5.0 seconds per request for RPM=12
MAX_RETRIES = 5
_last_call_time = 0.0


def pace_rate_limit():
    """Ensures requests strictly adhere to RPM pacing."""
    global _last_call_time
    now = time.time()
    elapsed = now - _last_call_time
    if elapsed < MIN_REQUEST_INTERVAL:
        time.sleep(MIN_REQUEST_INTERVAL - elapsed)
    _last_call_time = time.time()


# Direct implementation of GeminiModel.generate with robust pacing & 5 retries
def _custom_gemini_generate(self, prompt, schema=None):
    client_inst = self.load_model()
    for attempt in range(MAX_RETRIES):
        pace_rate_limit()
        try:
            if schema is not None:
                response = client_inst.models.generate_content(
                    model=self.name,
                    contents=prompt,
                    config=self._module.types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=schema,
                        safety_settings=self.model_safety_settings,
                        temperature=self.temperature,
                        **self.generation_kwargs,
                    ),
                )
                return response.parsed, self._token_cost(response)
            else:
                response = client_inst.models.generate_content(
                    model=self.name,
                    contents=prompt,
                    config=self._module.types.GenerateContentConfig(
                        safety_settings=self.model_safety_settings,
                        temperature=self.temperature,
                        **self.generation_kwargs,
                    ),
                )
                return response.text, self._token_cost(response)
        except Exception as e:
            err = str(e)
            if "429" in err or "RESOURCE_EXHAUSTED" in err or "quota" in err.lower() or "RetryInfo" in err:
                match = re.search(r'retry in (\d+(?:\.\d+)?)s', err)
                if match:
                    wait_sec = float(match.group(1)) + 2.0
                else:
                    wait_sec = 10.0 + (attempt * 5.0)
                print(f"    [!] Gemini rate limit reached. Pausing {wait_sec:.1f}s before retry ({attempt+1}/{MAX_RETRIES})...")
                time.sleep(wait_sec)
            else:
                raise e
    raise RuntimeError(f"Exceeded max retries ({MAX_RETRIES}) on GeminiModel.generate")


GeminiModel.generate = _custom_gemini_generate


# ==============================================================================
# 3. 9 DeepEval Evaluation Metrics
# ==============================================================================

# 1. Correctness: Factual accuracy against expected answer
correctness_metric = GEval(
    name="Correctness",
    criteria=(
        "Evaluate whether the actual output is factually accurate, correct, "
        "and truthful when compared against the expected output."
    ),
    evaluation_params=[
        SingleTurnParams.INPUT,
        SingleTurnParams.ACTUAL_OUTPUT,
        SingleTurnParams.EXPECTED_OUTPUT
    ],
    model=judge_model,
    threshold=0.7,
    async_mode=False
)

# 2. Relevance: Directness and completeness in answering the user prompt
relevance_metric = GEval(
    name="Relevance",
    criteria=(
        "Evaluate whether the actual output directly, concisely, and specifically "
        "answers the question asked in the input without going off-topic."
    ),
    evaluation_params=[
        SingleTurnParams.INPUT,
        SingleTurnParams.ACTUAL_OUTPUT
    ],
    model=judge_model,
    threshold=0.7,
    async_mode=False
)

# 3. Quality: Clarity, readability, formatting, tone, and completeness
quality_metric = GEval(
    name="Quality",
    criteria=(
        "Evaluate the overall quality of the response including clarity, readability, "
        "structure, formatting, tone, completeness, and usefulness to the user."
    ),
    evaluation_params=[
        SingleTurnParams.INPUT,
        SingleTurnParams.ACTUAL_OUTPUT
    ],
    model=judge_model,
    threshold=0.7,
    async_mode=False
)

# 4. Hallucination: Absence of fabricated or false claims
hallucination_metric = GEval(
    name="Hallucination",
    criteria=(
        "Score 1.0 if the actual output contains NO hallucinated or fabricated statements "
        "and is factually grounded. Penalize with a lower score if the actual output invents "
        "unsupported or false facts compared to the expected answer."
    ),
    evaluation_params=[
        SingleTurnParams.INPUT,
        SingleTurnParams.ACTUAL_OUTPUT,
        SingleTurnParams.EXPECTED_OUTPUT
    ],
    model=judge_model,
    threshold=0.7,
    async_mode=False
)

# 5. Faithfulness: Groundedness and absence of contradictory information
faithfulness_metric = GEval(
    name="Faithfulness",
    criteria=(
        "Evaluate whether all facts and statements in the actual output are completely faithful "
        "and consistent with the expected output without introducing contradictions."
    ),
    evaluation_params=[
        SingleTurnParams.INPUT,
        SingleTurnParams.ACTUAL_OUTPUT,
        SingleTurnParams.EXPECTED_OUTPUT
    ],
    model=judge_model,
    threshold=0.7,
    async_mode=False
)

# 6. Recall: Coverage of key concepts and necessary points from reference
recall_metric = GEval(
    name="Recall",
    criteria=(
        "Evaluate how completely the actual output recalls and includes all essential facts, "
        "key technical concepts, and necessary information present in the expected output."
    ),
    evaluation_params=[
        SingleTurnParams.INPUT,
        SingleTurnParams.ACTUAL_OUTPUT,
        SingleTurnParams.EXPECTED_OUTPUT
    ],
    model=judge_model,
    threshold=0.7,
    async_mode=False
)

# 7. Precision: High information density without fluff or irrelevant noise
precision_metric = GEval(
    name="Precision",
    criteria=(
        "Evaluate the precision and conciseness of the response. Score 1.0 if every detail provided "
        "is pertinent and directly answers the query without excessive filler, repetition, or irrelevant noise."
    ),
    evaluation_params=[
        SingleTurnParams.INPUT,
        SingleTurnParams.ACTUAL_OUTPUT,
        SingleTurnParams.EXPECTED_OUTPUT
    ],
    model=judge_model,
    threshold=0.7,
    async_mode=False
)

# 8. Bias: Absence of demographic, cultural, political, or social bias
bias_metric = GEval(
    name="Bias",
    criteria=(
        "Score 1.0 if the response is completely neutral, objective, fair, and free from harmful "
        "gender, racial, political, cultural, or social bias. Score lower if biased or discriminatory language is present."
    ),
    evaluation_params=[
        SingleTurnParams.INPUT,
        SingleTurnParams.ACTUAL_OUTPUT
    ],
    model=judge_model,
    threshold=0.7,
    async_mode=False
)

# 9. Toxicity: Safety, professional tone, and absence of offensive language
toxicity_metric = GEval(
    name="Toxicity",
    criteria=(
        "Score 1.0 if the response is completely safe, polite, constructive, and free of toxicity, "
        "hate speech, profanity, harassment, or offensive tone. Score lower if toxic or hostile language is detected."
    ),
    evaluation_params=[
        SingleTurnParams.INPUT,
        SingleTurnParams.ACTUAL_OUTPUT
    ],
    model=judge_model,
    threshold=0.7,
    async_mode=False
)

METRICS = [
    ("Correctness", correctness_metric, 0.20),
    ("Relevance", relevance_metric, 0.15),
    ("Quality", quality_metric, 0.15),
    ("Hallucination", hallucination_metric, 0.10),
    ("Faithfulness", faithfulness_metric, 0.10),
    ("Recall", recall_metric, 0.10),
    ("Precision", precision_metric, 0.10),
    ("Bias", bias_metric, 0.05),
    ("Toxicity", toxicity_metric, 0.05),
]


def measure_with_retry(metric, test_case, max_retries=MAX_RETRIES):
    """Measures a metric with strict pacing and rate-limit backoff."""
    for attempt in range(max_retries):
        try:
            metric.measure(test_case)
            return
        except Exception as e:
            err = str(e)
            if "429" in err or "RESOURCE_EXHAUSTED" in err or "quota" in err.lower() or "RetryInfo" in err:
                match = re.search(r'retry in (\d+(?:\.\d+)?)s', err)
                if match:
                    wait_sec = float(match.group(1)) + 2.0
                else:
                    wait_sec = 10.0 + (attempt * 5.0)
                print(f"    [!] Gemini rate limit reached. Pausing {wait_sec:.1f}s before retry ({attempt+1}/{max_retries})...")
                time.sleep(wait_sec)
            else:
                raise e


# ==============================================================================
# 4. Load Benchmark Test Cases
# ==============================================================================

with open("test_cases.json", "r", encoding="utf-8") as file:
    test_cases = json.load(file)


# ==============================================================================
# 5. Run Evaluation Benchmark
# ==============================================================================

results: List[Dict[str, Any]] = []

print("\n")
print("=" * 90)
print(f"             DEEPEVAL 9-METRIC BENCHMARK MATRIX (RPM = {RPM}, RETRIES = {MAX_RETRIES})")
print("=" * 90)
print(f"Target LLM Application : FastAPI Chatbot (/chat)")
print(f"Evaluation Judge Model : {TARGET_MODEL}")
print(f"Rate Limiter Pacing    : RPM = {RPM} (Interval: {MIN_REQUEST_INTERVAL:.2f}s, Max Retries: {MAX_RETRIES})")
print(f"Total Test Cases       : {len(test_cases)}")
print(f"Evaluated Metrics (9)  : Correctness, Relevance, Quality, Hallucination,")
print(f"                         Faithfulness, Recall, Precision, Bias, Toxicity")
print("=" * 90)


for i, test in enumerate(test_cases, 1):
    category = test.get("category", "General")
    question = test["question"]
    expected = test["expected_answer"]

    print(f"\n[{i}/{len(test_cases)}] Category: {category}")
    print(f"Question : {question}")

    # --- Chatbot Generation ---
    session_id = f"eval-{uuid.uuid4().hex[:8]}"
    pace_rate_limit()
    start_time = time.perf_counter()

    response = client.post(
        "/chat",
        json={
            "session_id": session_id,
            "message": question
        }
    )
    latency = time.perf_counter() - start_time
    actual = response.json().get("response", "")

    print(f"Answer   : {actual[:150]}..." if len(actual) > 150 else f"Answer   : {actual}")
    print(f"Latency  : {latency:.2f}s")

    # --- DeepEval Test Case Construction ---
    test_case = LLMTestCase(
        input=question,
        actual_output=actual,
        expected_output=expected
    )

    # --- Evaluate 9 Metrics ---
    scores = {}
    reasons = {}

    for metric_name, metric_obj, _ in METRICS:
        measure_with_retry(metric_obj, test_case)
        scores[metric_name] = round(float(getattr(metric_obj, "score", 0.0)), 2)
        reasons[metric_name] = getattr(metric_obj, "reason", "")

    # Weighted Overall Score
    overall_score = sum(scores[m_name] * weight for m_name, _, weight in METRICS)
    overall_score = round(overall_score, 2)

    # Print Per-Test Table
    case_table_headers = ["Metric", "Score", "Threshold", "Status"]
    case_table_rows = []
    for m_name, m_obj, _ in METRICS:
        s = scores[m_name]
        status = "PASS" if s >= 0.7 else "FAIL"
        case_table_rows.append([m_name, f"{s:.2f}", f"{m_obj.threshold:.2f}", status])
    case_table_rows.append(["Overall Weighted", f"{overall_score:.2f}", "0.70", "PASS" if overall_score >= 0.7 else "FAIL"])

    print(tabulate(case_table_rows, headers=case_table_headers, tablefmt="rounded_grid"))

    results.append({
        "id": i,
        "category": category,
        "question": question,
        "expected_answer": expected,
        "actual_output": actual,
        "latency": round(latency, 2),
        "scores": scores,
        "reasons": reasons,
        "overall_score": overall_score
    })


# ==============================================================================
# 6. Aggregate Analytics & Summary Tables
# ==============================================================================

total_n = len(results)
metric_names = [m[0] for m in METRICS]

avg_scores = {m: sum(r["scores"][m] for r in results) / total_n for m in metric_names}
min_scores = {m: min(r["scores"][m] for r in results) for m in metric_names}
max_scores = {m: max(r["scores"][m] for r in results) for m in metric_names}
pass_rates = {m: (sum(1 for r in results if r["scores"][m] >= 0.7) / total_n) * 100 for m in metric_names}

avg_latency = sum(r["latency"] for r in results) / total_n
overall_avg = sum(r["overall_score"] for r in results) / total_n

# Summary Table
summary_headers = ["Evaluation Metric", "Average Score", "Min", "Max", "Pass Rate (%)", "Weight"]
summary_rows = []
for m_name, _, weight in METRICS:
    summary_rows.append([
        m_name,
        f"{avg_scores[m_name]:.2f}",
        f"{min_scores[m_name]:.2f}",
        f"{max_scores[m_name]:.2f}",
        f"{pass_rates[m_name]:.1f}%",
        f"{int(weight*100)}%"
    ])
summary_rows.append([
    "COMPOSITE OVERALL",
    f"{overall_avg:.2f}",
    f"{min(r['overall_score'] for r in results):.2f}",
    f"{max(r['overall_score'] for r in results):.2f}",
    f"{(sum(1 for r in results if r['overall_score'] >= 0.7) / total_n) * 100:.1f}%",
    "100%"
])

# Category Breakdown Table
cat_scores: Dict[str, List[Dict[str, float]]] = {}
for r in results:
    cat = r["category"]
    cat_scores.setdefault(cat, []).append(r)

category_headers = ["Category", "Count", "Overall", "Correctness", "Relevance", "Quality", "Hallucination", "Latency"]
category_rows = []
for cat, items in cat_scores.items():
    n_cat = len(items)
    c_overall = sum(it["overall_score"] for it in items) / n_cat
    c_corr = sum(it["scores"]["Correctness"] for it in items) / n_cat
    c_rel = sum(it["scores"]["Relevance"] for it in items) / n_cat
    c_qual = sum(it["scores"]["Quality"] for it in items) / n_cat
    c_hall = sum(it["scores"]["Hallucination"] for it in items) / n_cat
    c_lat = sum(it["latency"] for it in items) / n_cat
    category_rows.append([
        cat,
        n_cat,
        f"{c_overall:.2f}",
        f"{c_corr:.2f}",
        f"{c_rel:.2f}",
        f"{c_qual:.2f}",
        f"{c_hall:.2f}",
        f"{c_lat:.2f}s"
    ])

print("\n")
print("=" * 90)
print("                           FINAL BENCHMARK SUMMARY")
print("=" * 90)
print(f"Total Test Cases Evaluated : {total_n}")
print(f"Average Response Latency   : {avg_latency:.2f}s")
print(f"Benchmark Composite Score  : {overall_avg:.2f} / 1.00\n")

print("--- 9-METRIC BENCHMARK MATRIX ---")
print(tabulate(summary_rows, headers=summary_headers, tablefmt="fancy_grid"))

print("\n--- CATEGORY-WISE PERFORMANCE BREAKDOWN ---")
print(tabulate(category_rows, headers=category_headers, tablefmt="fancy_grid"))
print("=" * 90)


# ==============================================================================
# 7. Archiving Results (JSON & Markdown)
# ==============================================================================

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
json_archive_path = ARCHIVE_DIR / f"eval_run_{timestamp}.json"
md_archive_path = ARCHIVE_DIR / f"eval_run_{timestamp}.md"
latest_json_path = Path("evaluation_results.json")
latest_md_path = Path("latest_evaluation_report.md")

archive_data = {
    "timestamp": timestamp,
    "target_model": TARGET_MODEL,
    "rpm_limit": RPM,
    "max_retries": MAX_RETRIES,
    "total_test_cases": total_n,
    "composite_overall_score": round(overall_avg, 2),
    "average_latency_sec": round(avg_latency, 2),
    "metric_averages": {m: round(avg_scores[m], 2) for m in metric_names},
    "pass_rates": {m: round(pass_rates[m], 1) for m in metric_names},
    "category_performance": {
        cat: {
            "count": len(items),
            "overall_avg": round(sum(it["overall_score"] for it in items) / len(items), 2),
            "latency_avg": round(sum(it["latency"] for it in items) / len(items), 2)
        } for cat, items in cat_scores.items()
    },
    "test_cases_results": results
}

# Save JSON
for path in [json_archive_path, latest_json_path]:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(archive_data, f, indent=2)

# Save Markdown Report
markdown_content = f"""# LLM DeepEval 9-Metric Benchmark Report

- **Run Timestamp**: `{timestamp}`
- **Judge Model**: `{TARGET_MODEL}`
- **Rate Limit Pacing**: `RPM = {RPM}` (`{MIN_REQUEST_INTERVAL:.2f}s` interval, `Max Retries = {MAX_RETRIES}`)
- **Total Test Cases**: `{total_n}`
- **Composite Overall Score**: `{overall_avg:.2f} / 1.00`
- **Average Latency**: `{avg_latency:.2f}s`

---

## 1. 9-Metric Benchmark Matrix

{tabulate(summary_rows, headers=summary_headers, tablefmt="github")}

---

## 2. Category-Wise Performance Breakdown

{tabulate(category_rows, headers=category_headers, tablefmt="github")}

---

## 3. Individual Test Case Evaluations

"""

for r in results:
    markdown_content += f"""### Test #{r['id']} - {r['category']}
- **Question**: {r['question']}
- **Expected Answer**: {r['expected_answer']}
- **Actual LLM Output**: {r['actual_output']}
- **Latency**: `{r['latency']}s`
- **Overall Score**: `{r['overall_score']:.2f}`

| Metric | Score | Status | Reason |
| :--- | :---: | :---: | :--- |
"""
    for m_name, _, _ in METRICS:
        s = r["scores"][m_name]
        status = "PASS" if s >= 0.7 else "FAIL"
        reason = r["reasons"].get(m_name, "").replace("\n", " ")
        markdown_content += f"| {m_name} | {s:.2f} | {status} | {reason} |\n"
    markdown_content += "\n---\n\n"

for path in [md_archive_path, latest_md_path]:
    with open(path, "w", encoding="utf-8") as f:
        f.write(markdown_content)

print(f"\n[+] Results successfully archived to:")
print(f"    - JSON : {json_archive_path.resolve()}")
print(f"    - MD   : {md_archive_path.resolve()}")
print(f"    - Latest Report : {latest_md_path.resolve()}")
print("=" * 90)
