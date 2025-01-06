<template>
  <div
    class="rounded-lg border bg-card text-card-foreground shadow-sm transition-shadow hover:shadow-md p-4"
  >
    <!-- Course Name and Group Tag -->
    <h2 id="course_name_card" class="text-base font-semibold flex items-center justify-between">
      {{ course.name }}
      <span id="course_number_groups"
        class="rounded-full bg-emerald-500 text-white px-2 py-1 text-xs font-medium"
      >
        Groups: {{ groupCount }}
      </span>
    </h2>

    <!-- Exam List -->
    <div class="mt-3 space-y-2">
      <div
        :id="'course_data_' + (index + 1)" 
        v-for="(exam, index) in course.exams"
        :key="exam.date"
        class="flex justify-between items-center rounded-md border bg-muted/50 p-2"
      >
        <span class="text-sm">{{ exam.date }}</span>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { PropType } from "vue";

interface Course {
  id: number;
  name: string;
  exams: { date: string; groupCount: number }[];
}

const props = defineProps<{
  course: Course;
  groupCount: number;
}>();
</script>
