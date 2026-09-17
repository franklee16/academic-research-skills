import type { ModuleSummary, PresentationManifest, SourceIndex } from "./types";

const baseUrl = import.meta.env.BASE_URL ?? "/";

function publicUrl(path: string): string {
  return `${baseUrl}${path.replace(/^\/+/, "")}`;
}

export async function fetchJson<T>(path: string): Promise<T> {
  const response = await fetch(publicUrl(path));
  if (!response.ok) {
    throw new Error(`Unable to load ${path}: ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export async function loadManifest(): Promise<PresentationManifest> {
  return fetchJson<PresentationManifest>("presentation-manifest.json");
}

export async function loadSourceIndex(): Promise<SourceIndex> {
  return fetchJson<SourceIndex>("source-index.json");
}

export async function loadSummaries(manifest: PresentationManifest): Promise<Record<string, ModuleSummary>> {
  const entries = await Promise.all(
    manifest.modules
      .filter((module) => module.summaryFile)
      .map(async (module) => {
        try {
          const summary = await fetchJson<ModuleSummary>(module.summaryFile as string);
          return [module.id, summary] as const;
        } catch (error) {
          return [
            module.id,
            {
              schemaVersion: 1,
              moduleId: module.id,
              title: module.title,
              displayCategory: module.displayCategory,
              sourceFileIds: module.sourceFileIds,
              summary: error instanceof Error ? error.message : "Summary could not be loaded.",
              status: "missing"
            }
          ] as const;
        }
      })
  );

  return Object.fromEntries(entries);
}

export async function loadMarkdown(readUrl: string): Promise<string> {
  const response = await fetch(readUrl);
  if (!response.ok) {
    throw new Error(`Unable to load source: ${response.status}`);
  }
  return response.text();
}
