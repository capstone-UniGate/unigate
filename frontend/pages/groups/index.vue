<template>
  <div class="p-4">

    <!-- Filter Component -->
    <GroupFilter @apply-filters="handleApplyFilters" :fetch-courses="fetchCourses" />

    <!-- Error Handling -->
    <ErrorMessage v-if="isError" :message="errorMessage" @retry="fetchGroups" />

    <!-- Groups List -->
    <GroupList v-if="!isLoading && !isError" :groups="groups" />
  </div>
</template>


<script setup lang="ts">
import GroupFilter from './GroupFilter.vue';
import GroupList from '@/components/GroupList.vue';
import ErrorMessage from '@/components/ErrorMessage.vue';
import { useGroups } from '@/composables/useGroups';

const { groups, isLoading, isError, errorMessage, getAllGroups, getCourses } = useGroups();

// Function to fetch groups
const fetchGroups = async (filters = {}) => {
  await getAllGroups(filters);
};

// Function to fetch courses
const fetchCourses = async () => {
  return await getCourses();
};

// Handle applying filters
const handleApplyFilters = (filters) => {
  fetchGroups(filters);
};

// Fetch groups on mount
fetchGroups();
</script>
