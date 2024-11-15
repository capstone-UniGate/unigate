<script setup lang="ts">
import { ref, onMounted } from "vue";
import { userGroupData } from "@/composables/userGroupData";

const groups = ref([]);
const isLoading = ref(true);
const isError = ref(false);

async function loadGroups() {
  try {
    isError.value = false;
    isLoading.value = true;
    groups.value = userGroupData();
  } catch (error) {
    isError.value = true;
  } finally {
    isLoading.value = false;
  }
}

onMounted(() => {
  loadGroups();
});
</script>

<template>
  <div class="container mx-auto p-6">
        <!-- Error Message Component -->
    <ErrorMessage v-if="isError" @retry="loadGroups" />
    <!-- Loading Indicator Component -->
    <LoadingIndicator v-if="isLoading" />

    <div class="flex justify-end items-center mb-6 py-2">
    <h1 class="text-2xl font-semibold text-gray-800 mb-6">Your Enrolled Groups</h1>
      <!-- Add the button here -->
      <Button class="ml-auto">Create a new group</Button>
    </div>

    <!-- Group Cards List -->
    <div v-if="!isLoading && !isError"
      class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4"
    >
      <GroupCard v-for="group in groups" :key="group.id" :group="group" />
    </div>
</div>
</template>
