import { ref } from "vue";

export function useCurrentStudent() {
  const currentStudent = ref();
  const isLoading = ref(false);
  const isError = ref(false);

  async function getCurrentStudent() {
    try {
      isError.value = false;
      isLoading.value = true;
      const response = await useApiFetch("/students/me", {
        method: "GET",
      });
      currentStudent.value = response;
    } catch (error) {
      isError.value = true;
    } finally {
      isLoading.value = false;
    }
  }

  return {
    currentStudent,
    isLoading,
    isError,
    getCurrentStudent,
  };
}
