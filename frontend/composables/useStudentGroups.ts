import { ref } from "vue";

export function useStudentGroups() {
  const groups = ref();
  const isLoading = ref(false);
  const isError = ref(false);

  async function getMyGroups() {
    try {
      isError.value = false;
      isLoading.value = true;
      const response = await useApiFetch("/students/groups", {
        method: "GET",
      });
      const data = response as { groups: any[] };
      groups.value = data.groups;
    } catch (error) {
      isError.value = true;
    } finally {
      isLoading.value = false;
    }
  }

  return {
    groups,
    isLoading,
    isError,
    getMyGroups,
  };
}
