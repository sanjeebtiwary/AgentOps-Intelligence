from cases import CASES
from metrics import compute_metrics
from run_benchmark import CONFIGS, build_engine


def run(name):
    policy, verify = CONFIGS[name]
    engine = build_engine(policy, verify)
    pairs = [(c, engine.execute(c.request)) for c in CASES]
    return pairs, compute_metrics(pairs, verifier_enabled=verify)


def test_case_ids_unique():
    assert len({c.id for c in CASES}) == len(CASES)


def test_full_config_matches_ground_truth():
    pairs, m = run("policy_verification")
    assert m["expected_outcome_accuracy"] == 1.0
    assert m["policy_violation_rate"] == 0.0
    assert m["silent_error_rate"] == 0.0
    assert m["verification_precision"] == 1.0 and m["verification_recall"] == 1.0


def test_baseline_misses_policy_and_verification_cases():
    pairs, m = run("baseline")
    missed = {c.id for c, o in pairs if o.status is not c.expected_status}
    assert missed == {"add_over_limit", "text_over_limit", "lossy_add_float"}
    assert m["policy_violation_rate"] == 1.0 and m["silent_error_rate"] > 0
    assert m["verification_precision"] is None


def test_strict_config_completes_fewer_tasks_than_baseline():
    # The documented trade-off: better outcome detection, fewer accepted results.
    assert run("policy_verification")[1]["task_success_rate"] < run("baseline")[1]["task_success_rate"]


def test_statuses_sum_to_case_count():
    for name in CONFIGS:
        m = run(name)[1]
        assert sum(m["status_counts"].values()) == m["cases"]
