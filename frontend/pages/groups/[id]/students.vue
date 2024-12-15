<script setup lang="ts">
import { ScrollArea } from "@/components/ui/scroll-area";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { useRoute, useRouter } from "vue-router";
import { useToast } from "@/components/ui/toast/use-toast";
import { ref, onMounted } from "vue";

import { useGroups } from "@/composables/useGroups";

const { getGroupStudents, handleUserBlock } = useGroups();
const { toast } = useToast();

const route = useRoute();
const router = useRouter();
const groupId = route.params.id;
const members = ref([]);
const isLoading = ref(true);

// Function to load members
const loadMembers = async () => {
  try {
    isLoading.value = true;
    const response = await getGroupStudents(groupId.toString());
    // Access the students array from the response
    members.value = response.students || [];
  } catch (error) {
    toast({
      title: "Error",
      description: "Failed to load group members",
      variant: "destructive",
    });
  } finally {
    isLoading.value = false;
  }
};

const handleBlock = async (studentId: string) => {
  try {
    const response = await handleUserBlock(
      groupId.toString(),
      studentId,
      "block",
    );

    if (response) {
      // Remove the blocked user from the members list
      members.value = members.value.filter((member) => member.id !== studentId);

      toast({
        title: "Success",
        description: "User has been blocked",
        variant: "success",
      });

      // Reload members to get updated list
      await loadMembers();
    }
  } catch (error) {
    toast({
      title: "Error",
      description: "Failed to block user",
      variant: "destructive",
    });
  }
};

// Load members when component mounts
onMounted(() => {
  loadMembers();
});
</script>

<template>
  <div class="p-6 bg-gray-50 min-h-screen">
    <!-- Header -->
    <h1 class="text-3xl font-semibold text-gray-800 ml-8 mt-4">
      Group Members
    </h1>

    <!-- Loading State -->
    <div v-if="isLoading" class="flex justify-center items-center h-96">
      <div class="text-gray-500">Loading members...</div>
    </div>

    <!-- Scrollable Area -->
    <ScrollArea
      v-else
      class="h-96 w-full rounded-lg border border-gray-300 bg-white shadow-sm p-4 m-4"
    >
      <!-- Empty State -->
      <div v-if="members.length === 0" class="text-center text-gray-500 py-4">
        No members found in this group.
      </div>

      <!-- Member List -->
      <div
        v-else
        v-for="member in members"
        :key="member.id"
        class="py-3 px-4 bg-gray-100 rounded-md mb-2 flex items-center justify-between hover:bg-gray-200 transition duration-200"
        data-testid="member"
      >
        <!-- Avatar with Default Image -->
        <Avatar class="mr-4">
          <AvatarImage
            src="https://via.placeholder.com/50"
            alt="Default Avatar"
          />
          <AvatarFallback
            >{{ member.name?.[0] }}{{ member.surname?.[0] }}</AvatarFallback
          >
        </Avatar>

        <!-- Member Info -->
        <div class="flex-grow">
          <div class="flex flex-col">
            <!-- Member Name -->
            <span class="text-gray-800 font-bold">
              {{ member.name }} {{ member.surname }}
            </span>
            <!-- Member Email -->
            <span class="text-gray-600 text-sm">
              {{ member.email }}
            </span>
            <!-- Student Number -->
            <span class="text-gray-500 text-xs">
              Student #{{ member.number }}
            </span>
          </div>
        </div>

        <!-- Block Button -->
        <button
          @click="handleBlock(member.id)"
          class="px-4 py-2 text-sm font-medium text-white bg-red-500 rounded-lg hover:bg-red-600 transition"
        >
          Block
        </button>
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
