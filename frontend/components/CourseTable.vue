<template>
  <div
    class="rounded-lg m-8 border bg-card text-card-foreground shadow-sm transition-shadow hover:shadow-md p-4"
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
        v-if="course_data"
        class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4"
      >
        <div
          :id="'course_data_' + 1"
          v-for="exam in course_data"
          :key="exam.exam_date"
          class="flex justify-between items-center rounded-md border bg-muted/50 p-2"
        >
          <div class="mt-3 space-y-2">
            <h3>{{ exam.exam_date }}</h3>
            <div
              :id="'course_stats_' + 2"
              class="justify-between items-center rounded-md border bg-muted/50 p-2"
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
              <div
                class="flex justify-between items-center rounded-md bg-muted/50 p-2"
              >
                <span class="text-sm"
                  >Maximum members per group: {{ exam.max_members }}</span
                >
              </div>
              <div
                class="flex justify-between items-center rounded-md bg-muted/50 p-2"
              >
                <span class="text-sm"
                  >Total numbers of members: {{ exam.total_members }}</span
                >
              </div>
              <div
                class="flex justify-between items-center rounded-md bg-muted/50 p-2"
              >
                <span class="text-sm"
                  >Total numbers of groups: {{ exam.total_groups }}</span
                >
              </div>
            </div>
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
