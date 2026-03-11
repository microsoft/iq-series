// ===============================================
// IQ Series — Foundry IQ Infrastructure
// Creates: Azure AI Search, Azure OpenAI (with model deployments),
//          AI Services (Foundry) with Foundry Project,
//          AI Search connection, and RBAC role assignments
// ===============================================

@description('Your user object ID (az ad signed-in-user show --query id -o tsv)')
param userObjectId string

@description('Resource name prefix')
param resourcePrefix string = 'iqseries'

@description('Azure region — must support agentic retrieval (see https://learn.microsoft.com/azure/search/search-region-support)')
param location string = 'eastus2'

@description('AI Search SKU')
@allowed(['basic', 'standard', 'standard2', 'standard3'])
param searchServiceSku string = 'standard'

@description('OpenAI service SKU')
@allowed(['S0'])
param openAiSku string = 'S0'

@description('AI Services SKU')
@allowed(['S0'])
param aiServicesSku string = 'S0'

@description('Embedding model name')
@allowed(['text-embedding-3-large'])
param embeddingModelName string = 'text-embedding-3-large'

@description('Embedding model version')
param embeddingModelVersion string = '1'

@description('Embedding model capacity (1K TPM per unit)')
@minValue(1)
@maxValue(200)
param embeddingModelCapacity int = 30

@description('Chat model name')
param chatModelName string = 'gpt-4o-mini'

@description('Chat model version')
param chatModelVersion string = '2024-07-18'

@description('Chat model capacity (1K TPM per unit)')
@minValue(1)
@maxValue(200)
param chatModelCapacity int = 30

// -----------------------------------------------
// Variables
// -----------------------------------------------

var uniqueSuffix = uniqueString(resourceGroup().id)

var names = {
  search: '${resourcePrefix}-search-${uniqueSuffix}'
  openAi: '${resourcePrefix}-openai-${uniqueSuffix}'
  aiServices: '${resourcePrefix}-ai-${uniqueSuffix}'
  project: '${resourcePrefix}-project'
  searchConnection: 'iq-series-search-connection'
  embeddingDeployment: 'text-embedding-3-large'
  chatDeployment: 'gpt-4o-mini'
}

// -----------------------------------------------
// RBAC role definition IDs
// -----------------------------------------------

var roles = {
  searchServiceContributor: '7ca78c08-252a-4471-8644-bb5ff32d4ba0'
  searchIndexDataContributor: '8ebe5a00-799e-43f5-93ac-243d3dce84a7'
  searchIndexDataReader: '1407120a-92aa-4202-b7e9-c0e197c71c8f'
  cognitiveServicesUser: 'a97b65f3-24c7-4388-baec-2e87135dc908'
  cognitiveServicesContributor: '25fbc0a9-bd7c-42a3-aa1a-3b75d497ee68'
  cognitiveServicesOpenAIUser: '5e0bd9bd-7b93-4f28-af87-19fc36ad61bd'
}

// ===============================================
// AZURE AI SEARCH
// ===============================================

resource searchService 'Microsoft.Search/searchServices@2023-11-01' = {
  name: names.search
  location: location
  sku: {
    name: searchServiceSku
  }
  properties: {
    replicaCount: 1
    partitionCount: 1
    hostingMode: 'default'
    publicNetworkAccess: 'enabled'
    disableLocalAuth: false
    authOptions: {
      aadOrApiKey: {
        aadAuthFailureMode: 'http401WithBearerChallenge'
      }
    }
    semanticSearch: 'standard'
  }
  identity: {
    type: 'SystemAssigned'
  }
}

// ===============================================
// AZURE OPENAI SERVICE
// ===============================================

resource openAiService 'Microsoft.CognitiveServices/accounts@2023-10-01-preview' = {
  name: names.openAi
  location: location
  sku: {
    name: openAiSku
  }
  kind: 'OpenAI'
  properties: {
    customSubDomainName: names.openAi
    networkAcls: {
      defaultAction: 'Allow'
    }
    publicNetworkAccess: 'Enabled'
    disableLocalAuth: false
  }
  identity: {
    type: 'SystemAssigned'
  }
}

// ===============================================
// AI SERVICES (FOUNDRY)
// ===============================================

resource aiServices 'Microsoft.CognitiveServices/accounts@2025-06-01' = {
  name: names.aiServices
  location: location
  sku: {
    name: aiServicesSku
  }
  kind: 'AIServices'
  properties: {
    customSubDomainName: names.aiServices
    allowProjectManagement: true
    networkAcls: {
      defaultAction: 'Allow'
    }
    publicNetworkAccess: 'Enabled'
    disableLocalAuth: false
  }
  identity: {
    type: 'SystemAssigned'
  }
}

// ===============================================
// FOUNDRY PROJECT
// ===============================================

resource project 'Microsoft.CognitiveServices/accounts/projects@2025-06-01' = {
  parent: aiServices
  name: names.project
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    displayName: 'IQ Series Foundry Project'
    description: 'Project for running the IQ Series cookbooks'
  }
}

// ===============================================
// AI SEARCH CONNECTION (Project → AI Search)
// ===============================================

resource searchConnection 'Microsoft.CognitiveServices/accounts/projects/connections@2025-06-01' = {
  parent: project
  name: names.searchConnection
  properties: {
    category: 'CognitiveSearch'
    authType: 'AAD'
    target: 'https://${searchService.name}.search.windows.net'
    isSharedToAll: true
    metadata: {
      ApiType: 'Azure'
      ResourceId: searchService.id
    }
  }
}

// ===============================================
// MODEL DEPLOYMENTS
// ===============================================

resource embeddingDeployment 'Microsoft.CognitiveServices/accounts/deployments@2023-10-01-preview' = {
  parent: openAiService
  name: names.embeddingDeployment
  properties: {
    model: {
      format: 'OpenAI'
      name: embeddingModelName
      version: embeddingModelVersion
    }
    raiPolicyName: 'Microsoft.Default'
  }
  sku: {
    name: 'Standard'
    capacity: embeddingModelCapacity
  }
}

resource chatDeployment 'Microsoft.CognitiveServices/accounts/deployments@2023-10-01-preview' = {
  parent: openAiService
  name: names.chatDeployment
  properties: {
    model: {
      format: 'OpenAI'
      name: chatModelName
      version: chatModelVersion
    }
    raiPolicyName: 'Microsoft.Default'
  }
  sku: {
    name: 'GlobalStandard'
    capacity: chatModelCapacity
  }
  dependsOn: [
    embeddingDeployment
  ]
}

// ===============================================
// SERVICE PRINCIPAL ROLE ASSIGNMENTS
// (AI Search managed identity → OpenAI & AI Services)
// ===============================================

resource searchToOpenAI_CogServicesUser 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(subscription().id, searchService.name, roles.cognitiveServicesOpenAIUser)
  properties: {
    principalId: searchService.identity.principalId
    principalType: 'ServicePrincipal'
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', roles.cognitiveServicesOpenAIUser)
  }
}

resource searchToAIServices_CogServicesUser 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(subscription().id, searchService.name, roles.cognitiveServicesUser)
  properties: {
    principalId: searchService.identity.principalId
    principalType: 'ServicePrincipal'
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', roles.cognitiveServicesUser)
  }
}

// ===============================================
// USER ROLE ASSIGNMENTS
// ===============================================

// Search Service Contributor
resource userRole_searchContributor 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(resourceGroup().id, searchService.name, userObjectId, roles.searchServiceContributor)
  scope: searchService
  properties: {
    principalId: userObjectId
    principalType: 'User'
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', roles.searchServiceContributor)
  }
}

// Search Index Data Reader
resource userRole_searchIndexReader 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(resourceGroup().id, searchService.name, userObjectId, roles.searchIndexDataReader)
  scope: searchService
  properties: {
    principalId: userObjectId
    principalType: 'User'
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', roles.searchIndexDataReader)
  }
}

// Search Index Data Contributor
resource userRole_searchIndexContributor 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(resourceGroup().id, searchService.name, userObjectId, roles.searchIndexDataContributor)
  scope: searchService
  properties: {
    principalId: userObjectId
    principalType: 'User'
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', roles.searchIndexDataContributor)
  }
}

// Cognitive Services Contributor (OpenAI)
resource userRole_openAiContributor 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(resourceGroup().id, openAiService.name, userObjectId, roles.cognitiveServicesContributor)
  scope: openAiService
  properties: {
    principalId: userObjectId
    principalType: 'User'
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', roles.cognitiveServicesContributor)
  }
}

// Cognitive Services Contributor (AI Services / Foundry)
resource userRole_aiServicesContributor 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(resourceGroup().id, aiServices.name, userObjectId, roles.cognitiveServicesContributor)
  scope: aiServices
  properties: {
    principalId: userObjectId
    principalType: 'User'
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', roles.cognitiveServicesContributor)
  }
}

// ===============================================
// DATA SEEDING (Deployment Script)
// Creates search index, uploads sample data,
// knowledge source, and knowledge base so the
// MCP endpoint is ready to use immediately
// ===============================================

@description('Seed sample data and create knowledge base during deployment')
param seedData bool = true

resource seedIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = if (seedData) {
  name: '${resourcePrefix}-seed-${uniqueSuffix}'
  location: location
}

// Grant the seed identity Search Service Contributor on the search service
resource seedRole_searchContributor 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (seedData) {
  name: guid(resourceGroup().id, searchService.name, 'seed', roles.searchServiceContributor)
  scope: searchService
  properties: {
    principalId: seedData ? seedIdentity.properties.principalId : ''
    principalType: 'ServicePrincipal'
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', roles.searchServiceContributor)
  }
}

// Grant the seed identity Search Index Data Contributor on the search service
resource seedRole_searchIndexContributor 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (seedData) {
  name: guid(resourceGroup().id, searchService.name, 'seed', roles.searchIndexDataContributor)
  scope: searchService
  properties: {
    principalId: seedData ? seedIdentity.properties.principalId : ''
    principalType: 'ServicePrincipal'
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', roles.searchIndexDataContributor)
  }
}

// Grant the seed identity Cognitive Services User on the OpenAI service
// (required for knowledge base model validation)
resource seedRole_cogServicesUser 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (seedData) {
  name: guid(resourceGroup().id, openAiService.name, 'seed', roles.cognitiveServicesUser)
  scope: openAiService
  properties: {
    principalId: seedData ? seedIdentity.properties.principalId : ''
    principalType: 'ServicePrincipal'
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', roles.cognitiveServicesUser)
  }
}

resource seedDataScript 'Microsoft.Resources/deploymentScripts@2023-08-01' = if (seedData) {
  name: '${resourcePrefix}-seed-data'
  location: location
  kind: 'AzureCLI'
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${seedIdentity.id}': {}
    }
  }
  properties: {
    azCliVersion: '2.61.0'
    retentionInterval: 'PT1H'
    cleanupPreference: 'OnSuccess'
    timeout: 'PT15M'
    forceUpdateTag: uniqueSuffix
    scriptContent: loadTextContent('scripts/seed-data.sh')
    environmentVariables: [
      { name: 'SEARCH_ENDPOINT', value: 'https://${searchService.name}.search.windows.net' }
      { name: 'AOAI_ENDPOINT', value: openAiService.properties.endpoint }
      { name: 'EMBEDDING_MODEL', value: embeddingModelName }
      { name: 'EMBEDDING_DEPLOYMENT', value: names.embeddingDeployment }
      { name: 'GPT_MODEL', value: chatModelName }
      { name: 'GPT_DEPLOYMENT', value: names.chatDeployment }
    ]
  }
  dependsOn: [
    seedRole_searchContributor
    seedRole_searchIndexContributor
    seedRole_cogServicesUser
    embeddingDeployment
    chatDeployment
  ]
}

// ===============================================
// OUTPUTS
// ===============================================

@description('AI Search endpoint')
output searchEndpoint string = 'https://${searchService.name}.search.windows.net'

@description('AI Search admin API key')
output searchApiKey string = searchService.listAdminKeys().primaryKey

@description('Azure OpenAI endpoint')
output openAiEndpoint string = openAiService.properties.endpoint

@description('AI Services endpoint')
output aiServicesEndpoint string = aiServices.properties.endpoint

@description('AI Services name')
output aiServicesName string = aiServices.name

@description('Embedding deployment name')
output embeddingDeploymentName string = embeddingDeployment.name

@description('Chat deployment name')
output chatDeploymentName string = chatDeployment.name

@description('Search service name')
output searchServiceName string = searchService.name

@description('OpenAI service name')
output openAiServiceName string = openAiService.name

@description('Foundry project endpoint')
output foundryProjectEndpoint string = 'https://${names.aiServices}.services.ai.azure.com/api/projects/${project.name}'

@description('AI Search connection name (use in .env)')
output searchConnectionName string = searchConnection.name

@description('Resource location')
output resourceLocation string = location

@description('Knowledge base name (for MCP endpoint)')
output knowledgeBaseName string = 'earth-knowledge-base'

@description('MCP endpoint URL (connect agents to the knowledge base)')
output mcpEndpoint string = 'https://${searchService.name}.search.windows.net/knowledgebases/earth-knowledge-base/mcp'
