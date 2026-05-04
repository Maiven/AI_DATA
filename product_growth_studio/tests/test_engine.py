from product_growth_studio.engine import FunnelSnapshot, detect_bottleneck, funnel_metrics, projected_paid_users


def test_funnel_metrics_basic() -> None:
    snap = FunnelSnapshot(visitors=1000, signup=200, activated=100, paid=25)
    m = funnel_metrics(snap)
    assert round(m["signup_rate"], 1) == 20.0
    assert round(m["activation_rate"], 1) == 50.0
    assert round(m["payment_rate"], 1) == 25.0
    assert round(m["full_cvr"], 1) == 2.5


def test_detect_bottleneck() -> None:
    snap = FunnelSnapshot(visitors=1000, signup=500, activated=100, paid=50)
    assert detect_bottleneck(snap) == "활성화"


def test_projection_increases_paid_users() -> None:
    snap = FunnelSnapshot(visitors=2000, signup=300, activated=120, paid=30)
    baseline = projected_paid_users(snap, "가입", 0)
    improved = projected_paid_users(snap, "가입", 20)
    assert improved > baseline
