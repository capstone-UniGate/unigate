<template>
  <div class="container mx-auto px-4 py-8 mt-16">
    <div v-if="isLoading">
      <LoadingIndicator />
    </div>
    <div v-else-if="isError">
      <ErrorMessage @retry="initializeData" />
    </div>
    <div v-else class="max-w-2xl mx-auto bg-white rounded-lg shadow-md p-6">
      <!-- User Profile Header -->
      <div class="flex items-center space-x-4 mb-6">
        <Avatar class="w-20 h-20">
          <AvatarImage
            src="https://github.com/radix-vue.png"
            alt="@radix-vue"
          />
          <AvatarFallback>{{ getInitials }}</AvatarFallback>
        </Avatar>
        <div>
          <h1 class="text-2xl font-bold text-gray-900">
            {{ currentStudent?.name }} {{ currentStudent?.surname }}
          </h1>
          <p class="text-gray-500">
            Student Number: {{ currentStudent?.number }}
          </p>
          <!-- Role Badge -->
          <span
            :class="[
              'inline-block px-3 py-1 mt-2 rounded-full text-sm font-medium',
              userRole === 'Student'
                ? 'bg-blue-100 text-blue-800'
                : 'bg-purple-100 text-purple-800',
            ]"
          >
            {{ userRole }}
          </span>
        </div>
      </div>

      <!-- User Details -->
      <div class="space-y-4">
        <div class="border-t pt-4">
          <h2 class="text-lg font-semibold text-gray-900 mb-2">
            Contact Information
          </h2>
          <p class="text-gray-600">Email: {{ currentStudent?.email }}</p>
          <p class="text-gray-600">Role: {{ userRole }}</p>
        </div>

        <div class="border-t pt-4">
          <h2 class="text-lg font-semibold text-gray-900 mb-2">Groups</h2>
          <div v-if="userGroups.length > 0" class="space-y-2">
            <div
              v-for="group in userGroups"
              :key="group.id"
              class="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
            >
              <span>{{ group.name }}</span>
              <Button
                @click="router.push(`/groups/${group.id}`)"
                variant="outline"
                class="text-sm"
              >
                View Group
              </Button>
            </div>
          </div>
          <p v-else class="text-gray-500">Not a member of any groups yet.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useCurrentStudent } from "@/composables/useCurrentStudent";
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import LoadingIndicator from "@/components/LoadingIndicator.vue";
import ErrorMessage from "@/components/ErrorMessage.vue";

const router = useRouter();
const { currentStudent, getCurrentStudent } = useCurrentStudent();
const userGroups = ref([]);
const isLoading = ref(true);
const isError = ref(false);

// Compute user role based on email prefix
const userRole = computed(() => {
  if (!currentStudent.value?.email) return "Unknown";
  const emailPrefix = currentStudent.value.email.charAt(0).toLowerCase();
  return emailPrefix === "s"
    ? "Student"
    : emailPrefix === "p"
      ? "Professor"
      : "Unknown";
});

// Compute initials from student name

// Initialize data
const initializeData = async () => {
  try {
    isLoading.value = true;
    isError.value = false;

    if (!currentStudent.value) {
      await getCurrentStudent();
    }

    // Here you would fetch user's groups
    // const groups = await fetchUserGroups()
    // userGroups.value = groups
  } catch (error) {
    console.error("Error initializing user data:", error);
    isError.value = true;
  } finally {
    isLoading.value = false;
  }
};

// Initialize on component mount
onMounted(initializeData);
</script>
