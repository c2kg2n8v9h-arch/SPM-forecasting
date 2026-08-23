# AWS Production Foundation

## Decision

Use this AWS-hosted, API-first design as a learning reference architecture. The current application remains entirely local and mock-first, optimizing for maintenance planners and inventory/procurement teams by providing secure, traceable recommendations rather than automating operational decisions.

This is a proposed target architecture. It creates no AWS resources and must be reviewed before any non-mock infrastructure or application implementation begins.

## Learning-only and mock-data boundary

All application flows must use deterministic mock data and local mock adapters.
Do not connect this project to an AWS account, Cognito tenant, ERP/MRO system,
email service, inventory system, third-party vector database, production AI
provider, or any source containing real operational or personal data.

The AWS services in this document describe the equivalent production controls
that the local design must model. For learning, use explicit simulated adapters:

| Production concern | Learning implementation |
| --- | --- |
| User sign-in and roles | Mock identity context with fixed roles and station/program scopes. |
| API edge/WAF | Local request validation, rate-limit simulation, payload limits, and rejected-request audit events. |
| Aurora records | Local, deterministic repository fixtures; no real customer data. |
| S3 documents | Repository sample documents or a local data directory containing only synthetic data. |
| SQS jobs | In-process/local queue simulation with deterministic retry and dead-letter scenarios. |
| Secrets/KMS | Environment-variable presence checks only; no real secret, token, or cloud credential. |
| Monitoring | Structured, redacted local logs and testable in-memory metrics/audit events. |

Mock data must be synthetic or explicitly approved public sample data. It must
not contain real employee, customer, aircraft, supplier, maintenance, financial,
credential, or operational records.

## User problem addressed

The current local CLI and static mock dashboard cannot give planners and buyers a shared, access-controlled, traceable view of forecast and material risk. The learning platform should simulate an authorized user reviewing a recommendation, inspecting its evidence and confidence, recording an approval/override decision, and retrieving that history without exposing another team's mock operational data.

## Proposed architecture

```text
Planner / Buyer browser
        |
CloudFront + AWS WAF
        |
API Gateway (authenticated, throttled)
        |
ECS Fargate API service --------------> Aurora PostgreSQL
        |                                      |
        |                                      +--> audit and approval records
        |
        +--> SQS job queue --> ECS Fargate worker --> S3 document/data storage
        |                                      |
        |                                      +--> forecast and retrieval processing
        |
        +--> Secrets Manager / KMS
        |
        +--> CloudWatch Logs, metrics, traces, alarms

Amazon Cognito supplies OIDC authentication and role claims.
```

## Service choices and rationale

| Need | AWS service | Security and usability rationale |
| --- | --- | --- |
| Sign-in and roles | Amazon Cognito, federation-ready | Supports SSO integration later and avoids application-managed passwords. |
| Public API edge | API Gateway + AWS WAF | Central authentication, throttling, request limits, and web attack protections. |
| Application runtime | ECS on Fargate in private subnets | Removes host management; supports a predictable API and worker runtime. |
| Operational data | Aurora PostgreSQL | Transactional approvals/audits, row-level access enforcement, backups, and recovery. |
| Documents and source files | Amazon S3 with KMS encryption | Durable versioned storage with scoped access and lifecycle retention rules. |
| Long-running work | SQS + worker service | Prevents slow ingestion/forecast tasks from blocking user requests; enables retries and dead-letter handling. |
| Secrets | AWS Secrets Manager | No credentials in code, images, CI logs, or local configuration files. |
| Encryption keys | AWS KMS | Centrally controlled encryption and auditable key access. |
| Monitoring | CloudWatch, X-Ray/OpenTelemetry | Supports operational visibility without logging sensitive record contents. |

## Privacy and data controls

- Treat every local fixture as synthetic. Production data is prohibited in this repository and in development/test environments unless separately approved and de-identified.
- Encrypt S3, Aurora, SQS, and logs with customer-managed KMS keys where the organization requires key ownership and revocation control.
- Block public S3 access, require TLS, restrict bucket access to named roles, enable versioning, and apply lifecycle/retention rules.
- Store only business-required fields. Log identifiers and event metadata, not document bodies, credentials, personal data, or full model prompts.
- Enforce access at the API and data layer using user role plus assigned station/program scope; never rely solely on a frontend filter.
- Do not transmit documents to an external LLM from this learning project. Any future production AI use requires data classification, privacy assessment, vendor review, and explicit approval.

## Authorization model

| Role | May do | May not do |
| --- | --- | --- |
| Maintenance Planner | View authorized forecasts/risks, submit plan decisions, request draft actions. | Approve procurement actions outside assigned authority; administer users or integrations. |
| Inventory/Procurement | View authorized material risk, review and approve/override purchase drafts within authority. | Change maintenance/compliance records; administer users or integrations. |
| Auditor | Read immutable decision and access history for assigned scope. | Alter operational data, recommendations, or logs. |
| Platform Administrator | Manage platform configuration through controlled change process. | Bypass business approvals or read business data by default. |

All write endpoints must record actor, role, time, input/version references, decision, reason, and correlation ID. The service must fail closed when claims, scope, or approval authority are missing.

## Network and reliability baseline

- Place ECS tasks and Aurora in private subnets; expose only CloudFront/API Gateway at the public edge.
- Use VPC endpoints for AWS service access where appropriate; avoid broad outbound internet access from workloads.
- Apply least-privilege IAM roles per service, short-lived credentials, and separate AWS accounts for development, staging, and production.
- Set API request limits, payload size limits, timeouts, retry policies, and circuit breakers. Use an SQS dead-letter queue and alarms for failed jobs.
- Enable automated backups, point-in-time recovery, multi-AZ production database deployment, tested restore procedures, and documented RTO/RPO.

## Delivery sequence

1. Introduce a local, versioned API with mock identity context, health checks, structured redacted logs, correlation IDs, and role/scope authorization tests.
2. Add local mock repositories for forecast runs, recommendations, approvals, and immutable audit events.
3. Simulate asynchronous document ingestion and forecast execution with a local queue, retries, and dead-letter scenarios.
4. Add usability flows for planner and buyer review/override decisions using only mock data.
5. Keep live-system adapters out of scope. Any future transition requires contract tests, privacy review, security review, and operational acceptance.

## Exit criteria for this foundation

- No cloud resources, external system calls, public data store, embedded secret, real personal/operational data, or unrestricted workload egress.
- Mock authentication, authorization, audit events, and privacy controls are covered by automated tests.
- A planner and a buyer can complete the core review workflow in a usability test, including stale-data, access-denied, and service-failure states.
- Recovery and rollback steps are documented and tested before production use.
