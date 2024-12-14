import { useCookie } from "#app";

export const useApiFetch = (
  url: string,
  options: { headers?: Record<string, string> } = {},
) => {
  const config = useRuntimeConfig();
  const tokenCookie = useCookie("access_token");

  // Merge headers with Authorization token
  const headers = {
    ...options.headers,
    Authorization: `Bearer ${tokenCookie.value}`,
  };

  return $fetch(url, {
    baseURL: config.public.baseURL,
    ...options,
    headers,
  });
};
