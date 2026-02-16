export interface Vendor {
  slug: string;           // vendor--family slug (e.g. "abeo-solutions-inc--crystal-practice-management")
  developer: string;      // developer/vendor name from metadata
  family: string;         // product family name from metadata
  product_name: string;   // focus product from summary (e.g. "Crystal Practice Management v6.0")
  summary: string;        // zagat-style summary
  grade: string;          // letter grade: "A" | "A-" | "B+" | ... | "F"
  coverage: string;       // "comprehensive" | "partial" | "minimal_stub_unclear"
  approach: string;       // "native" | "standards_based" | "hybrid" | "unclear"
  export_formats: string[];
  entity_count: number | null;
  field_count: number | null;
  has_data_dictionary: boolean;
  has_sample_data: boolean;
  billing_included: boolean | null;
  patient_communications: string; // "not_applicable" | "included" | "partial" | "excluded" | "unclear"
  chpl_ids: number[];
  ehi_documentation_url: string;
  has_analysis: boolean;
  has_research: boolean;
  has_report: boolean;
  has_entity_inventory: boolean;
  has_analysis_stats: boolean;
  analysis_files: string[];
  download_files: string[];
}
