<template>
  <div>
    <LoadingIndicator v-if="isLoading" />
    <ErrorMessage v-else-if="isError" @retry="fetchRequests" />

    <div v-else-if="requests.length > 0">
      <!-- Title Section -->
      <div class="text-center mt-10 mb-6">
        <h1 class="text-3xl font-bold text-gray-900">Join Requests</h1>
      </div>

      <div class="mx-auto max-w-5xl pb-20">
        <ul role="list" class="space-y-6">
          <li
            v-for="request in requests"
            :key="request.id"
            id="request"
            class="flex items-center justify-between gap-x-12 bg-white rounded-lg shadow-md p-6 hover:shadow-lg hover:scale-105 transition-transform duration-300"
          >
            <!-- Profile Section -->
            <div class="flex items-center gap-x-6">
              <img
                class="w-16 h-16 rounded-full"
                :src="placeholderImage"
                alt="Profile"
              />
              <div>
                <p class="text-lg font-semibold text-gray-900">
                  {{ request.student.name }} {{ request.student.surname }}
                </p>
              </div>
            </div>

            <!-- Buttons Section -->
            <div class="flex gap-x-4">
              <div v-if="request.status === 'PENDING'">
                <button
                  @click="handleRequest(request.id, 'reject')"
                  class="px-4 py-2 text-sm font-medium text-white bg-red-500 rounded-lg hover:bg-red-600 transition mr-5"
                  id="reject_btn"
                >
                  Reject
                </button>
                <button
                  @click="handleRequest(request.id, 'approve')"
                  class="px-4 py-2 text-sm font-medium text-white bg-green-500 rounded-lg hover:bg-green-600 transition"
                  id="approve_btn"
                >
                  Approve
                </button>
                <button
                  @click="handleRequest(request.id, 'block')"
                  class="px-4 py-2 text-sm font-medium text-white bg-gray-500 rounded-lg hover:bg-gray-600 transition ml-5"
                  id="block_btn"
                >
                  Block
                </button>
              </div>
            </div>
          </li>
        </ul>
      </div>
    </div>
    <NoJoinRequest v-else />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";

interface Request {
  id: string;
  status: string;
  student: {
    name: string;
    surname: string;
  };
}

const route = useRoute();
const router = useRouter();
const groupId = route.params.id as string;
const placeholderImage = "https://via.placeholder.com/150?text=Profile";
const requests = ref<Request[]>([]);
const isLoading = ref(true);
const isError = ref(false);

const { getGroupRequests, handleGroupRequest, currentStudent } = useGroups();

// Fetch requests
async function fetchRequests() {
  try {
    isLoading.value = true;
    isError.value = false;
    const response = await getGroupRequests(groupId);
    requests.value = response as Request[];
  } catch (error) {
    console.error("Error fetching requests:", error);
    isError.value = true;
    // Redirect to login if unauthorized
    if (error.response?.status === 401 || error.response?.status === 403) {
      router.push("/login");
    }
  } finally {
    isLoading.value = false;
  }
}

// Handle request actions (approve/reject/block)
async function handleRequest(
  requestId: string,
  action: "approve" | "reject" | "block",
) {
  try {
    await handleGroupRequest(groupId, requestId, action);
    // Remove the request from the list after successful action
    requests.value = requests.value.filter(
      (request) => request.id !== requestId,
    );
  } catch (error) {
    console.error(`Error ${action}ing request:`, error);
    if (error.response?.status === 401 || error.response?.status === 403) {
      router.push("/login");
    }
  }
}

// Initial fetch with authentication check
onMounted(async () => {
  if (!currentStudent.value) {
    router.push("/login");
    return;
  }
  await fetchRequests();
});
</script>
