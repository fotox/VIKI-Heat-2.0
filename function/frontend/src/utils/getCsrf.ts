export function getCsrfToken(): string {
  return document.cookie
    .split("; ")
    .find(row => row.startsWith("csrf_access_token="))
    ?.split("=")[1] || "";
}
