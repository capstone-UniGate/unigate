<script setup lang="ts">
import { ScrollArea } from "@/components/ui/scroll-area";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"; // Import Avatar components
import { useRoute, useRouter } from "vue-router";

const route = useRoute();
const router = useRouter();
const groupId = route.params.id;
const members = await useApiFetch(`groups/${groupId}/get_members`);
</script>

<template>
  <div class="p-6 bg-gray-50 min-h-screen">
    <!-- Header -->
    <h1 class="text-3xl font-semibold text-gray-800 ml-8 mt-4">
      Group Members
    </h1>

    <!-- Scrollable Area -->
    <ScrollArea
      class="h-96 w-full rounded-lg border border-gray-300 bg-white shadow-sm p-4 m-4"
    >
      <!-- Member List -->
      <div
        v-for="member in members"
        :key="member.id"
        class="py-3 px-4 bg-gray-100 rounded-md mb-2 flex items-center hover:bg-gray-200 transition duration-200"
        data-testid="member"
      >
        <!-- Avatar with Default Image -->
        <Avatar class="mr-4">
          <AvatarImage
            src="https://via.placeholder.com/50"
            alt="Default Avatar"
          />
        </Avatar>

        <!-- Member Name -->
        <span class="text-gray-800 font-bold"
          >{{ member.name }} {{ member.surname }}</span
        >
      </div>
    </ScrollArea>

    <NuxtLink
      :to="`/groups/${groupId}`"
      class="bg-gradient-to-r from-indigo-500 to-blue-500 text-white font-semibold py-2 px-3 rounded-md shadow-lg hover:from-blue-500 hover:to-blue-600 hover:shadow-xl active:scale-95 transition-all m-8"
    >
      Back to Group Details
    </NuxtLink>
  </div>
</template>

<style scoped></style>
