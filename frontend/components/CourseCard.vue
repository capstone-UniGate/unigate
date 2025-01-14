<template>
  <div
    class="rounded-lg border bg-card text-card-foreground shadow-sm transition-shadow hover:shadow-md p-4"
  >
    <!-- Course Name and Group Tag -->
    <h2
      id="course_name_card"
      class="text-base font-semibold flex items-center justify-between"
    >
      {{ course.name }}
      <span
        id="course_number_groups"
        class="rounded-full bg-emerald-500 text-white px-2 py-1 text-xs font-medium"
      >
        Groups: {{ groupCount }}
      </span>
    </h2>

    <!-- Average People per Group -->
    <p id="course_avg_members_group" class="text-sm mt-2">
      Average members per group: {{ avgMembers }}
    </p>

    <!-- Number of Active Groups -->
    <p id="course_number_active_groups" class="text-sm mt-2">
      Number of Active Groups: {{ activeGroupCount }}
    </p>

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
  exams: {
    date: string;
    groupCount: number;
    avgMembers: number;
    activeGroupCount: number;
  }[];
}

const props = defineProps<{
  course: Course;
  groupCount: number;
  avgMembers: number;
  activeGroupCount: number;
}>();
</script>
