<template>
  <Toaster />
  <!-- Error Message Component -->
  <ErrorMessage v-if="isError" @retry="loadGroup" />

  <!-- Loading Indicator Component -->
  <LoadingIndicator v-if="isLoading" />
  <div v-if="group">
    <!-- Avatar Modal -->
    <div
      v-if="isAvatarModalOpen"
      class="fixed inset-0 flex items-center justify-center bg-gray-900 bg-opacity-50 z-50"
    >
      <div class="bg-white rounded-lg shadow-xl p-6 w-80 text-center relative">
        <!-- Close Button -->
        <button
          @click="closeAvatarModal"
          class="absolute top-3 right-3 text-gray-500 hover:text-gray-700"
        >
          ✖
        </button>
        <!-- Enlarged Avatar -->
        <img
          :src="group.avatar"
          alt="Group Avatar"
          class="w-40 h-40 mx-auto rounded-full mb-4"
        />
        <!-- Group Name -->
        <h2 class="text-lg font-semibold text-gray-800">{{ group.name }}</h2>
      </div>
    </div>

    <div
      class="p-6 md:p-10 flex flex-col lg:flex-row items-center lg:items-start text-center lg:text-left gap-10"
    >
      <!-- Left Side: Group Details or Members -->
      <div class="flex-grow w-full lg:w-2/3">
        <!-- Show members if in the "members" section -->
        <div v-if="isViewingMembers">
          <h1 class="text-2xl font-semibold text-gray-800 mb-6">
            Members of
            <span class="text-primary-600">{{ group.name || "Group" }}</span>
          </h1>
          <ScrollArea
            class="h-[300px] lg:h-[400px] bg-white border border-gray-200 p-4 rounded-lg shadow-sm"
          >
            <ul>
              <li
                v-for="member in group.members"
                :key="member.id"
                class="flex items-center gap-4 mb-4"
              >
                <Avatar class="w-10 h-10">
                  <AvatarImage
                    src="https://via.placeholder.com/50"
                    alt="Member Avatar"
                  />
                  <AvatarFallback>NA</AvatarFallback>
                </Avatar>
                <router-link
                  :to="`/groups/${groupId}`"
                  class="text-gray-700 hover:text-primary-500 font-medium"
                >
                  {{ member.name }}
                </router-link>
              </li>
            </ul>
          </ScrollArea>
        </div>

        <!-- Group Details (if not viewing members) -->
        <div v-else>
          <div
            class="flex items-center gap-4 mb-6 justify-center lg:justify-start"
          >
            <Avatar
              class="cursor-pointer w-20 h-20 rounded-full border border-gray-300 hover:shadow-lg hover:scale-105 transition-all"
              @click="openAvatarModal"
            >
              <AvatarImage
                src="https://github.com/radix-vue.png"
                alt="Group Avatar"
              />
              <AvatarFallback>GN</AvatarFallback>
            </Avatar>
            <div>
              <h1 class="text-3xl font-bold text-gray-800">
                {{ group.name || "Group" }}
              </h1>
              <p class="text-sm text-gray-500 mt-1">Course</p>
            </div>
          </div>

          <div class="mb-6">
            <p class="text-gray-600">
              Number of
              <NuxtLink
                :to="`/groups/${groupId}/students`"
                class="text-blue-500 hover:underline"
                id="members_list"
              >
                members
              </NuxtLink>
              : <span class="font-semibold">{{ group.members_count }}</span>
            </p>
          </div>

          <div
            v-if="is_super_student && group.type == 'Private'"
            class="text-left mb-6"
          >
            <Button
              @click="toggleRequests"
              id="Manage_requests"
              class="bg-blue-500 text-white font-semibold py-2 px-4 rounded-lg shadow-lg hover:bg-blue-600 hover:shadow-xl active:scale-95 transition-all"
            >
              {{ showRequests ? "Hide Requests" : "Manage Requests" }}
            </Button>

            <div v-if="showRequests" class="mt-4">
              <h3 class="text-xl font-semibold mb-4">Join Requests</h3>
              <div v-if="isLoadingRequests">
                <LoadingIndicator />
              </div>
              <div
                v-else-if="requests.length === 0"
                id="no_requests"
                class="text-gray-500"
              >
                No pending requests
              </div>
              <div v-else class="space-y-4">
                <div
                  v-for="request in requests"
                  :key="request.id"
                  id="request"
                  class="bg-white p-4 rounded-lg shadow border"
                >
                  <div class="flex items-center justify-between">
                    <div>
                      <p class="font-medium">{{ request.student?.name }}</p>
                      <p class="text-sm text-gray-500" id="request_status">
                        Status: {{ request.status }}
                      </p>
                    </div>
                    <div class="space-x-2">
                      <Button
                        @click="handleRequest(request.id, 'approve')"
                        class="bg-green-500 hover:bg-green-600 col-span-2"
                        id="approve_button"
                      >
                        Approve
                      </Button>
                      <Button
                        @click="handleRequest(request.id, 'reject')"
                        class="bg-red-500 hover:bg-red-600"
                        id="reject_button"
                      >
                        Reject
                      </Button>
                      <Button
                        @click="handleRequest(request.id, 'block')"
                        class="bg-red-500 hover:bg-red-600"
                        id="block_button"
                      >
                        Block
                      </Button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="text-left mb-6">
            <p class="text-sm text-gray-500">Description</p>
            <p
              class="text-gray-700 text-base bg-gray-50 border border-gray-200 rounded-lg p-4"
            >
              {{ group.description || "No description available." }}
            </p>
          </div>

          <div class="text-left mb-6">
            <p class="text-sm text-gray-500">Tags</p>
            <p
              class="text-gray-700 text-base bg-gray-50 border border-gray-200 rounded-lg p-4"
            >
            <span class="mx-1" v-for="(tag, index) in group.tags" :key="index">{{ tag }}<span v-if="index < group.tags.length - 1">,</span></span>
            </p>
          </div>

          <div>
            <div v-if="isLoadingStatus">
              <LoadingIndicator />
            </div>
            <div v-else id="request_status_student">
              <p
                v-if="
                  userRequestStatus && userRequestStatus.includes('PENDING')
                "
              >
                Your request status: <strong>{{ userRequestStatus }}</strong>
              </p>
            </div>
          </div>

          <div class="text-center mt-6">
            <Button
              v-if="is_member_of"
              @click="leaveGroups"
              class="bg-red-500 text-white font-semibold py-2 px-4 rounded-lg shadow-lg hover:bg-red-600 hover:shadow-xl active:scale-95 transition-all"
              id="leave-group-button"
            >
              Leave Group
            </Button>
            <Button
              v-else-if="!is_member_of && group.type === 'Public'"
              @click="joinGroups"
              class="bg-indigo-500 text-white font-semibold py-2 px-4 rounded-lg shadow-lg hover:bg-indigo-600 hover:shadow-xl active:scale-95 transition-all"
              id="join-group-button"
            >
              Join Group
            </Button>

            <Button
              v-else-if="
                userRequestStatus == null ||
                (userRequestStatus.includes('REJECTED') &&
                  !is_member_of &&
                  group.type === 'Private' &&
                  !isBlocked)
              "
              @click="askToJoinGroup"
              class="bg-yellow-500 text-white font-semibold py-2 px-4 rounded-lg shadow-lg hover:bg-yellow-600 hover:shadow-xl active:scale-95 transition-all"
              id="ask-to-join-button"
              :disabled="isBlocked"
            >
              Ask to Join
            </Button>

            <Button
              v-else-if="userRequestStatus === 'PENDING'"
              @click="undoJoinRequest"
              class="bg-orange-500 text-white font-semibold py-2 px-4 rounded-lg shadow-lg hover:bg-orange-600 hover:shadow-xl active:scale-95 transition-all"
              id="undo-request-button"
            >
              Undo Request
            </Button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Toaster } from "@/components/ui/toast";
import { useToast } from "@/components/ui/toast/use-toast";
import { computed, ref, onMounted } from "vue";
import { Button } from "@/components/ui/button";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { ScrollArea } from "@/components/ui/scroll-area";
import { useRoute, useRouter } from "vue-router";
import { useGroups } from "@/composables/useGroups";
import { useCurrentStudent } from "@/composables/useCurrentStudent";

const route = useRoute();
const router = useRouter();
const { toast } = useToast();
const {
  getGroupById,
  leaveGroup,
  joinGroup,
  getGroupRequests,
  handleGroupRequest,
} = useGroups();
const { currentStudent, getCurrentStudent } = useCurrentStudent();

const groupId = route.params.id;
const isLoading = ref(false);
const isError = ref(false);
const group = ref<any>(null);
const isBlocked = ref(false);
const is_member_of = computed(() => {
  const isStudent = group.value.students?.some(
    (student) => student.number === currentStudent.value?.number,
  );

  const isSuperStudent = group.value.super_students?.some(
    (superStudent) => superStudent.number === currentStudent.value?.number,
  );

  return isStudent || isSuperStudent;
});

const isViewingMembers = ref(false);
const isAvatarModalOpen = ref(false);
const is_super_student = computed(() => {
  return group.value?.super_students?.some(
    (superStudent) => superStudent.number === currentStudent.value?.number,
  );
});

const userRequestStatus = ref(null);
const isLoadingStatus = ref(true);
const isErrorStatus = ref(false);

const showRequests = ref(false);
const requests = ref([]);
const isLoadingRequests = ref(false);

// Function to check if the current student is blocked
const checkBlockStatus = () => {
  const blockedStudents = group.value?.blocked_students || [];
  isBlocked.value = blockedStudents.some(
    (student: { number: any }) =>
      student.number === currentStudent.value?.number,
  );
  return isBlocked.value;
};

async function loadGroup() {
  try {
    isError.value = false;
    isLoading.value = true;

    // First get current student
    await getCurrentStudent();

    // Load group data
    const groupData = await getGroupById(groupId.toString());
    group.value = groupData;

    // Check if user is blocked for this specific group
    const blockStatus = await checkBlockStatus();
    if (blockStatus) {
      router.push("/groups/blocked");
      return;
    }
  } catch (error) {
    isError.value = true;
    toast({
      title: "Error",
      description: "Failed to load group information",
      variant: "destructive",
    });
  } finally {
    isLoading.value = false;
  }
}

onMounted(async () => {
  await loadGroup();
  await getCurrentStudent();
  await fetchUserRequestStatus();
  if (is_super_student.value) {
    await loadRequests();
  }
});

const openAvatarModal = () => {
  isAvatarModalOpen.value = true;
};

const closeAvatarModal = () => {
  isAvatarModalOpen.value = false;
};

const navigateToRequests = () => {
  router.push(`/groups/${groupId}/requests`);
};
const toggleRequests = async () => {
  showRequests.value = !showRequests.value;
  if (showRequests.value) {
    await loadRequests();
  }
};

const loadRequests = async () => {
  try {
    isLoadingRequests.value = true;
    const response = await getGroupRequests(groupId.toString());
    requests.value = response.filter((request) => request.status === "PENDING");
  } catch (error) {
    toast({
      title: "Error",
      description: "Failed to load requests",
      variant: "destructive",
    });
  } finally {
    isLoadingRequests.value = false;
  }
};

const handleRequest = async (
  requestId: string,
  action: "approve" | "reject" | "block",
) => {
  try {
    // Wait for the backend request to complete
    const response = (await handleGroupRequest(
      groupId.toString(),
      requestId,
      action,
    )) as boolean;

    // Only update the frontend if the backend request was successful
    if (response) {
      requests.value = requests.value.filter(
        (request) => request.id !== requestId,
      );

      toast({
        title: "Success",
      });
      // Reload group data to get fresh information
      await loadGroup();
    }
  } catch (error) {
    toast({
      title: "Error",
      description: `Failed to ${action} request`,
      variant: "destructive",
    });
  }
};

const askToJoinGroup = async () => {
  try {
    const groupData = await joinGroup(groupId.toString());

    // Manually set the userRequestStatus to "PENDING"
    userRequestStatus.value = "PENDING";

    toast({
      title: "Request Submitted",
      description: "Your join request has been successfully submitted.",
    });
  } catch (error) {
    console.error("Error submitting join request:", error);
    toast({
      title: "Error",
      description: "An error occurred while submitting the join request.",
      variant: "destructive",
    });
  }
};

const undoJoinRequest = async () => {
  try {
    // Call the backend to delete the join request
    await useApiFetch(`/groups/${groupId}/requests/undo`, {
      method: "DELETE",
    });

    // Update the userRequestStatus to null (frontend update)
    userRequestStatus.value = null;

    toast({
      title: "Request Cancelled",
      description: "Your join request has been successfully cancelled.",
      variant: "success",
    });
  } catch (error) {
    console.error("Error cancelling join request:", error);
    toast({
      title: "Error",
      description: "Failed to cancel the join request.",
      variant: "destructive",
    });
  }
};

const joinGroups = async () => {
  try {
    const response = await joinGroup(groupId.toString());
    is_member_of.value = true; // Update membership status
    await loadGroup(); // Reload group data to get fresh information
  } catch (error) {
    toast({
      variant: "destructive",
      description: error,
    });
  }
};

async function fetchUserRequestStatus() {
  try {
    isLoadingStatus.value = true;
    isErrorStatus.value = false;

    // Ensure current student is loaded
    if (!currentStudent.value) {
      await getCurrentStudent();
    }

    // Fetch the requests
    const requests = await getGroupRequests(groupId.toString());

    // Find the logged-in user's request
    const userRequest = requests.find(
      (request) => request.student_id === studentId,
    );
    // Update the status if found
    userRequestStatus.value = userRequest ? userRequest.status : null;
  } catch (error) {
    isErrorStatus.value = true;
  } finally {
    isLoadingStatus.value = false;
  }
}

const leaveGroups = async () => {
  try {
    isError.value = false;
    isLoading.value = true;
    const string_message = await leaveGroup(groupId.toString());

    if (string_message === "The student has been removed successfully") {
      is_member_of.value = false; // Update membership status
      setTimeout(() => {
        router.push("/groups");
      }, 1500);
    }
    await loadGroup(); // Reload group data to get fresh information
  } catch (error) {
    toast({
      variant: "destructive",
      description: "Failed to join group",
    });
    isError.value = true;
  } finally {
    isLoading.value = false;
  }
};
</script>
