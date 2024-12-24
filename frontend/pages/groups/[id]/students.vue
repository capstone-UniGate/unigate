<script setup lang="ts">
import { ScrollArea } from "@/components/ui/scroll-area";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { useRoute, useRouter } from "vue-router";
import { useToast } from "@/components/ui/toast/use-toast";
import { ref, onMounted } from "vue";
import { useCurrentStudent } from "@/composables/useCurrentStudent";
import { useGroups } from "@/composables/useGroups";
import { User } from "lucide-vue-next";

const { getGroupStudents, handleUserBlock } = useGroups();
const { currentStudent, getCurrentStudent } = useCurrentStudent();
const { toast } = useToast();

const route = useRoute();
const router = useRouter();
const groupId = route.params.id;
const members = ref([]);
const superStudents = ref([]);
const blockedStudents = ref([]);
const isLoading = ref(true);
const activeTab = ref("members");

// Function to check if current user is a super student
const isSuperStudent = () => {
  return superStudents.value.some(
    (student) => student.id === currentStudent.value?.id,
  );
};

const notSamestudent = () => {
  return superStudents.value.some(
    (student) => student.id !== currentStudent.value?.id,
  );
};

// Function to load members
const loadMembers = async () => {
  try {
    isLoading.value = true;
    const response = await getGroupStudents(groupId.toString());
    members.value = response.students || [];
    superStudents.value = response.super_students || [];
    blockedStudents.value = response.blocked_students || [];
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

const handleUnblock = async (studentId: string) => {
  try {
    const response = await handleUserBlock(
      groupId.toString(),
      studentId,
      "unblock",
    );

    if (response) {
      // Reload members to get updated lists
      await loadMembers();
    }
  } catch (error) {
    toast({
      title: "Error",
      description: "Failed to unblock user",
      variant: "destructive",
    });
  }
};

// Load current student and members when component mounts
onMounted(async () => {
  await getCurrentStudent();
  await loadMembers();
});
</script>

<template>
  <div class="p-6 bg-gray-50 min-h-screen">
    <!-- Header with Tabs -->
    <div class="flex flex-col ml-8 mt-4">
      <h1 class="text-3xl font-semibold text-gray-800 mb-6">Group Members</h1>

      <!-- Tabs - Only visible to super students -->
      <div v-if="isSuperStudent()" class="flex space-x-4 mb-6">
        <button
          class="px-4 py-2 rounded-lg font-medium transition-colors"
          :class="[
            activeTab === 'members'
              ? 'bg-blue-500 text-white'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300',
          ]"
          id="members_tab"
          @click="activeTab = 'members'"
        >
          Active Members ({{ members.length }})
        </button>
        <button
          class="px-4 py-2 rounded-lg font-medium transition-colors"
          :class="[
            activeTab === 'blocked'
              ? 'bg-blue-500 text-white'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300',
          ]"
          id="blocked_tab"
          @click="activeTab = 'blocked'"
        >
          Blocked Users ({{ blockedStudents.length }})
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="flex justify-center items-center h-96">
      <div class="text-gray-500">Loading members...</div>
    </div>

    <!-- Content Area -->
    <ScrollArea
      v-else
      class="h-96 w-full rounded-lg border border-gray-300 bg-white shadow-sm p-4 m-4"
      id="members_area"
    >
      <!-- Active Members List -->
      <div v-if="activeTab === 'members'">
        <div
          v-if="members.length === 0"
          class="text-center text-gray-500 py-4"
          id="no_members"
        >
          No members found in this group.
        </div>

        <div
          v-else
          v-for="member in members"
          :key="member.id"
          id="member"
          class="py-3 px-4 bg-gray-100 rounded-md mb-2 flex items-center justify-between hover:bg-gray-200 transition duration-200"
        >
          <!-- Avatar with Default Image -->
          <Avatar class="mr-4">
            <AvatarImage
              src="https://via.placeholder.com/50"
              alt="Default Avatar"
              id="avatar"
            />
            <AvatarFallback
              >{{ member.name?.[0] }}{{ member.surname?.[0] }}</AvatarFallback
            >
          </Avatar>

          <!-- Member Info -->
          <div class="flex-grow">
            <div class="flex flex-col">
              <!-- Member Name -->
              <span id="member_name" class="text-gray-800 font-bold">
                {{ member.name }} {{ member.surname }}
              </span>
              <!-- Member Email -->
              <span id="member_email" class="text-gray-600 text-sm">
                {{ member.email }}
              </span>
              <!-- Student Number -->
              <span id="member_number" class="text-gray-500 text-xs">
                Student #{{ member.number }}
              </span>
            </div>
          </div>

          <!-- Block Button - Only visible to super students -->
          <button
            v-if="isSuperStudent() && notSamestudent(member.id)"
            @click="handleBlock(member.id)"
            class="px-4 py-2 text-sm font-medium text-white bg-red-500 rounded-lg hover:bg-red-600 transition"
            id="block_member"
          >
            Block
          </button>
        </div>
      </div>

      <!-- Blocked Users List -->
      <div v-else-if="activeTab === 'blocked' && isSuperStudent()">
        <div
          v-if="blockedStudents.length === 0"
          class="text-center text-gray-500 py-4"
          id="no_blocked_users"
        >
          No blocked users.
        </div>

        <div
          v-else
          v-for="user in blockedStudents"
          :key="user.id"
          id="blocked_student"
          class="py-3 px-4 bg-gray-100 rounded-md mb-2 flex items-center justify-between hover:bg-gray-200 transition duration-200"
        >
          <Avatar class="mr-4">
            <AvatarImage
              src="https://via.placeholder.com/50"
              alt="Default Avatar"
            />
            <AvatarFallback
              >{{ user.name?.[0] }}{{ user.surname?.[0] }}</AvatarFallback
            >
          </Avatar>

          <div class="flex-grow">
            <div class="flex flex-col">
              <span class="text-gray-800 font-bold" id="blocked_student_name">
                {{ user.name }} {{ user.surname }}
              </span>
              <span class="text-gray-600 text-sm" id="blocked_student_email">
                {{ user.email }}
              </span>
              <span class="text-gray-500 text-xs" id="blocked_student_number">
                Student #{{ user.number }}
              </span>
            </div>
          </div>

          <!-- Unblock Button -->
          <button
            @click="handleUnblock(user.id)"
            class="px-4 py-2 text-sm font-medium text-white bg-green-500 rounded-lg hover:bg-green-600 transition"
            id="unblock_student"
          >
            Unblock
          </button>
        </div>
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
