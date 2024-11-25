<template>
  <div>
    <!-- Title Section -->
    <div class="text-center mt-10 mb-6">
      <h1 class="text-3xl font-bold text-gray-900">Join Requests</h1>
    </div>

    <div v-if="requests" class="mx-auto max-w-5xl pb-20">
      <ul role="list" class="space-y-6">
        <li
          v-for="request in requests"
          :key="request.id"
          class="flex items-center justify-between gap-x-12 bg-white rounded-lg shadow-md p-6 hover:shadow-lg hover:scale-105 transition-transform duration-300"
        >
          <!-- Profile Section -->
          <div class="flex items-center gap-x-6">
            <img
              class="w-16 h-16 rounded-full"
              :src="request.imageUrl"
              alt="Profile"
            />
            <div>
              <p class="text-lg font-semibold text-gray-900">
                {{ request.name }}
              </p>
              <p class="text-sm text-gray-500">Requesting access</p>
            </div>
          </div>

          <!-- Buttons Section -->
          <div class="flex gap-x-4">
            <!--<div v-if="request.status == 'PENDING'">-->
            <button
              @click="reject(request.id)"
              class="px-4 py-2 text-sm font-medium text-white bg-red-500 rounded-lg hover:bg-red-600 transition"
            >
              Reject
            </button>
            <button
              @click="approve(request.id)"
              class="px-4 py-2 text-sm font-medium text-white bg-green-500 rounded-lg hover:bg-green-600 transition"
            >
              Approve
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
            -->
          </div>
        </li>
      </ul>
    </div>
    <NoJoinRequest v-else />
  </div>
</template>

<script setup lang="ts">
// const route = useRoute();
// const groupId = route.params.id;
// const placeholderImage = "https://via.placeholder.com/150?text=Profile";
// const requests = await useApiFetch(`groups/${groupId}/requests`);

// function approve(id) {
//   useApiFetch(`requests/${id}/approve`, {
//     method: "post",
//   });
// }

// function reject(id) {
//   useApiFetch(`requests/${id}/reject`, {
//     method: "post",
//   });
// }

const route = useRoute();
const router = useRouter();
const groupId = route.params.id;
const currentUserId = 3;

// Mock data to represent the groups and their members
const groupsData = [
  {
    id: "1",
    name: "Group 1",
    description:
      "This is a sample description for Group 1. This is a sample description for Group 1.",
    isPrivate: true,
    creatorId: 3,
    rejectedUsers: [4], // Example rejected user ID
    blockedUsers: [5], // Example blocked user ID
    members: [],
  },
  {
    id: "2",
    name: "Group 2",
    description: "This is a sample description for Group 2.",
    isPrivate: false,
    creatorId: 4,
    rejectedUsers: [], // Add this field
    blockedUsers: [], // Example blocked user ID
  },
];
const group = groupsData.find((g) => g.id === groupId) || {
  name: "Group...",
  description: "",
  isPrivate: false,
  creatorId: null,
  rejectedUsers: [],
  blockedUsers: [],
  members: [],
};

// Check the rejection status when loading the group page. If the user is rejected, redirect them away
const isRejected = computed(() => {
  return group.rejectedUsers.includes(currentUserId);
});

const isBlocked = computed(() => {
  return group.blockedUsers.includes(currentUserId);
});

const requests = [
  {
    id: 1,
    name: "Leslie Alexander",
    imageUrl:
      "https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80",
  },
  {
    id: 2,
    name: "Michael Foster",
    role: "Co-Founder / CTO",
    imageUrl:
      "https://images.unsplash.com/photo-1519244703995-f4e0f30006d5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80",
  },
  {
    id: 3,
    name: "Dries Vincent",
    role: "Business Relations",
    imageUrl:
      "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80",
  },
  {
    id: 4,
    name: "Lindsay Walton",
    imageUrl:
      "https://images.unsplash.com/photo-1517841905240-472988babdf9?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80",
  },
  {
    id: 5,
    name: "Courtney Henry",
    imageUrl:
      "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80",
  },
];

if (group.isPrivate && isRejected.value) {
  router.push("/access-denied"); // Redirect to an "Access Denied" page
}

function approve(requestId: number) {
  // Find the request being approved
  const requestIndex = requests.findIndex((req) => req.id === requestId);
  if (requestIndex !== -1) {
    // Add the approved member to the group's members
    const approvedMember = requests[requestIndex];
    group.members.push(approvedMember);

    // Remove the request from the requests array
    requests.splice(requestIndex, 1);

    // Redirect the student to the group page after approval
    //TODO: Implement redirect logic

    router.push(`/groups/${groupId}`);
  }
}

function reject(requestId: number) {
  // Find the rejected request
  const requestIndex = requests.findIndex((req) => req.id === requestId);
  if (requestIndex !== -1) {
    // Remove the request from the list
    const rejectedMember = requests[requestIndex];
    requests.splice(requestIndex, 1);

    // Optionally, add a way to mark the user as "rejected" for private groups
    // For example: Store their rejection status in a database or local state
    if (!group.rejectedUsers) {
      group.rejectedUsers = [];
    }
    group.rejectedUsers.push(rejectedMember.id);

    // Notify the superstudent of the rejection
    //TODO: Implement notification logic
  }
}
</script>
