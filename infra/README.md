# Deploy to Your Own Azure Subscription

This folder contains the infrastructure-as-code to deploy all Azure resources needed for The IQ Series cookbooks.

## One-Click Deploy

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://aka.ms/iq-series/deploytoazure)

Click the button above to deploy directly from the Azure Portal. You'll be prompted for:
- **User Object ID** — run `az ad signed-in-user show --query id -o tsv` to get yours
- **Resource Prefix** — a short name prefix for all resources (default: `iqs`)
- **Location** — Azure region (must support [agentic retrieval](https://learn.microsoft.com/azure/search/search-region-support))

The default chat model is `gpt-5.4-mini`, version `2026-03-17`. You can override **Chat Model Name** and **Chat Model Version** in the portal for a model/version supported in your region and subscription. The chat deployment name follows **Chat Model Name** on both the Azure OpenAI and Foundry resources. After redeploying existing resources, update your cookbook `.env` values to match the deployment outputs.

Sample data is seeded automatically by an **Azure Container Apps Consumption runner** using managed identity. It creates the `earth-at-night` index, uploads the NASA sample documents, and creates `earth-knowledge-source` and `earth-knowledge-base`. It uses no Azure Files mount, storage account keys, or deployment-script storage account.

The runner's internal-only readiness endpoint opens only after seeding is verified. Permission-propagation failures are retried for up to 10 minutes per operation; other failures surface in the runner's console logs and prevent readiness. The runner scales to zero when idle; a subsequent cold start safely repeats the setup. Set **Seed Data** to `false` only if you intentionally want infrastructure without sample data.

If seeding fails, open the Container App named by the **seedRunnerName** deployment output and inspect **Monitoring > Log stream** (console and system logs). Fix the reported error and redeploy or restart its revision. Do not treat a partial deployment as a ready-to-use knowledge base.

After deployment, copy the output values from the portal and create a `.env` file **inside each episode's `cookbook/` folder** (e.g., `1-Foundry-IQ-Unlocking-Knowledge-for-Agents/cookbook/.env`):

```
SEARCH_ENDPOINT=<searchEndpoint output>
AOAI_ENDPOINT=<openAiEndpoint output>
AOAI_EMBEDDING_MODEL=text-embedding-3-large
AOAI_EMBEDDING_DEPLOYMENT=text-embedding-3-large
AOAI_GPT_MODEL=gpt-5.4-mini
AOAI_GPT_DEPLOYMENT=gpt-5.4-mini
FOUNDRY_PROJECT_ENDPOINT=<foundryProjectEndpoint output>
FOUNDRY_MODEL_DEPLOYMENT_NAME=gpt-5.4-mini
AZURE_AI_SEARCH_CONNECTION_NAME=<searchConnectionName output>
```

## What Gets Deployed

| Resource | Purpose |
|----------|---------|
| **Azure AI Search** (Standard) | Vector search, semantic ranking, agentic retrieval |
| **Azure OpenAI** | `text-embedding-3-large` + `gpt-5.4-mini` model deployments |
| **Azure AI Services** | Foundry resource with project management enabled |
| **Foundry Project** | Project for running the IQ Series cookbooks |
| **AI Search Connection** | Connects the Foundry project to your AI Search service |
| **RBAC Role Assignments** | Proper permissions for your user + service-to-service access |
| **Container Apps environment + seeding app** | Keyless automatic setup, readiness checks, and scale-to-zero (when `seedData=true`) |

## 📋 Prerequisites

- **Azure Subscription** with permissions to create resources and assign roles
- The `Microsoft.App` resource provider registered for automatic seeding
- **Azure CLI** installed and configured ([Install guide](https://learn.microsoft.com/cli/azure/install-azure-cli))
- **Python 3.10+** installed
- A region that supports [agentic retrieval](https://learn.microsoft.com/azure/search/search-region-support) (default: `eastus`)

## 🚀 Quick Start

### 1. Login to Azure

```bash
az login
```

### 2. Deploy Infrastructure

⏱️ Estimated time: 10-20 minutes, including automatic seeding and permission propagation

**macOS / Linux:**

```bash
cd infra
./deploy.sh -g "iq-series-rg" -l "eastus"
```

**Windows (PowerShell):**

```powershell
cd infra
.\deploy.ps1 -ResourceGroupName "iq-series-rg" -Location "eastus"
```

This will:
- Create the resource group
- Deploy all Azure resources via Bicep
- Set up RBAC role assignments
- Seed the sample index, documents, knowledge source, and knowledge base automatically
- Generate a `.env` file in the repo root with all endpoints

### 3. Run the Cookbooks

From the `infra` directory, copy the generated configuration into the cookbook folder.

**macOS / Linux:**

```bash
cp ../.env ../Foundry-IQ/1-Foundry-IQ-Unlocking-Knowledge-for-Agents/cookbook/.env
cd ../Foundry-IQ/1-Foundry-IQ-Unlocking-Knowledge-for-Agents/cookbook/
# Open foundry-iq-cookbook.ipynb in VS Code or Jupyter
```

**Windows (PowerShell):**

```powershell
Copy-Item -LiteralPath ..\.env -Destination ..\Foundry-IQ\1-Foundry-IQ-Unlocking-Knowledge-for-Agents\cookbook\.env
Set-Location ..\Foundry-IQ\1-Foundry-IQ-Unlocking-Knowledge-for-Agents\cookbook
# Open foundry-iq-cookbook.ipynb in VS Code or Jupyter
```

The notebooks automatically read the `.env` file in their cookbook folder.

## Updating the Deployment Template

`main.bicep` is the source of truth. When changing the default chat model:

1. Update `chatModelName` and `chatModelVersion` in `main.bicep` and `main.parameters.json`.
2. Regenerate the portal template from the repository root:

   ```powershell
   az bicep build --file infra\main.bicep --outfile infra\azuredeploy.json
   ```

3. Update the `AOAI_GPT_MODEL` example above and commit the source, parameters, and generated template together.
4. Merge the changes into `main` in `microsoft/iq-series`. The shared Deploy to Azure short link loads `infra/azuredeploy.json` from that repository and branch, so changes in a local checkout, fork, or unmerged branch do not change the button's defaults.

Do not edit only `azuredeploy.json`: the next Bicep build would overwrite those changes. Pinned model defaults still need maintenance as models retire; review [model retirements](https://learn.microsoft.com/azure/ai-foundry/openai/concepts/model-retirements) and model availability before choosing a replacement.

## 🧹 Cleanup

Delete all resources to avoid ongoing charges:

```bash
az group delete --name iq-series-rg --yes --no-wait
```

## 📁 Files

| File | Description |
|------|-------------|
| `main.bicep` | Bicep template defining all Azure resources |
| `azuredeploy.json` | Generated ARM template loaded by the Deploy to Azure button |
| `main.parameters.json` | Default parameter values |
| `deploy.sh` | Deployment script for macOS/Linux |
| `deploy.ps1` | Deployment script for Windows PowerShell |
| `scripts/seed_data.py` | Idempotent managed-identity seeding and readiness endpoint |
| `scripts/seed-data.sh` | Installs dependencies and starts the seeder |
| `scripts/requirements.txt` | Seeding dependencies embedded in the portal template |

After changing any seeding file, rebuild `azuredeploy.json` as above: the runner's code and dependencies are embedded in the template, so one-click deployment does not download scripts from a branch.
