# Lab 02: A2A for Context‑Aware, Agentic Experiences

## Understanding A2A

A2A (Agent2Agent) is an open protocol that gives AI agents a common language to discover each other, exchange messages, and collaborate across different frameworks and vendors. Instead of treating another agent like a simple tool call, A2A allows true agent-to-agent interaction, including multi-turn conversations, delegation, and bidirectional workflows.

In practice, the flow is: discover an agent through its agent card, authenticate, send a request, and optionally stream task updates/results for long-running work. A2A is designed to be secure and enterprise-ready (HTTPS, standard auth patterns, opaque execution), while supporting rich modalities beyond plain text.

A2A and MCP are complementary:

- MCP standardizes how an agent connects to tools, APIs, and data sources (agent-to-tool).
- A2A standardizes how agents communicate with other agents (agent-to-agent).

Think of MCP as how an agent uses capabilities, and A2A as how agents collaborate with each other to solve more complex end-to-end tasks.

In this lab you are going to learn how to leverage Work IQ via A2A.

## Run the supported Work IQ A2A sample

> [!IMPORTANT]
> Work IQ CLI 1.0 no longer includes the legacy `workiq a2aserver`
> command. Use the current Microsoft Work IQ A2A sample instead.

Complete the app registration and delegated `WorkIQAgent.Ask` permission
steps in the
[Work IQ A2A quickstart](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/work-iq/a2a/quickstart).
Keep the resulting application ID and tenant ID available as `APP_ID` and
`TENANT_ID`.

Clone the official samples:

```bash
git clone https://github.com/microsoft/work-iq-samples.git
cd work-iq-samples/dotnet/a2a
```

On Windows, start the .NET A2A client with Windows Account Manager:

```bash
dotnet run -- --token WAM --appid <APP_ID> --tenant <TENANT_ID>
```

On macOS and Linux, WAM is unavailable. Start the client with a pre-obtained
Work IQ bearer token instead:

```bash
dotnet run -- --token <JWT>
```

After authentication, the terminal displays a `READY` line for the Work IQ
A2A gateway.

## Consume Work IQ via A2A

At the `You >` prompt, send:

```text
Who am I? What is my role in the company?
```

Work IQ returns an answer grounded in the signed-in user's Microsoft 365
profile and permissions. Anonymize names, email addresses, account aliases,
and other personal data before sharing the output.

Send a second message in the same session:

```text
When is my next meeting?
```

The sample preserves the A2A conversation context and sends both requests to
the Work IQ gateway at `https://workiq.svc.cloud.microsoft/a2a/`.

For a lower-level view of the JSON-RPC request and the `A2A-Version: 1.0`
header, run the official raw HTTP sample:

```bash
cd ../a2a-raw
# Windows with WAM:
dotnet run -- --token WAM --appid <APP_ID> --tenant <TENANT_ID>

# Any platform with a pre-obtained Work IQ bearer token:
dotnet run -- --token <JWT>
```

For badge evidence, capture the successful A2A terminal exchange and
anonymize all personal or organization-specific data. Never include access
tokens in a screenshot.

## Wrap up

As you can see, you can consume Work IQ as a remote agent from any other
agent that supports the A2A protocol. The supported gateway speaks A2A
directly, so a local relay server is not required.

## Where to go next

- **Explore the IQ Series** — Learn about Foundry IQ with [Episode 1: Foundry IQ: Unlocking Knowledge for your Agents](../../../Foundry-IQ/1-Foundry-IQ-Unlocking-Knowledge-for-Agents/).
