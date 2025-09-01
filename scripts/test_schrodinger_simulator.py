import pytest
import random
from math import sqrt

class SchrodingerSimulator:
    def __init__(self, p, rng=None):
        self.p = p
        self.rng = rng or random.Random()

    def run_trial(self, force_emit=None):
        """
        Run a single trial.
        - force_emit: None (random), True (force emission), False (force no emission)
        Returns: 'Dead' or 'Alive'
        """
        if force_emit is True:
            emitted = True
        elif force_emit is False:
            emitted = False
        else:
            emitted = (self.rng.random() < self.p)

        return "Dead" if emitted else "Alive"

    def monte_carlo(self, N):
        dead_count = 0
        for _ in range(N):
            if self.run_trial() == "Dead":
                dead_count += 1
        return dead_count, dead_count / N


# ------------------- Unit Tests -------------------

def test_forced_emission():
    sim = SchrodingerSimulator(p=0.5)
    assert sim.run_trial(force_emit=True) == "Dead"


def test_forced_no_emission():
    sim = SchrodingerSimulator(p=0.5)
    assert sim.run_trial(force_emit=False) == "Alive"


def test_observation_is_sticky():
    sim = SchrodingerSimulator(p=0.0)  # never emits
    result1 = sim.run_trial()
    result2 = sim.run_trial(force_emit=False)
    assert result1 == "Alive"
    assert result2 == "Alive"


def test_probabilistic_behavior_within_tolerance():
    p = 0.2
    N = 1000
    sim = SchrodingerSimulator(p=p, rng=random.Random(42))
    dead_count, proportion = sim.monte_carlo(N)

    # Compute tolerance using 3 sigma rule
    sigma = sqrt(p * (1 - p) / N)
    lower = p - 3 * sigma
    upper = p + 3 * sigma

    assert lower <= proportion <= upper, f"Observed proportion {proportion} out of range [{lower}, {upper}]"

def test_boundary_p_zero():
    sim = SchrodingerSimulator(p=0.0, rng=random.Random(123))
    dead_count, proportion = sim.monte_carlo(200)
    assert dead_count == 0
    assert proportion == 0.0

def test_boundary_p_one():
    sim = SchrodingerSimulator(p=1.0, rng=random.Random(123))
    dead_count, proportion = sim.monte_carlo(200)
    assert dead_count == 200
    assert proportion == 1.0
