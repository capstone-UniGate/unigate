<template>
  <div class="container mx-auto p-6">
    <div class="flex flex-col md:flex-row bg-white rounded-lg shadow-md overflow-hidden max-w-3xl mx-auto">

      <div class="w-full md:w-1/2 p-6 flex items-center justify-center">
        <CardContent class="max-w-full">
        </CardContent>
      </div>

      <div class="w-full md:w-1/2 p-6">
        <h1 class="text-3xl font-bold text-gray-800 mb-2">{{ group?.name || 'Loading...' }}</h1>
        <CardDescription class="text-gray-600 mb-4">
          {{ group.description || 'No description available.' }}
        </CardDescription>

        <div class="mb-6">
          <h2 class="text-xl font-semibold text-gray-700 mb-2">Members</h2>
          <ul class="text-gray-600">
            <li v-for="member in group.members || []" :key="member.id">
              <NuxtLink :to="`/member/${member.id}`" class="text-blue-500 hover:underline">
                {{ member.name }}
              </NuxtLink>
            </li>
          </ul>
        </div>

        <div class="text-center mt-4">
          <Button v-if="!isMember" @click="joinGroup" class="bg-blue-500 text-white px-4 py-2 rounded-md">Join Group</Button>
          <p v-else class="text-green-500">You are a member of this group.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router';
import { ref } from 'vue';
import { CardContent, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

const route = useRoute();
const groupId = route.params.id;

const groupsData = [
  { id: '1', name: 'Group 1', description: 'This is a sample description for Group 1.', members: [{ id: 1, name: 'Sara' }, { id: 2, name: 'John' }, { id: 3, name: 'Daniel' }] },
  { id: '2', name: 'Group 2', description: 'This is a sample description for Group 2.', members: [{ id: 4, name: 'David' }, { id: 5, name: 'Alice' }, { id: 6, name: 'Lisa' }] },
];

const group = groupsData.find(g => g.id === groupId) || { name: 'Loading...', description: '', members: [] };
const isMember = ref(false);

function joinGroup() {
  alert('Join group clicked');
}
</script>

<style scoped>
.container {
  max-width: 1200px;
}

img {
  width: 100%;
  height: auto;
  object-fit: cover;
  border-radius: 8px;
  max-height: 300px;
}

.max-w-3xl {
  background-color: #ffffff;
  border-radius: 10px;
}
</style>
