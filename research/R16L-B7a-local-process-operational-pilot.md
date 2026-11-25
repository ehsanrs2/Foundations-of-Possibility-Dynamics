# R16-L / B7a — Local process operational feasibility

2026-11-25. **Local engineering pilot, not independent physical evidence.**

The pilot actually creates a child Python process in a private temporary directory, advances an immutable work ID and checkpoint, stops only that owned child, observes its exit and unavailable response interface, and restarts from the same checkpoint. A same-ID probe followed by a second completed work step must succeed before the five-second local deadline. A no-restart negative control observes full follow-up to the deadline. Monotonic-clock chronology is recorded; errors/timeouts abort rather than manufacture a successful result.

No external fault injection, network, privileged system control, production service, personal data or third-party infrastructure. Each worker is explicitly owned by the pilot and cleaned up. The process is a trivial checkpointed workload, not an HPC job, independent physical failure mechanism or a model of real service availability beyond this local interface. The same operator controls and assesses the experiment; no external clock calibration or independently signed evidence. There is no independently sampled system, calibrated hazard, H1 preregistration or comparative feature effect.

Run on Linux: python -m unittest tests.test_p1_r16l_b7_process_pilot -v ; python -m experiments.p1_r16l_b7_process_pilot

Next: independent observer and approved isolated apparatus; separate controller and assessor logging, verified same-work identity, clock calibration and external attestation before any field admission. Repeated local runs do not constitute independent systems. B7-I/Q/H remain blocked. Do not use this pilot to unlock P1.
