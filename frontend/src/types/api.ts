export interface PropertyAddress {
  street: string
  city: string
  state: string
  zip_code: string
  county?: string
  parcel_number?: string
}

export interface Deed {
  deed_type: string
  grantor: string
  grantee: string
  recording_date: string
  document_number: string
  book_page?: string
}

export interface Lien {
  lien_type: string
  creditor: string
  amount?: number
  recording_date: string
  document_number: string
  status: string
}

export interface Encumbrance {
  encumbrance_type: string
  description: string
  recording_date: string
  document_number: string
}

export interface TitleSearchResult {
  search_id: string
  property_address: PropertyAddress
  status: string
  deeds: Deed[]
  liens: Lien[]
  encumbrances: Encumbrance[]
  created_at: string
  completed_at?: string
  risk_score?: number
}

export interface RiskScore {
  score_id: string
  search_id?: string
  property_address?: Record<string, string>
  overall_risk_score: number
  risk_level: string
  risk_factors: RiskFactor[]
  recommendations: string[]
  created_at: string
  model_version: string
}

export interface RiskFactor {
  factor_name: string
  factor_type: string
  severity: string
  description: string
  impact_score: number
  evidence?: Record<string, any>
}

export interface ComplianceReport {
  report_id: string
  search_id?: string
  property_address?: Record<string, any>
  jurisdiction: string
  checks: ComplianceCheck[]
  overall_status: string
  created_at: string
  checked_by: string
}

export interface ComplianceCheck {
  rule_name: string
  rule_type: string
  status: string
  description: string
  details?: Record<string, any>
  violations: string[]
  recommendations: string[]
}

