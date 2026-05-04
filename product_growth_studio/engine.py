from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass
class FunnelSnapshot:
    visitors: int
    signup: int
    activated: int
    paid: int


def pct(numerator: float, denominator: float) -> float:
    return (numerator / denominator * 100.0) if denominator > 0 else 0.0


def funnel_metrics(snapshot: FunnelSnapshot) -> Dict[str, float]:
    return {
        "signup_rate": pct(snapshot.signup, snapshot.visitors),
        "activation_rate": pct(snapshot.activated, snapshot.signup),
        "payment_rate": pct(snapshot.paid, snapshot.activated),
        "full_cvr": pct(snapshot.paid, snapshot.visitors),
    }


def detect_bottleneck(snapshot: FunnelSnapshot) -> str:
    metrics = funnel_metrics(snapshot)
    step_rates = {
        "가입": metrics["signup_rate"],
        "활성화": metrics["activation_rate"],
        "결제": metrics["payment_rate"],
    }
    return min(step_rates, key=step_rates.get)


def projected_paid_users(snapshot: FunnelSnapshot, improve_step: str, improve_pct: float) -> int:
    rates = funnel_metrics(snapshot)
    signup_rate = rates["signup_rate"]
    activation_rate = rates["activation_rate"]
    payment_rate = rates["payment_rate"]

    factor = 1 + (improve_pct / 100.0)
    if improve_step == "가입":
        signup_rate *= factor
    elif improve_step == "활성화":
        activation_rate *= factor
    elif improve_step == "결제":
        payment_rate *= factor

    paid = snapshot.visitors * (signup_rate / 100.0) * (activation_rate / 100.0) * (payment_rate / 100.0)
    return max(0, int(round(paid)))
