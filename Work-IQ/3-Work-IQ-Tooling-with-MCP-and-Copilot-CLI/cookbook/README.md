# Episode 3 Cookbook: Tooling with MCP & Copilot CLI

This folder contains the hands-on cookbook for Episode 3 of The Work IQ Series.

## 📋 Prerequisites

- **Microsoft 365 Tenant** with proper licensing
- **Node.js** 22 or later installed
- **MCP Inspector** downloaded and running on your environment
- **Work IQ** enabled in your target tenant with **Administrative consent** for the **Work IQ application**

## 🛠️ Downloading and running MCP Inspector

**MCP Inspector** is an open-source, web-based tool for visualizing, debugging, and validating MCP protocol interactions. It helps you inspect tools, resources, and prompts offered by an MCP server.

The official GitHub repository is: [https://github.com/modelcontextprotocol/inspector](https://github.com/modelcontextprotocol/inspector)

---

### Prerequisites

- Node.js ^22.7.5 and npm

---

### 1. Start MCP Inspector

```sh
npx @modelcontextprotocol/inspector
```

Once the tool is running, it will open your browser and show you the MCP Inspector user interface.

## ⚙️ Enabling Work IQ in your tenant

Follow this brief enablement flow as a tenant admin:

1. Verify licensing requirements are satisfied for users who need Work IQ. You can find additional details about the licensing model in the article [Understand usage-based billing and cost management for Copilot Credits](https://learn.microsoft.com/en-us/microsoft-365/copilot/usage-based-billing-overview-copilot-credits)
1. Ensure you have a **Global Administrator** role in your organization.
1. Create the Work IQ service principal in your organization using one of these methods:

   **Option A: Using Graph Explorer (Admin center)**
   - Go to [Graph Explorer](https://aka.ms/ge) and sign in with an admin account.
   - Set the method to **POST** and the URL to `https://graph.microsoft.com/v1.0/servicePrincipals`.
   - Select **Modify permissions** and consent to `Application.ReadWrite.All`.
   - Enter the following in the **Request body**:
     ```json
     {
       "appId": "fdcc1f02-fc51-4226-8753-f668596af7f7"
     }
     ```
   - Select **Run query**. A **201 Created** response confirms success.

   **Option B: Using Azure CLI**
   ```bash
   az ad sp create --id fdcc1f02-fc51-4226-8753-f668596af7f7
   ```

Your tenant is now ready to use Work IQ. For complete prerequisites, detailed instructions, and troubleshooting, see the [full Work IQ enablement guide](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/work-iq/enable-work-iq).

## 📓 Lab Instructions

The [**Work IQ Lab for Episode 03**](./work-iq-lab03.md) walks you through the basic capabilities of Work IQ MCP, step by step:

1. Asking a prompt via Work IQ MCP
1. Reading the schema of a resource via Work IQ MCP
1. Fetching a resource via Work IQ MCP
1. Creating an event in your caldendar via Work IQ MCP

## Additional Resources

- [Episode 3 README](../README.md)
- [Work IQ overview](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/work-iq)
- [Copilot Dev Camp - Work IQ](https://microsoft.github.io/copilot-camp/pages/work-iq/)
