import { ref } from "vue";
import { fetchCurrentStudent } from "@/services/studentService";

export function useCurrentStudent() {
  const currentStudent = ref(null);
  const isLoading = ref(false);
  const isError = ref(false);

  async function getCurrentStudent() {
    try {
      isError.value = false;
      isLoading.value = true;
      const response = await fetchCurrentStudent();
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
