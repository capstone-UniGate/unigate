<template>
  <div class="p-4">
    <GroupFilter @apply-filters="handleApplyFilters" />
    <div v-if="isLoading" class="text-center text-gray-500">Loading...</div>
    <div v-if="isError" class="text-red-500 mt-4">{{ errorMessage }}</div>
    <GroupList :groups="groups" />
  </div>
</template>

<script setup lang="ts">
import GroupFilter from './GroupFilter.vue';
import GroupList from '@/components/GroupList.vue';
import { useGroups } from '@/composables/useGroups';

const { groups, isLoading, isError, errorMessage, getAllGroups } = useGroups();

const fetchGroups = async (filters = {}) => {
  await getAllGroups(filters);
};

const handleApplyFilters = (filters) => {
  fetchGroups(filters);
};

fetchGroups();
</script>