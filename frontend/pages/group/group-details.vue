<template>
  <div class="p-6 md:p-10 flex flex-col lg:flex-row">
    <!-- Left Side: Group Details -->
    <div class="flex-grow mb-6 lg:mb-0">
      <div class="flex items-center gap-4 mb-6">
        <Avatar class="cursor-pointer" @click="showModal = true">
          <AvatarImage src="https://github.com/radix-vue.png" alt="@radix-vue" />
          <AvatarFallback>GN</AvatarFallback>
        </Avatar>
        <h1 class="text-3xl font-bold text-gray-800">{{ group.name || 'Group...' }}</h1>
      </div>

      <!-- Modal for Enlarged Avatar -->
      <div v-if="showModal" class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
        <div class="bg-white p-6 rounded-lg shadow-lg">
          <img src="https://github.com/radix-vue.png" alt="Enlarged Avatar" class="w-64 h-64 object-cover rounded-full" />
          <button @click="showModal = false" class="mt-4 bg-red-500 text-white px-4 py-2 rounded-md">Close</button>
        </div>
      </div>

      <!-- Other Group Details -->
      <div class="text-gray-600 mb-6">
        <p>{{ group.description || 'Group description...' }}</p>
      </div>

      <!-- Display Number of Members with "Members" as a Link -->
      <div class="mb-6">
        <p class="text-lg text-gray-700">
          Number of <NuxtLink :to="`/group/${groupId}/members`" class="text-blue-500 hover:underline">members</NuxtLink>: {{ group.members.length }}
        </p>
      </div>

      <!-- Show Join Button Only if User is Not a Member or Superstudent -->
      <div v-if="!isMember && !isSuperstudent" class="text-center mt-6">
        <Button @click="joinGroup" class="bg-blue-500 text-white px-4 py-2 rounded-md">Join Group</Button>
      </div>
    </div>

    <!-- Right Side: Superstudent Join Requests Section as a Scroll Area -->
    <div v-if="isSuperstudent && group.isPrivate" class="w-full lg:w-80 lg:ml-6">
      <ScrollArea class="h-[300px] lg:h-[400px] bg-gray-100 p-4 rounded-lg shadow-md">
        <h2 class="text-xl font-semibold text-gray-700 mb-4">Manage Join Requests</h2>
        <TooltipProvider>
          <ul>
            <li v-for="request in joinRequests" :key="request.id" class="flex items-center justify-between mb-2">
              <span>{{ request.name }}</span>
              <div class="flex space-x-2">
                <!-- Approve Button with Tooltip -->
                <Tooltip>
                  <TooltipTrigger asChild>
                    <Button class="bg-green-500 text-white w-8 h-8 rounded-full hover:bg-green-600">
                      <Avatar src="/icons/check.svg" alt="Approve" />
                    </Button>
                  </TooltipTrigger>
                  <TooltipContent>Accept</TooltipContent>
                </Tooltip>

                <!-- Reject Button with Tooltip -->
                <Tooltip>
                  <TooltipTrigger asChild>
                    <Button class="bg-red-500 text-white w-8 h-8 rounded-full hover:bg-red-600">
                      <Avatar src="/icons/x.svg" alt="Reject" />
                    </Button>
                  </TooltipTrigger>
                  <TooltipContent>Reject</TooltipContent>
                </Tooltip>

                <!-- Block Button with Tooltip -->
                <Tooltip>
                  <TooltipTrigger asChild>
                    <Button class="bg-gray-500 text-white w-8 h-8 rounded-full hover:bg-gray-600">
                      <Avatar src="/icons/ban.svg" alt="Block" />
                    </Button>
                  </TooltipTrigger>
                  <TooltipContent>Block</TooltipContent>
                </Tooltip>
              </div>
            </li>
          </ul>
        </TooltipProvider>
      </ScrollArea>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { Button } from '@/components/ui/button';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Tooltip, TooltipProvider, TooltipTrigger, TooltipContent } from '@/components/ui/tooltip';
import { useRoute } from 'vue-router';

const route = useRoute();
const groupId = route.params.id;
const currentUserId = 3;
const showModal = ref(false);

const groupsData = [
  {
    id: '1',
    name: 'Group 1',
    description: 'This is a sample description for Group 1. This is a sample description for Group 1.',
    isPrivate: true,
    creatorId: 3,
    members: [{ id: 1, name: 'Alice' }, { id: 2, name: 'Bob' }]
  },
  {
    id: '2',
    name: 'Group 2',
    description: 'This is a sample description for Group 2.',
    isPrivate: false,
    creatorId: 4,
    members: [{ id: 3, name: 'David' }, { id: 4, name: 'Alice' }]
  },
];
const group = groupsData.find(g => g.id === groupId) || { name: 'Group...', description: '', isPrivate: false, creatorId: null, members: [] };

const isMember = computed(() => group.members.some(member => member.id === currentUserId));
const isSuperstudent = computed(() => group.creatorId === currentUserId);

const joinRequests = ref([
  { id: 5, name: 'New Member 1' },
  { id: 6, name: 'New Member 2' },
]);

function approveRequest(requestId: number) {
  alert(`Approved request for user ID: ${requestId}`);
}

function rejectRequest(requestId: number) {
  alert(`Rejected request for user ID: ${requestId}`);
}

function blockRequest(requestId: number) {
  alert(`Blocked request for user ID: ${requestId}`);
}

const joinGroup = () => {
  alert('Join group clicked');
};
</script>

<style scoped>
.p-6 {
  padding: 1.5rem;
}
.md\:p-10 {
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
</style>
