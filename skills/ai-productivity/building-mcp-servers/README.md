# MCP Server Builder

**Category:** ai-productivity · **Priority:** supporting · **Audience:** full-stack

Designs and implements MCP (Model Context Protocol) servers in TypeScript (MCP SDK) or Python (FastMCP): tool granularity (coverage vs workflow tools), stdio vs stateless streamable-HTTP transport, Zod/Pydantic input schemas with outputSchema and structuredContent, the four tool annotations, pagination and response projection to protect the context window, actionable error messages, and a 10-question read-only evaluation set. Use when exposing an internal API or service to Claude as tools, reviewing an existing MCP server that agents use poorly, or deciding whether to ship one fat workflow tool or many primitives.

## When Claude should reach for this

Trigger phrases: `mcp server`, `model context protocol`, `fastmcp`, `registerTool`, `mcp tools`, `expose api to claude`

## What you get

Open [`SKILL.md`](SKILL.md) for the full instructions Claude loads.
