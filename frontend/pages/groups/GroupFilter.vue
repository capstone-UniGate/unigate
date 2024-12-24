<script setup lang="ts">
import { ref, defineEmits } from 'vue';

const course = ref('');
const examDate = ref('');
const participants = ref<number | null>(null);
const isPublic = ref<boolean | null>(null);
const orderBy = ref('NEWEST');

const emit = defineEmits(['apply-filters']);

const applyFilters = () => {
  emit('apply-filters', {
    course: course.value,
    examDate: examDate.value,
    participants: participants.value,
    isPublic: isPublic.value,
    orderBy: orderBy.value,
  });
};

const clearFilters = () => {
  course.value = '';
  examDate.value = '';
  participants.value = null;
  isPublic.value = null;
  orderBy.value = 'NEWEST';
  applyFilters();
};
</script>

<template>
  <div class="flex flex-wrap gap-4 mb-4 items-center">
    <div class="flex flex-col">
      <label for="course" class="mb-1 text-sm">Course</label>
      <input id="course" v-model="course" class="input border rounded p-2" placeholder="Course" />
    </div>
    <div class="flex flex-col">
      <label for="examDate" class="mb-1 text-sm">Exam Date</label>
      <input id="examDate" v-model="examDate" class="input border rounded p-2" type="date" placeholder="Exam Date" />
    </div>
    <div class="flex flex-col">
      <label for="participants" class="mb-1 text-sm">Number of Participants</label>
      <input id="participants" v-model.number="participants" class="input border rounded p-2" type="number" placeholder="Number of Participants" min="0" />
    </div>
    <div class="flex flex-col">
      <label for="isPublic" class="mb-1 text-sm">Type</label>
      <select id="isPublic" v-model="isPublic" class="select border rounded p-2">
        <option :value="null">All</option>
        <option :value="true">Public</option>
        <option :value="false">Private</option>
      </select>
    </div>
    <div class="flex flex-col">
      <label for="orderBy" class="mb-1 text-sm">Order By</label>
      <select id="orderBy" v-model="orderBy" class="select border rounded p-2">
        <option value="NEWEST">Newest</option>
        <option value="OLDEST">Oldest</option>
      </select>
    </div>
    <div class="flex flex-col">
      <button @click="applyFilters" class="button bg-blue-500 text-white rounded p-2 mt-6">Apply Filters</button>
    </div>
    <div class="flex flex-col">
      <button @click="clearFilters" class="button bg-gray-300 text-black rounded p-2 mt-6">Clear Filters</button>
    </div>
  </div>
</template>