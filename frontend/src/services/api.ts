/**
 * API client for Record Linkage backend
 */

import axios, { AxiosInstance } from 'axios';
import type {
  RecordPair,
  MatchResult,
  BatchMatchRequest,
  BatchMatchResult,
  DatasetInfo,
  HealthCheck,
} from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const API_V1 = `${API_BASE_URL}/api/v1`;

class RecordLinkageAPI {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_V1,
      headers: {
        'Content-Type': 'application/json',
      },
      timeout: 30000, // 30 seconds
    });

    // Add response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        console.error('API Error:', error);
        return Promise.reject(error);
      }
    );
  }

  // Health Check
  async healthCheck(): Promise<HealthCheck> {
    const response = await this.client.get<HealthCheck>('/health');
    return response.data;
  }

  // Dataset Management
  async listDatasets(): Promise<DatasetInfo[]> {
    const response = await this.client.get<DatasetInfo[]>('/datasets/');
    return response.data;
  }

  async getDatasetInfo(
    datasetName: string,
    includeSamples: boolean = true
  ): Promise<DatasetInfo> {
    const response = await this.client.get<DatasetInfo>(
      `/datasets/${datasetName}`,
      {
        params: { include_samples: includeSamples },
      }
    );
    return response.data;
  }

  async uploadDataset(file: File): Promise<{ status: string; filename: string }> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await this.client.post('/datasets/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  }

  // Matching
  async predictMatch(
    recordPair: RecordPair,
    includeExplanation: boolean = true
  ): Promise<MatchResult> {
    const response = await this.client.post<MatchResult>('/match/predict', recordPair, {
      params: {
        include_explanation: includeExplanation,
      },
    });
    return response.data;
  }

  async batchMatch(request: BatchMatchRequest): Promise<BatchMatchResult> {
    const response = await this.client.post<BatchMatchResult>('/match/batch', request);
    return response.data;
  }

  async optimizeThreshold(datasetName: string): Promise<{ optimal_threshold: number }> {
    const response = await this.client.get(`/match/threshold/optimize`, {
      params: { dataset_name: datasetName },
    });
    return response.data;
  }
}

// Export singleton instance
export const api = new RecordLinkageAPI();
export default api;
