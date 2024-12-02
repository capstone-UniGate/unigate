<script setup lang="ts">
const groups = ref();
const isLoading = ref(false);
const isError = ref(false);

async function loadGroups() {
  try {
    isError.value = false;
    isLoading.value = true;
    groups.value = await useApiFetch("groups/get");
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
  <div class="p-4">
    <h1 class="text-2xl font-bold mb-4">Explore Groups</h1>

    <!-- Error Message Component -->
    <ErrorMessage v-if="isError" @retry="loadGroups" />

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
