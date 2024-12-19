import { ref } from "vue";

export function useGroups() {
  const groups = ref();
  const isLoading = ref(false);
  const isError = ref(false);
  const { currentStudent, getCurrentStudent } = useCurrentStudent();

  // Ensure user is authenticated before making requests
  const ensureAuthenticated = async () => {
    if (!currentStudent.value) {
      await getCurrentStudent();
    }
    if (!currentStudent.value) {
      throw new Error("User not authenticated");
    }
    return currentStudent.value;
  };

  // Add this function to check authentication status
  const checkAuthStatus = async () => {
    try {
      if (!currentStudent.value) {
        await getCurrentStudent();
      }
      return !!currentStudent.value;
    } catch (error) {
      return false;
    }
  };

  async function getAllGroups() {
    try {
      await ensureAuthenticated();
      isError.value = false;
      isLoading.value = true;
      const response = await useApiFetch("/groups", {
        method: "GET",
      });
      groups.value = response;
    } catch (error) {
      isError.value = true;
      throw error;
    } finally {
      isLoading.value = false;
    }
  }

  async function getGroupById(groupId: string) {
    try {
      await ensureAuthenticated();
      isError.value = false;
      isLoading.value = true;
      const response = await useApiFetch(`/groups/${groupId}`, {
        method: "GET",
      });
      return response;
    } catch (error) {
      isError.value = true;
      throw error;
    } finally {
      isLoading.value = false;
    }
  }

  async function createGroup(groupData: any) {
    try {
      await ensureAuthenticated();
      isError.value = false;
      isLoading.value = true;
      const response = await useApiFetch("/groups", {
        method: "POST",
        body: groupData,
      });
      return response;
    } catch (error) {
      isError.value = true;
    } finally {
      isLoading.value = false;
    }
  }

  async function joinGroup(groupId: string) {
    try {
      await getCurrentStudent();

      if (!currentStudent.value) {
        throw new Error("No student found");
      }

      isError.value = false;
      isLoading.value = true;
      const response = await useApiFetch(`/groups/${groupId}/join`, {
        method: "POST",
        body: {
          student_id: currentStudent.value.id,
        },
      });
      return response;
    } catch (error) {
      isError.value = true;
      throw error;
    } finally {
      isLoading.value = false;
    }
  }

  async function leaveGroup(groupId: string) {
    try {
      isError.value = false;
      isLoading.value = true;
      const response = await useApiFetch(`/groups/${groupId}/leave`, {
        method: "POST",
      });
      return response;
    } catch (error) {
      isError.value = true;
    } finally {
      isLoading.value = false;
    }
  }

  async function getGroupStudents(groupId: string) {
    try {
      await ensureAuthenticated();
      isError.value = false;
      isLoading.value = true;
      const response = await useApiFetch(`/groups/${groupId}/students`, {
        method: "GET",
      });
      return response;
    } catch (error) {
      isError.value = true;
    } finally {
      isLoading.value = false;
    }
  }

  async function getGroupRequests(groupId: string) {
    try {
      await ensureAuthenticated();
      isError.value = false;
      isLoading.value = true;
      const response = await useApiFetch(`/groups/${groupId}/requests`, {
        method: "GET",
      });
      return response;
    } catch (error) {
      isError.value = true;
      throw error;
    } finally {
      isLoading.value = false;
    }
  }

  async function handleGroupRequest(
    groupId: string,
    requestId: string,
    action: "approve" | "reject" | "block",
  ) {
    try {
      await ensureAuthenticated();
      isError.value = false;
      isLoading.value = true;
      const response = await useApiFetch(
        `/groups/${groupId}/requests/${requestId}/${action}`,
        {
          method: "POST",
        },
      );
      return response;
    } catch (error) {
      isError.value = true;
      throw error;
    } finally {
      isLoading.value = false;
    }
  }

  async function handleUserBlock(
    groupId: string,
    studentId: string,
    action: "block" | "unblock",
  ) {
    try {
      isError.value = false;
      isLoading.value = true;
      const response = await useApiFetch(
        `/groups/${groupId}/students/${studentId}/${action}`,
        {
          method: "POST",
        },
      );
      return response;
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
    currentStudent,
    getAllGroups,
    getGroupById,
    createGroup,
    joinGroup,
    leaveGroup,
    getGroupStudents,
    getGroupRequests,
    handleGroupRequest,
    handleUserBlock,
    checkAuthStatus,
  };
}
