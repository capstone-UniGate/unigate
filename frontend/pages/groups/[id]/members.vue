<script setup lang="ts">
import { ScrollArea } from "@/components/ui/scroll-area";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"; // Import Avatar components
import { useRoute, useRouter } from "vue-router";

const route = useRoute();
const router = useRouter();
const groupId = route.params.id;

// Mock members (call API)
const groupMembers = [
  { id: 1, name: "Alice" },
  { id: 2, name: "Bob" },
  { id: 3, name: "Charlie" },
  { id: 4, name: "David" },
];
</script>



<template>
  <div class="p-6 bg-gray-50 min-h-screen">
    <!-- Header -->
    <h1 class="text-3xl font-semibold text-gray-800 mb-6">
      Members of Group {{ groupId }}
    </h1>

    <!-- Scrollable Area -->
    <ScrollArea class="h-96 w-full rounded-lg border border-gray-300 bg-white shadow-sm p-4">
      
      <!-- Member List -->
      <div
        v-for="member in groupMembers"
        :key="member.id"
        class="py-3 px-4 bg-gray-100 rounded-md mb-2 flex items-center hover:bg-gray-200 transition duration-200"
      >
        <!-- Avatar with Default Image -->
        <Avatar class="mr-4">
          <AvatarImage src="https://via.placeholder.com/50" alt="Default Avatar" />
        </Avatar>
        
        <!-- Member Name -->
        <span class="text-gray-800 font-bold">{{ member.name }}</span>
      </div>
    </ScrollArea>
  </div>
</template>

<style scoped>
</style>
