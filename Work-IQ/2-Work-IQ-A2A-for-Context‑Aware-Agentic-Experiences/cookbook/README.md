# Episode 2 Cookbook: A2A for Context‑Aware, Agentic Experiences

This folder contains the hands-on cookbook for Episode 2 of The Work IQ Series.

## 📋 Prerequisites

- **Microsoft 365 Tenant** with proper licensing
- **.NET SDK 8** or later installed
- **Microsoft Entra app registration** with delegated `WorkIQAgent.Ask`
  permission and admin consent
- **Work IQ** enabled in your target tenant with **Administrative consent** for the **Work IQ application**

## 🛠️ Set up the supported Work IQ A2A sample

Work IQ CLI 1.0 does not expose the legacy `a2aserver` command. Episode 2
uses Microsoft's current Work IQ A2A sample, which connects directly to the
hosted Work IQ A2A gateway.

1. Follow the app registration and delegated permission steps in the
   [Work IQ A2A quickstart](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/work-iq/a2a/quickstart).
1. Record the application ID and tenant ID.
1. Clone the official samples:

   ```bash
   git clone https://github.com/microsoft/work-iq-samples.git
   ```

The lab runs the `dotnet/a2a` sample. A raw JSON-RPC implementation is also
available under `dotnet/a2a-raw`.

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

The [**Work IQ Lab for Episode 02**](./work-iq-lab02.md) walks you through the basic capabilities of Work IQ A2A, step by step:

1. Starting the current Microsoft Work IQ A2A sample
1. Asking a prompt via Work IQ A2A
1. Asking a second prompt within the same A2A conversation context
1. Inspecting the raw JSON-RPC sample

## Additional Resources

- [Episode 2 README](../README.md)
- [Work IQ overview](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/work-iq)
- [Work IQ A2A quickstart](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/work-iq/a2a/quickstart)
- [Work IQ samples](https://github.com/microsoft/work-iq-samples)
- [Copilot Dev Camp - Work IQ](https://microsoft.github.io/copilot-camp/pages/work-iq/)
