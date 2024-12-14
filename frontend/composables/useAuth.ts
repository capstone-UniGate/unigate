import { useCookie } from "#app";
import { computed } from "vue";
import { useApiFetch } from "./useApiFetch";

interface LoginPayload {
  username: string;
  password: string;
}

interface LoginResponse {
  access_token: string;
}

export function useAuth() {
  const tokenCookie = useCookie<string>("access_token", {
    secure: true,
    sameSite: "strict",
    path: "/",
  });

  const isLoggedIn = computed(() => !!tokenCookie.value);

  async function login(payload: LoginPayload) {
    // Convert the payload into FormData
    const formData = new FormData();
    formData.append("username", payload.username);
    formData.append("password", payload.password);

    const response = await useApiFetch("/auth/login", {
      method: "post",
      body: formData, // now sending multipart/form-data
    });

    if (!response) throw new Error("Login failed");
    tokenCookie.value = (response as LoginResponse).access_token;
  }

  function logout() {
    tokenCookie.value = "";
  }

  return {
    isLoggedIn,
    login,
    logout,
  };
}
