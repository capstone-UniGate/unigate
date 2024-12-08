<template>

  <div  v-if="requests.length > 0 ">
    <!-- Title Section -->
    <div class="text-center mt-10 mb-6">
      <h1 class="text-3xl font-bold text-gray-900">Join Requests</h1>
    </div>

    <div class="mx-auto max-w-5xl pb-20">
      <ul role="list" class="space-y-6" >
        <li
          v-for="request in requests"
          :key="request.id"
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
                {{ request.student.name }}  {{ request.student.surname }}
              </p>
            </div>
          </div>

          <!-- Buttons Section -->
          <div class="flex gap-x-4">
            <div v-if="request.status == 'PENDING'">
            <button
              @click="reject(request.id)"
              class="px-4 py-2 text-sm font-medium text-white bg-red-500 rounded-lg hover:bg-red-600 transition mr-5">
              Reject
            </button>
            <button
              @click="approve(request.id)"
              class="px-4 py-2 text-sm font-medium text-white bg-green-500 rounded-lg hover:bg-green-600 transition">
              Approve
            </button>

            <button
              @click="block(request.id)"
              class="px-4 py-2 text-sm font-medium text-white bg-gray-500 rounded-lg hover:bg-gray-600 transition"
            >
              Block
            </button>

            <!--</div>-->

            <!--
            <div v-else>
              <span
                v-if="request.status == 'APPROVED'"
                class="inline-flex items-center rounded-md bg-red-50 px-2 py-1 text-xs font-medium text-red-700 ring-1 ring-inset ring-red-600/20"
              >
                Approved
              </span>
              <span
                v-if="request.status == 'REJECTED'"
                class="inline-flex items-center rounded-md bg-green-50 px-2 py-1 text-xs font-medium text-green-700 ring-1 ring-inset ring-green-600/20"
              >
                Rejected
              </span>
            </div>
          </div>
        </li>
      </ul>
    </div>
  </div>
  <NoJoinRequest v-else/>
</template>

<script setup lang="ts">
const route = useRoute();
const groupId = route.params.id;
const placeholderImage = "https://via.placeholder.com/150?text=Profile";
const requests = ref([]); // Initialize as empty array

// Fetch requests
async function fetchRequests() {
  try {
    requests.value = await useApiFetch(`groups/${groupId}/requests`);
  } catch (error) {
    console.error("Error fetching requests:", error);
  }
}
fetchRequests();

function approve(id) {
  useApiFetch(`requests/${id}/approve`, {
    method: "post",
  }).then(() => {
    if (requests.value) {
      requests.value = requests.value.filter((request) => request.id !== id);
    }
  });
}



function reject(id) {
  useApiFetch(`requests/${id}/reject`, {
    method: "post",
  }).then(() => {
    if (requests.value) {
      requests.value = requests.value.filter((request) => request.id !== id);
    }
  });
}




function block(requestId: number) {
  // Find the request with the given ID
  const requestIndex = requests.findIndex((req) => req.id === requestId);

  if (requestIndex !== -1) {
    // Remove the request from the list
    const blockedUser = requests[requestIndex];
    requests.splice(requestIndex, 1);

    // Optionally, add a way to mark the user as "blocked" for private groups
    // For example: Store their blocked status in a database or local state
    if (!group.blockedUsers) {
      group.blockedUsers = [];
    }
    group.blockedUsers.push(blockedUser.id);
  }
}
</script>
