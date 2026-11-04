# R13 minimal physical-service evidence request (draft; NOT sent)

For a potential data custodian, request a small securely shared, authorized, pseudonymous set of **individual service episodes**, not private customer information.

- Stable nonidentifying physical system/group and **same service-goal IDs** at three times: active pre-fault, actually lost because of fault, and regained or censored through a predefined deadline.
- Pre-fault timestamped raw asset dependency graph, available capabilities, inventories, controller-visible state and policy/plan version, all measured before the prediction cut-off.
- Source incident/failure report showing physically supported event identity and causal connection to that exact loss, with aliases and common cause information.
- Complete observation and action/repair timeline linked by system, service, episode and policy trajectory IDs, including failed actions and kit use where applicable.
- Recovery timestamp of the **same service** or verified follow-up through the deadline; explicit censoring, data gaps, time zones and clock-quality notes.
- Permissions, pseudonymous independent-system sampling group, raw-source URI, checksum, schema version, documentation and a permitted research usage statement.
- Independent analyst review of physical mapping and of service-level join validity. Preregistration before viewing any independent test outcomes.

DO NOT request names, addresses, credentials, unredacted critical infrastructure topology or other personal/security-sensitive information. The [R13 admission script](../experiments/p1_r13_real_data_admission.py) evaluates schema and chronology only; no self-reported completeness flag can confer independent observational provenance.
