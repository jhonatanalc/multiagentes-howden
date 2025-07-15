import {
	IExecuteFunctions,
	INodeExecutionData,
	INodeType,
	INodeTypeDescription,
	NodeOperationError,
} from 'n8n-workflow';

import { OptionsWithUri } from 'request';

export class AgenticRag implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Agentic RAG',
		name: 'agenticRag',
		icon: 'file:agenticrag.svg',
		group: ['transform'],
		version: 1,
		subtitle: '={{$parameter["operation"] + ": " + $parameter["resource"]}}',
		description: 'Interact with Agentic RAG Knowledge Graph',
		defaults: {
			name: 'Agentic RAG',
		},
		inputs: ['main'],
		outputs: ['main'],
		credentials: [
			{
				name: 'agenticRagApi',
				required: false,
			},
		],
		properties: [
			{
				displayName: 'Resource',
				name: 'resource',
				type: 'options',
				noDataExpression: true,
				options: [
					{
						name: 'Chat',
						value: 'chat',
					},
					{
						name: 'Search',
						value: 'search',
					},
					{
						name: 'Document',
						value: 'document',
					},
				],
				default: 'chat',
			},
			{
				displayName: 'Operation',
				name: 'operation',
				type: 'options',
				noDataExpression: true,
				displayOptions: {
					show: {
						resource: ['chat'],
					},
				},
				options: [
					{
						name: 'Send Message',
						value: 'sendMessage',
						description: 'Send a message to the agentic RAG system',
						action: 'Send a message',
					},
				],
				default: 'sendMessage',
			},
			{
				displayName: 'Operation',
				name: 'operation',
				type: 'options',
				noDataExpression: true,
				displayOptions: {
					show: {
						resource: ['search'],
					},
				},
				options: [
					{
						name: 'Vector Search',
						value: 'vectorSearch',
						description: 'Perform vector similarity search',
						action: 'Perform vector search',
					},
					{
						name: 'Graph Search',
						value: 'graphSearch',
						description: 'Search the knowledge graph',
						action: 'Search knowledge graph',
					},
					{
						name: 'Hybrid Search',
						value: 'hybridSearch',
						description: 'Perform hybrid search combining vector and graph',
						action: 'Perform hybrid search',
					},
				],
				default: 'vectorSearch',
			},
			{
				displayName: 'Message',
				name: 'message',
				type: 'string',
				displayOptions: {
					show: {
						resource: ['chat'],
						operation: ['sendMessage'],
					},
				},
				default: '',
				description: 'The message to send to the agentic RAG system',
			},
			{
				displayName: 'Session ID',
				name: 'sessionId',
				type: 'string',
				displayOptions: {
					show: {
						resource: ['chat'],
						operation: ['sendMessage'],
					},
				},
				default: '',
				description: 'Session ID for conversation context (optional)',
			},
			{
				displayName: 'Query',
				name: 'query',
				type: 'string',
				displayOptions: {
					show: {
						resource: ['search'],
					},
				},
				default: '',
				description: 'Search query',
			},
			{
				displayName: 'Limit',
				name: 'limit',
				type: 'number',
				displayOptions: {
					show: {
						resource: ['search'],
					},
				},
				default: 10,
				description: 'Maximum number of results to return',
			},
			{
				displayName: 'Stream Response',
				name: 'stream',
				type: 'boolean',
				displayOptions: {
					show: {
						resource: ['chat'],
						operation: ['sendMessage'],
					},
				},
				default: false,
				description: 'Whether to stream the response',
			},
		],
	};

	async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
		const items = this.getInputData();
		const returnData: INodeExecutionData[] = [];

		const credentials = await this.getCredentials('agenticRagApi');
		const baseUrl = credentials.baseUrl as string;
		const apiKey = credentials.apiKey as string;

		for (let i = 0; i < items.length; i++) {
			const resource = this.getNodeParameter('resource', i) as string;
			const operation = this.getNodeParameter('operation', i) as string;

			let responseData;

			if (resource === 'chat') {
				if (operation === 'sendMessage') {
					const message = this.getNodeParameter('message', i) as string;
					const sessionId = this.getNodeParameter('sessionId', i) as string;
					const stream = this.getNodeParameter('stream', i) as boolean;

					const body: any = {
						message,
						session_id: sessionId || undefined,
					};

					const options: OptionsWithUri = {
						method: 'POST',
						uri: `${baseUrl}/chat`,
						body,
						json: true,
						headers: {},
					};

					if (apiKey) {
						options.headers!['Authorization'] = `Bearer ${apiKey}`;
					}

					if (stream) {
						// Para streaming, necesitaríamos implementar manejo especial
						// Por ahora, usaremos la respuesta normal
						body.stream = false;
					}

					responseData = await this.helpers.request(options);
				}
			} else if (resource === 'search') {
				const query = this.getNodeParameter('query', i) as string;
				const limit = this.getNodeParameter('limit', i) as number;

				let endpoint = '';
				const body: any = { query, limit };

				switch (operation) {
					case 'vectorSearch':
						endpoint = '/search/vector';
						break;
					case 'graphSearch':
						endpoint = '/search/graph';
						break;
					case 'hybridSearch':
						endpoint = '/search/hybrid';
						break;
					default:
						throw new NodeOperationError(this.getNode(), `Unknown operation: ${operation}`);
				}

				const options: OptionsWithUri = {
					method: 'POST',
					uri: `${baseUrl}${endpoint}`,
					body,
					json: true,
					headers: {},
				};

				if (apiKey) {
					options.headers!['Authorization'] = `Bearer ${apiKey}`;
				}

				responseData = await this.helpers.request(options);
			}

			if (Array.isArray(responseData)) {
				returnData.push.apply(returnData, responseData as INodeExecutionData[]);
			} else {
				returnData.push({
					json: responseData,
				});
			}
		}

		return [returnData];
	}
}