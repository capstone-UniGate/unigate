<template>
  <div
    class="rounded-lg border bg-card text-card-foreground shadow-sm transition-shadow hover:shadow-md p-4"
  >
    <!-- Course Name and Group Tag -->
    <h2
      id="course_name_card"
      class="text-base font-semibold flex items-center justify-between"
    >
      {{ course }}
    </h2>

    <!-- Exam List -->
    <div class="mt-3 space-y-2">
      <div
        :id="'course_data_' + (index + 1)"
        v-for="exam in course_data"
        :key="exam.exam_date"
        class="flex justify-between items-center rounded-md border bg-muted/50 p-2"
      >
        <div class="mt-3 space-y-2">
          <span class="text-sm">{{ exam.exam_date }}</span>
          <div
            :id="'course_stats_' + index"
            class="flex justify-between items-center rounded-md border bg-muted/50 p-2"
          >
            <div
              class="flex justify-between items-center rounded-md bg-muted/50 p-2"
            >
              <span class="text-sm"
                >Average members per group: {{ exam.average_members }}</span
              >
            </div>
            <div
              class="flex justify-between items-center rounded-md bg-muted/50 p-2"
            >
              <span class="text-sm"
                >Minimum members per group: {{ exam.min_members }}</span
              >
            </div>
            <span class="text-sm"
              >Maximum members per group: {{ exam.max_members }}</span
            >
            <span class="text-sm"
              >Total numbers of members: {{ exam.total_members }}</span
            >
            <span class="text-sm"
              >Total numbers of groups: {{ exam.total_groups }}</span
            >
          </div>
        </div>
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
  course: string;
  course_data: {
    exam_date: string;
    average_members: number;
    min_members: number;
    max_members: number;
    total_members: number;
    total_groups: number;
  }[];
}>();
</script>
