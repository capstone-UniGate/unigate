import { useApiFetch } from "@/composables/useApiFetch";

export async function fetchCurrentStudent() {
  return await useApiFetch("/students/me", {
    method: "GET",
  });
}
