export interface Vendor {
  slug: string;           // vendor--family slug (e.g. "abeo-solutions-inc--crystal-practice-management")
  developer: string;      // developer/vendor name from metadata
  family: string;         // product family name from metadata
  product_name: string;   // focus product from summary (e.g. "Crystal Practice Management v6.0")
  summary: string;        // zagat-style summary
  holistic_score: number;
  chpl_ids: number[];
  has_analysis: boolean;
  has_research: boolean;
  has_report: boolean;
  analysis_files: string[];
  download_files: string[];
}
