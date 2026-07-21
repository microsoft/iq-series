# Lab 03: Tooling with MCP & Copilot CLI

## Understanding MCP

MCP (Model Context Protocol) is an open-source standard for connecting AI applications to external systems. Think of it as a "universal plug" for AI. Just like USB-C lets you connect your phone to almost anything, MCP lets AI models connect to tools, apps, and data sources without writing custom integration code for each one. This means an AI agent can call APIs, read files, send messages, and much more, all through a single standardized protocol. As a result, developers save time and AI solutions become more powerful, flexible, and easier to maintain.

An MCP server exposes three core primitives that AI applications can discover and use:

- **Tools**: Executable functions that AI applications can invoke to perform actions — such as querying a database, calling an external API, or manipulating files. Tools are the primary way agents *do things* through MCP.
- **Resources**: Data sources that provide contextual information to the AI application — such as file contents, database records, or API responses. Resources let agents *read* structured context without executing logic.
- **Prompts**: Reusable interaction templates that help structure how the language model is used, such as system prompts or few-shot examples. Prompts make it easy to share and standardize proven interaction patterns across agents.

In this lab you are going to learn how to leverage Work IQ via MCP.

## Understanding the Unified MCP Server of Work IQ

Work IQ exposes a unified MCP server that collapses hundreds of Microsoft 365 operations into just 10 generic tools. Rather than requiring a separate integration for every Microsoft 365 API, agents connect once and get immediate access to mail, calendar, files, people, chat, and sites, as well as the ability to act on that data.

The design of the Work IQ MCP server follows two key principles:

- **Simple verb-based tools**: Tools are expressed as generic verbs — `ask`, `fetch`, `create`, `update`, and others — making them easy for any agent or LLM to understand and invoke without Microsoft 365 specific knowledge.
- **Resource paths as context**: Resource paths define what the agent is currently working with, giving the agent precise, scoped access to the right data at the right time.

A standout feature is dynamic schema discovery via `getSchema`. Agents can call `getSchema` to understand what data exists in Microsoft 365, how it is organized, and how to interact with it, all at runtime. This turns every Microsoft 365 data source into a self-describing interface, allowing agents to adapt dynamically without hardcoded assumptions about the underlying data model.

## Prepare your tenant for consuming Work IQ via MCP

In this section you are going to register a Microsoft Entra ID application to allow your code to authenticate and consume Work IQ over MCP. If you already completed this step in [Lab 01](../../../Work-IQ/1-Work-IQ-Data-context-and-tools-at-scale/cookbook/work-iq-lab01.md){:target="_blank"}, you can skip this section and reuse the same `CLIENT_ID`, `TENANT_ID`, and `CLIENT_SECRET` values here.

However, in order to use the same application also in this lab, you will still need to configure the Redirect URL accordingly to the below step **Add a redirect URI**.

### Register the consumer application in Entra ID

In order to consume Work IQ you need to register a consumer application in your Entra ID tenant. Follow the steps below to complete the registration.

**Create the app registration**

1. Open the [Azure portal](https://portal.azure.com) and navigate to **Microsoft Entra ID** → **App registrations** → **New registration**.
2. Set the **Name** to `Work IQ Consumer`.
3. Under **Supported account types**, select **Accounts in this organizational directory only (single tenant)**.
4. Click **Register**.

**Configure a client secret**

1. In the app registration you just created, navigate to **Certificates & secrets** → **Client secrets** → **New client secret**.
2. Provide a description (for example, `ClientSecret`) and choose an expiration period.
3. Click **Add**, then immediately copy the **Value** of the newly created secret — you will not be able to retrieve it again after leaving this page.

**Add a redirect URI**

1. Navigate to **Authentication** → **Add a platform** → **Web**.
2. In the **Redirect URIs** field, for example enter `http://localhost:6274/oauth/callback`.
3. Click **Configure** to save the redirect URI.

**Configure delegated permissions for Work IQ API**

1. Navigate to **API permissions** → **Add a permission**.
2. Select the **APIs my organization uses** tab and search for `Work IQ`.
3. Select **Delegated permissions**, then find and check the **WorkIQAgent.Ask** permission.
4. Click **Add permissions**.

**Grant admin consent**

The `WorkIQAgent.Ask` permission requires admin consent before any user in the tenant can use it. A Global Administrator or Privileged Role Administrator must grant it:

1. Back on the **API permissions** page, click **Grant admin consent for \<your tenant\>**.
2. Confirm by clicking **Yes** in the dialog box.
3. Verify that the **Status** column for `WorkIQAgent.Ask` now shows a green check mark indicating consent has been granted.

**Retrieve the tenant and client identifiers**

Before proceeding, collect the following values from the app registration's **Overview** page — you will need them in the next steps:

| Value | Where to find it |
|---|---|
| `TENANT_ID` | **Directory (tenant) ID** |
| `CLIENT_ID` | **Application (client) ID** |
| `CLIENT_SECRET` | The secret value you copied earlier |


## Connecting to Work IQ via MCP

Open the **MCP Inspector** and configure the **Transport Type** field with value `Streamable HTTP` and the URL with value `https://workiq.svc.cloud.microsoft/mcp`.

It is now time to configure the **Authentication** settings. Select the **Authentication** command to expand the configuration section. Then configure the **OAuth 2.0 Flow** settings providing **Client ID**, **Client Secret**, and provide the following value for the Scope:

```text
api://workiq.svc.cloud.microsoft/WorkIQAgent.Ask
```

Now select the **Open Auth Settings** command in the middle of the screen and select **Quick OAuth Flow**. You will be prompted to login and you will need to provide valid credentials in your target tenant. Once the authentication flow will be completed, you will see a green box informing you that `Authentication completed successfully`.

You can now select the **Connect** command on the left side of the screen and start consuming the Work IQ unified MCP server.

## Consuming the Work IQ Unified MCP Server

Under the **Tools** tab select the **List Tools** command to retrieve the list of tools provided by the Work IQ Unified MCP Server. You should be able to see tools like:

- **ask**: Ask a question to Microsoft 365 Copilot for information about emails, meetings, files, and other M365 data. Returns the answer text in both content and structured content (under 'answer'), with conversationId in structured content for multi-turn conversations.
- **list_agents**: List available Microsoft 365 Copilot agents. Returns agent IDs that can be passed to ask's agentId parameter.
- **delete_entity**: Delete a WorkIQ entity by path. Sends HTTP DELETE to the entity path. Returns confirmation with status code on success. WorkIQ entity paths borrow from the conventions of Microsoft Graph.
- **do_action**: Execute a WorkIQ action via HTTP POST. Actions perform complex operations like sending mail, copying items, or moving resources. Use get_schema first to discover required parameters. WorkIQ entity paths borrow from the conventions of Microsoft Graph.
- **create_entity**: Create a new WorkIQ entity by POSTing JSON to a parent collection path. Use get_schema first to discover required fields. Returns the created entity JSON. WorkIQ entity paths borrow from the conventions of Microsoft Graph.
- **get_schema**: Get the OpenAPI schema for a WorkIQ operation. Returns a self-contained YAML schema with request/response schemas inlined. Use to discover required fields before calling create_entity or update_entity.
- **search_paths**: Search for available API paths in WorkIQ. Returns paths matching a regex filter. Use this to discover what entity paths are available before calling fetch, fetch_blob, create_entity, update_entity, or delete_entity tools. For example, search for 'messages' to find email-related paths, or 'calendar' for calendar paths. For file content (documents, images, photos — /content or $value endpoints), use fetch_blob.
- **call_function**: Call a WorkIQ function via HTTP GET. Functions compute or synthesize data rather than simply reading entities — e.g., getSchedule, delta, reminderView. Use get_schema to discover function parameters. WorkIQ entity paths borrow from the conventions of Microsoft Graph.
- **fetch**: Fetch one or more WorkIQ entities by path. Use entity paths discovered from ask responses or well-known paths like `/me/messages`. Returns JSON array with results for each path. WorkIQ entity paths borrow from the conventions of Microsoft Graph. Always include a $select query parameter with only the fields you need to reduce response size (e.g., `/me/messages?$select=id,subject,from`). For collection endpoints, include $top to limit results (e.g., `/me/messages?$select=id,subject&$top=10`). Some APIs do not support $top (e.g., `/me/chats/{id}/members`) — omit `$top` for those. Use the get-schema tool to discover available fields if unsure. For file content (documents, images, photos — e.g. `/content` or `$value` endpoints), use fetch_blob instead.
- **update_entity**: Update an existing WorkIQ entity by PATCHing JSON to its path. Use get_schema first to discover updatable fields. Only include fields you want to change. Returns the updated entity JSON. WorkIQ entity paths borrow from the conventions of Microsoft Graph.

### Consuming the ask tool

The `ask` tool is one of the most powerful and versatile tools provided by the Work IQ MCP server. It allows agents to query for information about emails, meetings, files, people, and other Microsoft 365 data. The tool abstracts the complexity of multiple Microsoft 365 APIs into a single, conversational interface.

When you call the `ask` tool, you provide a natural language question, and the Work IQ service processes it through the Work IQ intelligent engine. The response includes both plain text and structured content, making it easy for agents to extract specific information. Additionally, the `ask` tool supports multi-turn conversations by returning a `conversationId` that you can use to ask follow-up questions within the same conversation context.

#### Exercise: Ask "Who am I? What is my role in the company?"

In this exercise, you will use the MCP Inspector to interact with the `ask` tool and retrieve information about your identity and role in your organization.

**Step 1: Locate the ask tool in MCP Inspector**

1. In the MCP Inspector, navigate to the **Tools** tab if you're not already there.
2. You should see the `ask` tool listed among the Work IQ MCP server tools. Select it to view its schema and parameters.

**Step 2: Prepare your question**

The `ask` tool accepts a `question` parameter (required) and optionally an `agentId` parameter and `conversationId` for multi-turn scenarios. For this exercise, you only need to provide the question parameter.

**Step 3: Execute the tool call**

1. In the MCP Inspector, click on the `ask` tool to prepare a tool call.
2. In the **question** field, enter the following value:
  ```text
  Who am I? What is my role in the company?
  ```
3. Click the **Run Tool** button to invoke the tool.

**Step 4: Observe the response**

After executing the tool call, you will see:

- **Unstructured Content**: The response includes the answer as plain text content
- **Structured Content**: The response also includes structured content with an 'answer' field containing the formatted response, and a 'conversationId' field that you can use for multi-turn conversations to maintain context across follow-up questions

**Step 5: Try a follow-up question**

The `conversationId` from the previous structured response enables multi-turn conversations. Try asking a follow-up question in the same conversation context:

1. Call the `ask` tool again with your follow-up question.
2. Include the `conversationId` from the previous response to maintain context.
3. For example, use the following question:
  ```
  Who is my manager?
  ```

This demonstrates how Work IQ's MCP server enables natural, conversational interactions with Microsoft 365 data without requiring agents to understand the underlying APIs or resource paths.

### Consuming the getSchema tool

The `getSchema` tool is a powerful discovery mechanism that enables agents to understand the structure and requirements of Work IQ operations at runtime. Rather than relying on hardcoded knowledge, agents can query `getSchema` to discover what fields are available, which are required, and what data types they expect. This makes Work IQ truly self-describing and allows agents to adapt dynamically to changes in Microsoft 365 APIs without requiring updates to agent code.

When you call the `getSchema` tool with a Work IQ entity path or operation name, it returns the OpenAPI schema for that operation, including detailed metadata about request parameters, response structure, and field types. This is particularly useful when building queries — you can use `getSchema` to understand what fields you can fetch, what filters are available, and what the response will look like.

#### Exercise: Get the schema for `/me/messages`

In this exercise, you will use the MCP Inspector to retrieve the schema for the `/me/messages` endpoint and understand the structure of email messages in your mailbox.

**Step 1: Locate the getSchema tool in MCP Inspector**

1. In the MCP Inspector, navigate to the **Tools** tab.
2. Find and select the `getSchema` tool to view its parameters.

**Step 2: Prepare the schema query**

The `getSchema` tool accepts a `path` parameter that specifies which Work IQ operation you want to understand. For this exercise, you will request the schema for `/me/messages`.

**Step 3: Execute the tool call**

1. In the MCP Inspector, click on the `getSchema` tool.
2. In the **path** field, enter the following JSON:
  ```
  /me/messages
  ```
3. In the **operationType** field, enter the following JSON:
  ```
  fetch
  ```
4. Select the **Run Tool** command to invoke the tool.

**Step 4: Observe the schema response**

After executing the tool call, you will receive a detailed OpenAPI schema that includes:

- **Collection structure**: The response returns a `messageCollectionResponse` that contains:
  - `value`: An array of message objects
  - `@odata.count`: Total count of messages (optional)
  - `@odata.nextLink`: URL for pagination to retrieve the next set of results (optional)

- **Message object properties**: Each message in the array contains the following fields:
  - **Core identity**: `id`, `subject`, `conversationId`, `internetMessageId`
  - **Recipients and senders**: `from`, `sender`, `toRecipients`, `ccRecipients`, `bccRecipients`, `replyTo` (each contains email address and name)
  - **Content**: `body` (with `content` and `contentType` as "text" or "html"), `bodyPreview`, `uniqueBody`
  - **Timestamps**: `receivedDateTime`, `sentDateTime`, `createdDateTime`, `lastModifiedDateTime`
  - **Status flags**: `isRead`, `isDraft`, `hasAttachments`, `isDeliveryReceiptRequested`, `isReadReceiptRequested`
  - **Message properties**: `importance` (low/normal/high), `inferenceClassification` (focused/other), `categories`
  - **Advanced features**: `flag` (followup flag with status), `internetMessageHeaders`, `webLink`, `parentFolderId`
  - **Attachments and extensions**: `attachments`, `extensions`, `multiValueExtendedProperties`, `singleValueExtendedProperties`

**Step 5: Use the schema to build a fetch query**

Now that you understand the schema, you can use this information to construct a `fetch` tool call. For example:

1. Select the `fetch` tool
2. In the **entityUrls** field select **Add Item** and add the following entity URL:
  ```
  /me/messages?$top=10&$select=id,subject
  
  ```
3. Select **Run Tool** to get the output

This demonstrates how `getSchema` enables agents to discover the capabilities of Work IQ entities before acting on them, making interactions safer, more efficient, and more predictable.

## Wrap up

As you can see, you can consume Work IQ through its unified MCP server from any agent or application that supports MCP. This approach opens plenty of possibilities like integrating Work IQ with almost any agentic platform, enabling you to access the intelligent layer of Work IQ while leveraging standard MCP tools and patterns across your AI solutions.

## Where to go next

- **Explore the IQ Series** — Learn about Foundry IQ with [Episode 1: Foundry IQ: Unlocking Knowledge for your Agents](../../../Foundry-IQ/1-Foundry-IQ-Unlocking-Knowledge-for-Agents/).