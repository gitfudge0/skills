---
name: fudge:experience-measurement
description: Define or assess whether a launched UI helps people complete a task. Use for outcome metrics, funnel and event plans, postlaunch analysis, or UI experiments; use fudge:ux-research for qualitative observation of people.
---

# Experience measurement

Measure the task the person came to do. A click, page view, or shorter session may help diagnose a result, but is not task success by itself. Match the measurement effort to the decision at hand.

## Choose the work

- **Plan:** Define success, guardrails, events, data checks, and a comparison before instrumenting or launching. If the UI is already live without a baseline, specify a prospective read or a credible comparison.
- **Analyze:** Inspect available data and its collection rules. Report observed results, missing coverage, uncertainty, and the change the evidence supports.
- **Experiment:** When the decision needs a causal answer and a controlled comparison is feasible, specify assignment, exposure, outcome window, guardrails, and a decision rule before reading results. Check for uneven assignment or exposure and concurrent changes before interpreting the outcome.

## Define the task measure

1. State whose task matters, where it starts, and what verified completion means. Define the eligible population, unit of analysis, start event, success event, and time window. Say how repeat visits, multiple attempts, partial completions, and exclusions count. Make the numerator and denominator reproducible.
2. Add diagnostics for the steps where people may stall, abandon, encounter an error, retry, or ask for help. Include relevant guardrails such as incorrect submissions, support contacts, accessibility issues, or downstream reversals. Do not improve a completion rate by silently narrowing eligibility or counting an unverified click as success.
3. Name the segments that could change the decision, such as role, entry route, device, new versus returning user, or assistive technology where responsibly measurable. Use only attributes the project may collect and retain under its privacy and consent rules. Avoid small segments that could expose a person.

## Establish trustworthy data

For each necessary event, specify its trigger, time, actor or session key, task or attempt key, and properties needed to reconstruct the task. Distinguish client intent from server-confirmed success. Check event order, duplicates, missing events, retry paths, clock or identity joins, and whether the data can reproduce known test journeys. State what was inspected and what remains unverified. Instrumentation changes are implementation work: use `fudge:delegate` when requested, then verify the recorded events. Do not write to analytics or other external systems without authorization.

Use an existing baseline only if its event definitions, eligible population, time window, and collection quality are comparable. If none exists, say so. Plan a forward baseline, phased rollout, or controlled comparison as the situation allows. A forward measure of the redesigned UI alone cannot establish whether that redesign helped; without a credible comparator, the original effect remains unanswered and current performance becomes the baseline for future changes. Account for traffic mix, seasonality, campaigns, product changes, and other plausible confounds. A before-and-after difference alone does not establish that the UI caused it. For an experiment, inspect assignment integrity and guardrails as well as the primary outcome; report the effect and uncertainty in terms the decision owner can use.

## Turn evidence into a decision

Return the metric definition, data provenance and quality checks, observed results or an explicit **not yet measured** status, comparison limits, and a recommendation tied to the evidence. State what result would prompt keeping, revising, or reverting the design and when to measure again. Pair funnel or event evidence with `fudge:ux-research` when the team needs to understand why people struggle; analytics does not supply their reasoning. Do not invent events, a baseline, improvement, statistical confidence, or a causal claim. `fudge:ship` owns implementation and delivery when this work sits inside a broader build.
