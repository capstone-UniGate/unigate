import { ref } from "vue";

export function useGroups() {
  const groups = ref();
  const isLoading = ref(false);
  const isError = ref(false);

  async function getAllGroups() {
    try {
      isError.value = false;
      isLoading.value = true;
      const response = await useApiFetch("/groups", {
        method: "GET",
      });
      groups.value = response;
    } catch (error) {
      isError.value = true;
    } finally {
      isLoading.value = false;
    }
  }

  async function getGroupById(groupId: string) {
    try {
      isError.value = false;
      isLoading.value = true;
      const response = await useApiFetch(`/groups/${groupId}`, {
        method: "GET",
      });
      return response;
    } catch (error) {
      isError.value = true;
    } finally {
      isLoading.value = false;
    }
  }

  async function createGroup(groupData: any) {
    try {
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
      isError.value = false;
      isLoading.value = true;
      const response = await useApiFetch(`/groups/${groupId}/join`, {
        method: "POST",
      });
      return response;
    } catch (error) {
      isError.value = true;
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
      isError.value = false;
      isLoading.value = true;
      const response = await useApiFetch(`/groups/${groupId}/requests`, {
        method: "GET",
      });
      return response;
    } catch (error) {
      isError.value = true;
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
    getAllGroups,
    getGroupById,
    createGroup,
    joinGroup,
    leaveGroup,
    getGroupStudents,
    getGroupRequests,
    handleGroupRequest,
    handleUserBlock,
  };
}