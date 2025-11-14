/**
 * Type definitions for Record Linkage application
 */

export interface RecordBase {
  id?: string;
  fields: Record<string, string>;
}

export interface RecordPair {
  record_a: RecordBase;
  record_b: RecordBase;
}

export interface MatchPrediction {
  is_match: boolean;
  match_probability: number;
  confidence: 'High' | 'Medium' | 'Low';
  similarity_score: number;
}

export interface FeatureContribution {
  field_name: string;
  contribution: number;
  value_a: string;
  value_b: string;
}

export interface TokenContribution {
  token: string;
  contribution: number;
  position: number;
}

export interface Explanation {
  method: 'SHAP' | 'LIME';
  feature_contributions: FeatureContribution[];
  token_contributions?: TokenContribution[];
  top_positive_features: string[];
  top_negative_features: string[];
}

export interface MatchResult {
  prediction: MatchPrediction;
  explanation?: Explanation;
  record_pair: RecordPair;
}

export interface BatchMatchRequest {
  dataset_a: RecordBase[];
  dataset_b: RecordBase[];
  threshold?: number;
  include_explanations: boolean;
}

export interface BatchMatchResult {
  total_comparisons: number;
  matches_found: number;
  match_results: MatchResult[];
  processing_time: number;
}

export interface DatasetInfo {
  name: string;
  description: string;
  num_records: number;
  fields: string[];
  sample_records?: RecordBase[];
}

export interface HealthCheck {
  status: string;
  version: string;
  model_loaded: boolean;
  device: string;
}

export interface ErrorResponse {
  error: string;
  detail?: string;
  status_code: number;
}
