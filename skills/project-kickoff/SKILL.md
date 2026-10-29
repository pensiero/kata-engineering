---
name: project-kickoff
description: Turn a rough project idea into a structured starting point before execution begins. Use this skill whenever starting something new from a vague idea — it interrogates the concept, challenges weak assumptions, and produces a project brief, a phased project shape, first actions, and a refined kickoff prompt ready to hand to an agent.
---

# Project Kickoff

Turn a rough idea into a strong starting point for AI-assisted execution — not by rewriting it, but by clarifying it, challenging weak thinking, and producing what is needed to start well.

## 1. Interrogate

If the idea is too vague to work with, say so and ask the few questions that matter most. Wait for the answers.

## 2. Critique

Summarize the idea in plain language: the core problem, the likely users, the desired outcome. Then name what is ambiguous, assumed, contradictory, vague or too broad. Be direct; do not flatter or rubber-stamp weak thinking. Separate facts, assumptions (labelled as provisional) and unknowns.

## 3. Produce

Always:

- **Brief** — problem, target users, goals and non-goals, constraints, success criteria, risks.
- **Project shape** — MVP / next / later. If the scope is too broad, recommend a narrower first version.
- **First 3 actions** — concrete, ordered by dependency.
- **Kickoff prompt** — what an execution agent needs: the brief, constraints, success criteria and phased framing. Optimized for execution quality, not hype.

Only when the idea needs them:

- **Research** — unknowns and assumptions to validate, reference systems worth studying, and what must be answered before building vs. what can wait.
- **Execution plan** — phases, dependencies and decision points, when there is more than one phase.
- **Quality gates** — what must be true before building starts, and before the first version is reviewed.

When there are several valid paths, present the best ones and recommend one. Prefer a sharper, smaller, more executable project. Do not invent certainty.

## 4. Hand off

Once the human approves, write the outcome where `build` will find it: the project's `PLAN.md` (from `build`'s plan template), with the brief at the top under "What we're building", the shape as Up Next and Deferred, unknowns as Open Questions, and ordering rules as Prioritization. If the project keeps its work in a tracker, the work goes there and the brief stays in `PLAN.md`. If there is no project directory yet, give the outputs in chat.

This skill produces strategy, not code. Pass the kickoff prompt to `build`, whose Bootstrap phase selects the tier and scaffolds the project.
