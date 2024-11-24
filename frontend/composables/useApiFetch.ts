export const useApiFetch = (url: string, options = {}) => {
  const config = useRuntimeConfig();

  return $fetch(url, {
    baseURL: config.public.baseURL,
    ...options,
  });
};
