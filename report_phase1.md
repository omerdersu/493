# IE493 Phase 1 Report — Group 13

## 1. Methodology

We analyzed a dataset of 1,000 patients arriving at a 5-doctor Emergency Room. The simulation starts at 08:00 with all doctors available and an empty queue. Priority levels are ignored in this phase, and the system operates on a First-Come, First-Served basis.

**Assumptions:**
- Infinite buffer: there is no limit on the number of patients who can wait.
- Steady-state analysis: we assume the system reaches equilibrium over the observation period.
- No breaks or shift changes for doctors.
- Patients do not leave the queue before being served.

**Key Formulas:**
- Arrival rate: λ = (number of patients − 1) / total observation time
- Service rate per doctor: μ = 1 / mean service time
- Server utilization: ρ = λ / (s × μ), where s = 5
- Coefficient of Variation: Cv = std(service time) / mean(service time)
- Erlang-C formula for P(wait > 0)
- M/M/5 waiting time: Wq = C(s, r) / (s × μ − λ)
- Kingman approximation for M/G/5: Wq(M/G/5) ≈ Wq(M/M/5) × (1 + Cv²) / 2
- Little's Law: L = λ × W, Lq = λ × Wq

---

## 2. Task 1: Data Inference and Distribution Fitting

### Parameter Estimation

From our dataset of 1,000 patients observed over 4044.6 minutes:

| Parameter | Value |
|-----------|-------|
| λ (arrival rate) | 0.2470 patients/min (14.82 patients/hour) |
| μ (service rate per doctor) | 0.0637 patients/min |
| Mean inter-arrival time (1/λ) | 4.05 min |
| Mean service time (1/μ) | 15.70 min |
| ρ (utilization) | 0.7757 (77.6%) |
| Cv (service times) | 0.4240 |

### Goodness-of-Fit

We tested whether inter-arrival times follow an Exponential distribution and whether service times follow a Lognormal distribution using the Kolmogorov-Smirnov test at α = 0.05.

| Distribution | KS Statistic | p-value | Result |
|-------------|-------------|---------|--------|
| Inter-arrival ~ Exponential | 0.0203 | 0.7980 | Fail to reject H₀ — Good fit |
| Service ~ Lognormal | 0.0241 | 0.5999 | Fail to reject H₀ — Good fit |

The Lognormal fit parameters are σ = 0.3963 and μ_log = 2.6741.

Both distributions pass the KS test with high p-values, confirming that arrivals are well-modeled by a Poisson process and service times by a Lognormal distribution.

Histograms with the fitted curves are shown in Figure 1.

---

## 3. Task 2: Theoretical Modeling

Using the estimated parameters, we computed the theoretical performance metrics for the M/M/5 and M/G/5 models.

- Offered load: r = λ/μ = 3.8787 Erlangs
- Erlang-C probability: C(5, r) = 0.5083
- Kingman correction factor: (1 + Cv²)/2 = 0.5899

| Metric | M/M/5 | M/G/5 |
|--------|-------|-------|
| Wq (avg queue wait, min) | 7.1185 | 4.1992 |
| Lq (avg queue length) | 1.7582 | 1.0372 |
| W (avg time in system, min) | 22.8221 | 19.9028 |
| L (avg number in system) | 5.6369 | 4.9159 |

Since our Cv = 0.424 is less than 1, service times have lower variability than an Exponential distribution. The Kingman correction reduces the M/M/5 estimate by about 41%, bringing it closer to reality.

---

## 4. Comparison Table

We compare the observed simulation results with both theoretical models.

| Metric | Observed | M/M/5 | M/G/5 |
|--------|----------|-------|-------|
| Wq (min) | 4.8916 | 7.1185 | 4.1992 |
| Lq (patients) | 1.2082 | 1.7582 | 1.0372 |
| W (min) | 20.5953 | 22.8221 | 19.9028 |
| L (patients) | 5.0869 | 5.6369 | 4.9159 |

The M/M/5 model overestimates Wq by 45.5% because it assumes Cv = 1, which means more variability in service times than we actually have. The M/G/5 model underestimates Wq by 14.2%. The observed value falls between the two models but is closer to the M/G/5 prediction.

The remaining gap between M/G/5 and the observed value comes from two factors. First, the Kingman formula is an approximation, not exact. Second, our dataset of 1,000 patients is a single finite sample, so the observed statistics carry sampling noise.

---

## 5. Task 3: PASTA Property

The PASTA property states that Poisson arrivals see time averages. We verify this by comparing two quantities:

- p5 (time average): the fraction of total simulation time when all 5 doctors were busy = 50.27%
- a5 (arrival average): the fraction of arriving patients who found all 5 doctors busy = 50.70%

The difference |p5 − a5| = 0.0043, which is very small. This confirms that PASTA holds for our Poisson arrival process. Patients arriving at random see the same system state as a continuous observer would.

---

## 6. Task 4: Sensitivity Analysis

### 4.1 Warm-up Period

We simulated 5,000 patients at three utilization levels and tracked how long it takes for the cumulative average Wq to stabilize near the theoretical M/G/5 value. The criterion is that the cumulative average must stay within ±5% of the theoretical Wq for 500 consecutive patients.

| ρ | Theoretical Wq (min) | Simulated Wq (min) | Warm-up ends at patient # |
|---|---------------------|--------------------|-----------------------------|
| 0.60 | 1.09 | 1.11 | ~3121 |
| 0.80 | 5.13 | 4.71 | >5000 (not stabilised) |
| 0.95 | 32.53 | 19.57 | >5000 (not stabilised) |

At low utilization, the system stabilizes within a few thousand patients. At ρ = 0.80, the cumulative average is close to the theoretical value but has not yet settled within the strict ±5% band. At ρ = 0.95, the system is far from steady state even after 5,000 patients. This is expected because high utilization causes long queues to build up slowly, and the cumulative average converges very slowly.

The warm-up plot is shown in Figure 2.

### 4.2 Arrival Patterns

We compared four arrival distributions while keeping the same mean arrival rate and service time distribution.

| Pattern | Wq (min) | W (min) | p5 | a5 | PASTA |
|---------|---------|--------|------|------|-------|
| Poisson (Exp) | 4.15 | 19.85 | 0.4823 | 0.4902 | Holds |
| Erlang-2 | 2.01 | 17.72 | 0.4142 | 0.3636 | Fails |
| Erlang-3 | 1.24 | 16.94 | 0.3667 | 0.2962 | Fails |
| Uniform | 1.52 | 17.22 | 0.3667 | 0.3006 | Fails |

Poisson arrivals produce the highest waiting times because they have the most variability. Erlang and Uniform arrivals are more regular, which leads to less queueing. PASTA only holds for Poisson arrivals, as expected from theory. For the other arrival types, the arrival average a5 is consistently lower than the time average p5, meaning these patients are less likely to arrive during busy periods because their arrivals are more evenly spaced.

### 4.3 Service Time Variation

We tested how different levels of service variability affect Wq, using 1,000 replications of 5,000 patients each.

| Scenario | Cv | Wq Simulated (min) | Wq Kingman (min) |
|----------|------|-------------------|------------------|
| Erlang-25 | 0.20 | 3.89 | 3.70 |
| Erlang-9 | 0.33 | 4.10 | 3.95 |
| Our data (Lognormal) | 0.42 | 4.29 | 4.20 |
| Exponential | 1.00 | 7.09 | 7.12 |
| Hyperexponential | 1.50 | 11.14 | 11.57 |

Higher service variability leads to longer waiting times. Going from Cv = 0.20 to Cv = 1.50 almost triples the average waiting time. The Kingman approximation tracks the simulation results well across all Cv values, which validates its use as a quick estimation tool.

---

## 7. Simulation Validation

We verified the correctness of our simulation by checking that the total service time required by all patients equals the total busy time across all doctors.

| Doctor | Busy Time (min) | Patients Served |
|--------|----------------|-----------------|
| 1 | 3123.37 | 192 |
| 2 | 3157.64 | 193 |
| 3 | 3161.09 | 199 |
| 4 | 3136.58 | 204 |
| 5 | 3124.93 | 212 |
| **Total** | **15703.61** | **1000** |

Total service time required from the dataset is also 15703.61 minutes. The difference is 0.000000 minutes. In an FCFS queue without preemption, each patient's service time is processed by exactly one doctor without interruption. No work is lost or duplicated, so these totals must match exactly. This confirms that our simulation logic is correct.

---

## 8. Insights

The main findings from Phase 1 are:

1. The arrival process is well-described by a Poisson process, and service times follow a Lognormal distribution with Cv = 0.42. Since Cv < 1, service times are less variable than Exponential, which means less queueing than the M/M/5 model predicts.

2. The M/M/5 model overestimates waiting times by about 45% because it assumes Exponential service times. The M/G/5 model with Kingman approximation gives a much closer estimate, underestimating by about 14%.

3. PASTA holds for our system, confirming the Poisson nature of arrivals. When we switch to more regular arrival patterns like Erlang or Uniform, PASTA breaks down as expected.

4. The system is most sensitive to utilization. At ρ = 0.95, waiting times grow very fast and the system takes much longer to reach steady state. Service variability also has a big impact, with higher Cv leading to longer waits. These results highlight that both capacity planning and service consistency are important for ER performance.
