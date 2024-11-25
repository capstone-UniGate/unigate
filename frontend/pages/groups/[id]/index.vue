<template>
  <Toaster />

  <div class="p-6 md:p-10 flex flex-col lg:flex-row items-center lg:items-start text-center lg:text-left gap-10">
    <!-- Left Side: Group Details or Members -->
    <div class="flex-grow w-full lg:w-2/3">
      <!-- Show members if in the "members" section -->
      <div v-if="isViewingMembers">
        <h1 class="text-2xl font-semibold text-gray-800 mb-6">
          Members of <span class="text-primary-600">{{ group.name || "Group" }}</span>
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
        <div class="flex items-center gap-4 mb-6 justify-center lg:justify-start">
          <Avatar class="cursor-pointer w-20 h-20 rounded-full border border-gray-300">
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
              :to="`/groups/${groupId}/members`"
              class="text-blue-500 hover:underline"
            >
              members
            </NuxtLink>
            : <span class="font-semibold">{{ group.members.length }}</span>
          </p>
        </div>

        <div class="text-left mb-6">
          <p class="text-sm text-gray-500">Description</p>
          <p class="text-gray-700 text-base bg-gray-50 border border-gray-200 rounded-lg p-4">
            {{ group.description || "No description available." }}
          </p>
        </div>

        <div class="text-left mb-6">
          <p class="text-sm text-gray-500">Tags</p>
          <p class="text-gray-700 text-base bg-gray-50 border border-gray-200 rounded-lg p-4">
            [tag1], [tag2]
          </p>
        </div>

        <!-- Join Group Button -->
        <div v-if="!isMember && !isSuperstudent" class="text-center mt-6">
          <Button
            @click="joinGroup"
            class="ml-auto bg-gradient-to-r from-indigo-500 to-blue-500 text-white font-semibold py-1 px-2 rounded-lg shadow-lg hover:from-blue-500 hover:to-blue-600 hover:shadow-xl active:scale-95 transition-all"          >
            Join Group
          </Button>
        </div>
      </div>
    </div>

    <!-- Right Side: Superstudent Join Requests Section -->
    <div
      v-if="!isViewingMembers && isSuperstudent && group.isPrivate"
      class="w-full lg:w-80"
    >
      <Button
        @click="navigateToRequests"
        class="ml-auto mt-4 bg-gradient-to-r from-indigo-500 to-blue-500 text-white font-semibold py-1 px-2 rounded-lg shadow-lg hover:from-blue-500 hover:to-blue-600 hover:shadow-xl active:scale-95 transition-all"
      >
        Manage Requests
      </Button>

      
    </div>
  </div>
</template>

<script setup lang="ts">
import { Toaster } from "@/components/ui/toast";
import { useToast } from "@/components/ui/toast/use-toast";
import { ref, computed } from "vue";
import { Button } from "@/components/ui/button";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { ScrollArea } from "@/components/ui/scroll-area";
import { useRoute, useRouter } from "vue-router";

const route = useRoute();
const router = useRouter();
const toast = useToast();

const groupId = route.params.id;
const currentUserId = 3;

// Mock data to represent the groups and their members
const groupsData = [
  {
    id: "1",
    name: "Group 1",
    description: "This is a sample description for Group 1.",
    isPrivate: true,
    creatorId: 3,
    members: [
      { id: 1, name: "Alice" },
      { id: 2, name: "Bob" },
    ],
    rejectedUsers: [4],
    blockedUsers: [5],
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
  },
];

const group = groupsData.find((g) => g.id === groupId) || {
  name: "Group...",
  description: "",
  isPrivate: false,
  creatorId: null,
  members: [],
};

const isViewingMembers = computed(() => route.path.endsWith("/members"));
const isSuperstudent = computed(() => group.creatorId === currentUserId);
const isMember = computed(() => group.members.some((member) => member.id === currentUserId));

const joinGroup = () => {
  alert("Join group clicked");
};
const navigateToRequests = () => router.push(`/groups/${groupId}/requests`);
</script>

<style scoped>

</style>
