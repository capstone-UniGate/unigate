<template>
  <div class="rounded-lg m-6 border bg-card text-card-foreground shadow-sm p-4">
    <!-- Course Name -->
    <h2
      id="course_name_card"
      class="text-lg font-semibold flex items-center justify-between border-b pb-2 mb-4"
    >
      {{ course }}
    </h2>

    <!-- Exam List -->
    <div
      v-if="course_data"
      class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3"
    >
      <div
        v-for="(exam, index) in course_data"
        :key="index"
        class="rounded-lg border bg-muted/50 p-3"
      >
        <h3 class="text-sm font-medium mb-2">Exam Date: {{ exam.exam_date }}</h3>
        <table class="w-full text-sm border-collapse">
          <tbody>
            <tr>
              <td class="font-medium pr-2">Avg members/group:</td>
              <td>{{ exam.average_members }}</td>
            </tr>
            <tr>
              <td class="font-medium pr-2">Min members:</td>
              <td>{{ exam.min_members }}</td>
            </tr>
            <tr>
              <td class="font-medium pr-2">Max members:</td>
              <td>{{ exam.max_members }}</td>
            </tr>
            <tr>
              <td class="font-medium pr-2">Total members:</td>
              <td>{{ exam.total_members }}</td>
            </tr>
            <tr>
              <td class="font-medium pr-2">Total groups:</td>
              <td>{{ exam.total_groups }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
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

<style scoped>
.text-primary {
  color: #1d4ed8;
}
.bg-muted\50 {
  background-color: rgba(229, 231, 235, 0.5);
}
.table {
  width: 100%;
  border-collapse: collapse;
}
td {
  padding: 0.25rem 0;
}
</style>