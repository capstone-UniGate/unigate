<template>
  <Toaster />

  <div class="p-6 md:p-10 flex flex-col lg:flex-row">
    <!-- Left Side: Group Details or Members -->
    <div class="flex-grow mb-6 lg:mb-0">
      <!-- Show members if is in the sezction "members" -->
      <div v-if="isViewingMembers">
        <h1 class="text-3xl font-bold text-gray-800 mb-6">
          Members of {{ group.name || "Group..." }}
        </h1>
        <ScrollArea
          class="h-[300px] lg:h-[400px] bg-gray-100 p-4 rounded-lg shadow-md"
        >
          <ul>
            <li
              v-for="member in group.members"
              :key="member.id"
              class="mb-4 text-lg text-gray-700 flex items-center"
            >
              <Avatar class="inline-block mr-2">
                <AvatarImage
                  src="https://via.placeholder.com/50"
                  alt="Member Avatar"
                />
                <AvatarFallback>NA</AvatarFallback>
              </Avatar>
              <router-link
                :to="`/groups/${groupId}`"
                class="text-blue-500 hover:underline"
              >
                {{ member.name }}
              </router-link>
            </li>
          </ul>
        </ScrollArea>
        <NuxtLink
          :to="`/groups/${groupId}`"
          class="text-blue-500 hover:underline mt-4 inline-block"
        >
          Back to Group Details
        </NuxtLink>
      </div>

      <!-- Dettagli del gruppo (se non si sta visualizzando i membri) -->
      <div v-else>
        <div class="flex items-center gap-4 mb-6">
          <Avatar class="cursor-pointer" @click="showModal = true">
            <AvatarImage
              src="https://github.com/radix-vue.png"
              alt="@radix-vue"
            />
            <AvatarFallback>GN</AvatarFallback>
          </Avatar>
          <h1 class="text-3xl font-bold text-gray-800">
            {{ group.name || "Group..." }}
          </h1>
        </div>

        <div class="text-gray-600 mb-6">
          <p>{{ group.description || "Group description..." }}</p>
        </div>

        <div class="mb-6">
          <p class="text-lg text-gray-700">
            Number of
            <NuxtLink
              :to="`/groups/${groupId}/members`"
              class="text-blue-500 hover:underline"
            >
              members
            </NuxtLink>
            : {{ group.members.length }}
          </p>
        </div>

        <div v-if="!isMember && !isSuperstudent" class="text-center mt-6">
          <Button
            @click="joinGroup"
            class="bg-blue-500 text-white px-4 py-2 rounded-md"
          >
            Join Group
          </Button>
        </div>
      </div>
    </div>

    <!-- Right Side: Superstudent Join Requests Section -->
    <NuxtLink
      :to="`/groups/${groupId}/requests`"
      v-if="!isViewingMembers && isSuperstudent && group.isPrivate"
      class="w-full lg:w-80 lg:ml-6"
    >
      Manage Requests
    </NuxtLink>
  </div>
</template>

<script setup lang="ts">
import { Toaster } from "@/components/ui/toast";
import { useToast } from "@/components/ui/toast/use-toast";
import { ref, computed } from "vue";
import { Button } from "@/components/ui/button";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { ScrollArea } from "@/components/ui/scroll-area";
import {
  Tooltip,
  TooltipProvider,
  TooltipTrigger,
  TooltipContent,
} from "@/components/ui/tooltip";
import { useRoute } from "vue-router";

const route = useRoute();
const router = useRouter();
const toast = useToast();

const groupId = route.params.id;
const currentUserId = 3;
const showModal = ref(false);

// Mock data to represent the groups and their members
const groupsData = [
  {
    id: "1",
    name: "Group 1",
    description:
      "This is a sample description for Group 1. This is a sample description for Group 1.",
    isPrivate: true,
    creatorId: 3,
    members: [
      { id: 1, name: "Alice" },
      { id: 2, name: "Bob" },
    ],
    rejectedUsers: [4], // Example rejected user ID
    blockedUsers: [5], // Example blocked user ID
  },
  {
    id: "2",
    name: "Group 2",
    description: "This is a sample description for Group 2.",
    isPrivate: false,
    creatorId: 4,
    members: [
      { id: 3, name: "David" },
      { id: 4, name: "Alice" },
    ],
    rejectedUsers: [], // Add this field
    blockedUsers: [], // Example blocked user ID
  },
];
const group = groupsData.find((g) => g.id === groupId) || {
  name: "Group...",
  description: "",
  isPrivate: false,
  creatorId: null,
  members: [],
  rejectedUsers: [],
  blockedUsers: [],
};

const isViewingMembers = computed(() => {
  return route.path.endsWith("/members");
});

// Computed Properties for Access Control
const isSuperstudent = computed(() => group.creatorId === currentUserId);

const isMember = computed(() => {
  return group.members.some((member) => member.id === currentUserId);
});

// Check the rejection status when loading the group page. If the user is rejected, redirect them away
const isRejected = computed(() => {
  return group.rejectedUsers.includes(currentUserId);
});

const isBlocked = computed(() => {
  return group.blockedUsers.includes(currentUserId);
});
const joinRequests = ref([
  { id: 5, name: "New Member 1" },
  { id: 6, name: "New Member 2" },
]);

if (group.isPrivate && isRejected.value) {
  router.push("/access-denied"); // Redirect to an "Access Denied" page
}

// Access Logic
if (group.isPrivate && isBlocked.value) {
  // Redirect to the "Blocked" page
  router.push("/blocked"); // Redirect to the "Blocked" page
} else if (group.isPrivate && isRejected.value) {
  // Redirect to the main page of the group with normal view
  // router.push("/access-denied"); // Redirect to an "Access Denied" page
} else if (group.isPrivate && !isMember.value) {
  // Redirect to the "Join Group" page
}

function approveRequest(requestId: number) {
  // Find the request being approved
  const requestIndex = joinRequests.value.findIndex(
    (req) => req.id === requestId,
  );
  if (requestIndex !== -1) {
    // Add the approved member to the group's members
    const approvedMember = joinRequests.value[requestIndex];
    group.members.push(approvedMember);

    // Remove the request from the joinRequests array
    joinRequests.value.splice(requestIndex, 1);

    // Redirect the student to the group page after approval
    //TODO: Implement redirect logic

    router.push(`/groups/${groupId}`);
  }
}

function rejectRequest(requestId: number) {
  // Find the rejected request
  const requestIndex = joinRequests.value.findIndex(
    (req) => req.id === requestId,
  );
  if (requestIndex !== -1) {
    // Remove the request from the list
    const rejectedMember = joinRequests.value[requestIndex];
    joinRequests.value.splice(requestIndex, 1);

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

function blockRequest(requestId: number) {
  const requestIndex = joinRequests.value.findIndex(
    (req) => req.id === requestId,
  );
  if (requestIndex !== -1) {
    const blockedMember = joinRequests.value[requestIndex];

    // Add the blocked user to blockedUsers
    group.blockedUsers.push(blockedMember.id);

    // Remove the request from joinRequests
    joinRequests.value.splice(requestIndex, 1);

    // Notify the stufdent of the block
    //TODO: Implement notification logic
  }
}

const joinGroup = () => {
  alert("Join group clicked");
};
</script>

<style scoped>
.p-6 {
  padding: 1.5rem;
}

.md:p-10 {
  padding: 2.5rem;
}

.bg-white {
  background-color: #ffffff;
}
.shadow-md {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
.cursor-pointer {
  cursor: pointer;
}
.shadow-md {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
</style>
