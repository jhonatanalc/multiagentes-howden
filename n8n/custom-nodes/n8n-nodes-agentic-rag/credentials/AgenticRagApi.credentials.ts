import {
	ICredentialType,
	INodeProperties,
} from 'n8n-workflow';

export class AgenticRagApi implements ICredentialType {
	name = 'agenticRagApi';
	displayName = 'Agentic RAG API';
	documentationUrl = 'https://github.com/howden/agentic-rag-knowledge-graph';
	properties: INodeProperties[] = [
		{
			displayName: 'API Base URL',
			name: 'baseUrl',
			type: 'string',
			default: 'http://localhost:8058',
			description: 'Base URL of the Agentic RAG API',
		},
		{
			displayName: 'API Key',
			name: 'apiKey',
			type: 'string',
			typeOptions: {
				password: true,
			},
			default: '',
			description: 'API Key for authentication (if required)',
		},
	];
}