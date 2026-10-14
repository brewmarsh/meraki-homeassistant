from src.staging_test.reporter import ReportManager


def test_fingerprint_stability():
    manager = ReportManager("token", "repo")
    failure = {"entity_id": "sensor.test", "state": "unknown"}
    f1 = manager.generate_fingerprint(failure)
    f2 = manager.generate_fingerprint(failure)
    assert f1 == f2


def test_fingerprint_uniqueness():
    manager = ReportManager("token", "repo")
    f1 = manager.generate_fingerprint({"entity_id": "sensor.a", "state": "unknown"})
    f2 = manager.generate_fingerprint({"entity_id": "sensor.b", "state": "unknown"})
    assert f1 != f2
