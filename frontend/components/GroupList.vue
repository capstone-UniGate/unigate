<script setup lang="ts">
const { groups, isLoading, isError, getAllGroups } = useGroups();

onMounted(() => {
  getAllGroups();
});
</script>

<template>
  <div class="p-4">
    <h1 class="text-2xl font-bold mb-4">Explore Groups</h1>

    <!-- Error Message Component -->
    <ErrorMessage v-if="isError" @retry="getAllGroups" />

    <!-- Loading Indicator Component -->
    <LoadingIndicator v-if="isLoading" />

    <!-- Group Cards List -->
    <div
      v-if="!isLoading && !isError"
      class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4"
    >
      <GroupCard v-for="group in groups" :key="group.id" :group="group" />
    </div>
  </div>
</template>
