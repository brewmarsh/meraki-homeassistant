# Roadmap: The Retrospective Loop

## Concept

A weekly GitHub action that gathers pull request history.

## Mechanism

Uses `gh pr list` to generate a `context/weekly_review.txt` artifact.

## Goal

Feeds this context to a smart agent (Gemini 1.5 Pro) to automatically update `agents.md` with lessons learned from failed continuous integration runs.
