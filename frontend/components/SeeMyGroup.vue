<script setup lang="ts">
const { groups, isLoading, isError, getMyGroups } = useStudentGroups();

onMounted(() => {
  getMyGroups();
});
</script>

<template>
  <div class="container mx-auto p-6">
    <!-- Error Message Component -->
    <ErrorMessage
      v-if="isError"
      @retry="getMyGroups"
      data-testid="error-mesMsage"
    />

    <!-- Loading Indicator Component -->
    <LoadingIndicator v-if="isLoading" data-testid="loading-indicator" />

    <div class="flex justify-end items-center mb-6 py-2">
      <h1
        class="text-2xl font-semibold text-gray-800"
        data-testid="page-heading"
      >
        Your Enrolled Groups
      </h1>
      <Button
        @click="() => $router.push('create')"
        class="ml-auto bg-gradient-to-r from-indigo-500 to-blue-500 text-white font-semibold py-1 px-2 rounded-lg shadow-lg hover:from-blue-500 hover:to-blue-600 hover:shadow-xl active:scale-95 transition-all"
        data-testid="create-group-button"
      >
        Create a new group
      </Button>
    </div>

    <!-- Group Cards List -->
    <div
      v-if="!isLoading && !isError"
      class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4"
      data-testid="group-cards-container"
    >
      <GroupCard
        v-for="group in groups"
        :key="group.id"
        :group="group"
        data-testid="group-card"
      />
    </div>
  </div>
</template>
