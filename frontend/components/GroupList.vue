<script setup lang="ts">
const router = useRouter();
const { groups, isLoading, isError, getAllGroups, searchGroups } = useGroups();

const gotoYourGroups = () => {
  // Fetch groups for the authenticated user
  router.push("/groups/see-my-group");
};

onMounted(() => {
  getAllGroups();
});
</script>

<template>
  <div class="p-4">
    <h1 class="text-2xl font-bold mb-4">Explore Groups</h1>

    <!-- Error Message Component -->
    <ErrorMessage v-if="isError" @retry="getAllGroups" />

    <Button
      @click="gotoYourGroups"
      class="ml-auto bg-gradient-to-r from-indigo-500 to-blue-500 text-white font-semibold py-1 px-2 rounded-lg shadow-lg hover:from-blue-500 hover:to-blue-600 hover:shadow-xl active:scale-95 transition-all mb-4"
    >
      See Your Groups
    </Button>

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
