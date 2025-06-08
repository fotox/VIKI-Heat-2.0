export function maskText(text: string | null | undefined): string | null {
  if (text == null) return null;
  return '*'.repeat(10);
}
