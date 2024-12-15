import { useCookie } from "#app";

export const useApiFetch = (
  url: string,
  options: { headers?: Record<string, string> } = {},
) => {
  const config = useRuntimeConfig();
  const tokenCookie = useCookie("access_token");

  // Ensure headers object exists
  if (!options.headers) {
    options.headers = {};
  }

  // Only add Authorization header if token exists
  if (tokenCookie.value) {
    options.headers.Authorization = `Bearer ${tokenCookie.value}`;
  }

  return $fetch(url, {
    baseURL: config.public.baseURL,
    ...options,
    headers: options.headers,
  });
};
