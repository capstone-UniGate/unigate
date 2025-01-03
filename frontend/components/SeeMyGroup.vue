<script setup lang="ts">
const { groups, isLoading, isError, getMyGroups } = useStudentGroups();
const router = useRouter();

const gotoAllGroups = () => {
  // Fetch groups for the authenticated user
  router.push("/groups");
};

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
      data-testid="error-message"
    />

    <div class="flex justify-end items-center py-2">
      <div>
        <h1
          class="text-2xl font-semibold text-gray-800"
          data-testid="page-heading"
        >
          Your Enrolled Groups
        </h1>
        <Button
          @click="gotoAllGroups"
          class="bg-gradient-to-r from-indigo-500 to-blue-500 text-white font-semibold py-1 px-2 rounded-lg shadow-lg hover:from-blue-500 hover:to-blue-600 hover:shadow-xl active:scale-95 transition-all m-4"
        >
          All Groups
        </Button>
      </div>

      <Button
        @click="() => $router.push('create')"
        class="ml-auto bg-gradient-to-r from-indigo-500 to-blue-500 text-white font-semibold py-1 px-2 rounded-lg shadow-lg hover:from-blue-500 hover:to-blue-600 hover:shadow-xl active:scale-95 transition-all"
        data-testid="create-group-button"
      >
        Create a new group
      </Button>
    </div>

    <!-- Loading Indicator -->
    <div v-if="isLoading" class="py-4" data-testid="loading-indicator">
      <LoadingIndicator />
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
