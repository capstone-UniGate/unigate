export const useApiFetch = (url: string, options = {}) => {
  const config = useRuntimeConfig();
  const token = localStorage.getItem('unigate-token');

  return $fetch(url, {
    baseURL: config.public.baseURL,
    headers: {
      ...(token ? { Authorization: token } : {}),
    },
    ...options,
  });
};
