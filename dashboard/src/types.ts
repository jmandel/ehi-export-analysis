export interface Vendor {
  slug: string;           // vendor--family slug (e.g. "abeo-solutions-inc--crystal-practice-management")
  developer: string;      // developer/vendor name from metadata
  family: string;         // product family name from metadata
  product_name: string;   // focus product from summary (e.g. "Crystal Practice Management v6.0")
  summary: string;        // zagat-style summary
  holistic_score: number;
  export_fidelity: string;       // "native" | "mapped_comprehensive" | "mapped_limited" | "standard_only"
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
