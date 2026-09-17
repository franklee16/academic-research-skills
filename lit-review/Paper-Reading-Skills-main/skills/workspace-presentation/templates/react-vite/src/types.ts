export type DisplayCategory = "primary-display" | "summarize-then-link" | "link-only";

export interface PresentationManifest {
  schemaVersion: number;
  presentation: {
    title: string;
    slug: string;
    generatedAt: string;
    sourceKind: string;
    sourcePath: string;
    sourceLabel?: string;
    status?: string;
    description?: string;
  };
  sections: PresentationSection[];
  modules: PresentationModule[];
  sourceFileIds: string[];
  warnings?: string[];
}

export interface PresentationSection {
  id: string;
  title: string;
  kind?: string;
  summaryFile?: string;
}

export interface PresentationModule {
  id: string;
  sectionId: string;
  title: string;
  workflow?: string;
  displayCategory: DisplayCategory;
  summaryFile?: string;
  sourceFileIds: string[];
}

export interface SourceIndex {
  schemaVersion: number;
  sourceRoot?: string;
  files: SourceFile[];
}

export interface SourceFile {
  id: string;
  label: string;
  path: string;
  relativePath?: string;
  readUrl?: string;
  openHref?: string;
  workflow?: string;
  displayCategory?: DisplayCategory;
  exists?: boolean;
}

export interface ModuleSummary {
  schemaVersion: number;
  moduleId: string;
  title: string;
  displayCategory: DisplayCategory;
  sourceFileIds: string[];
  summary: string;
  status?: string;
  takeaways?: string[];
  structuredItems?: StructuredItem[];
  risks?: RiskItem[];
  nextActions?: NextAction[];
  missingSources?: string[];
}

export interface StructuredItem {
  label: string;
  kind?: string;
  status?: string;
  value: string;
  sourceFileIds?: string[];
}

export interface RiskItem {
  label: string;
  severity?: "low" | "medium" | "high";
  description: string;
  sourceFileIds?: string[];
}

export interface NextAction {
  label: string;
  status?: string;
  sourceFileIds?: string[];
}
