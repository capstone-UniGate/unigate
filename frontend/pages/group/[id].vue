<template>
  <div class="p-6 md:p-10">
    <div class="flex items-center gap-4 mb-6">
      <!-- Avatar with Click Event to Open Modal -->
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

    <!-- Show Join Button Only if User is Not a Member -->
    <div v-if="!isMember" class="text-center mt-6">
      <Button class="bg-blue-500 text-white px-4 py-2 rounded-md">Join Group</Button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { Button } from '@/components/ui/button';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { useRoute } from 'vue-router';

const route = useRoute();
const groupId = route.params.id;
const currentUserId = 3; // Assume this is the logged-in user’s ID
const showModal = ref(false);

// Mock data to represent the groups and their members
const groupsData = [
  { 
    id: '1', 
    name: 'Group 1', 
    description: 'This is a sample description for Group 1, This is a sample description for Group 1, This is a sample description for Group 1, This is a sample description for Group 1.', 
    isPrivate: true, 
    members: [{ id: 1, name: 'Alice' }, { id: 2, name: 'Bob' }] 
  },
  { 
    id: '2', 
    name: 'Group 2', 
    description: 'This is a sample description for Group 2.', 
    isPrivate: false, 
    members: [{ id: 3, name: 'David' }, { id: 4, name: 'Alice' }] // Assuming the user is a member of Group 2
  },
];
const group = groupsData.find(g => g.id === groupId) || { name: 'Group...', description: '', isPrivate: false, members: [] };

// Check if the current user is a member of the group
const isMember = computed(() => group.members.some(member => member.id === currentUserId));

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
