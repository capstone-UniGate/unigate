<template>
  <div class="dashboard mx-auto p-4 max-w-4xl">
    <h1 class="text-2xl font-bold mb-4">Professor Dashboard</h1>

    <!-- Autocomplete -->
    <div class="mb-6">
      <Autocomplete
        v-model="searchTerm"
        :options="courses"
        placeholder="Search for a course/exam"
        @select="onCourseSelect"
      />
    </div>

    <!-- Course List -->
    <ul class="grid gap-4 md:grid-cols-2">
      <li
        v-for="course in filteredCourses"
        :key="course.id"
        class="p-4 border rounded-md bg-gray-50 shadow-sm hover:shadow-md transition"
      >
        <div class="font-medium text-lg">{{ course.name }}</div>
        <div class="text-gray-600">Groups: {{ course.groupCount }}</div>
      </li>
    </ul>
  </div>
</template>

<script lang="ts">
import { ref, computed } from "vue";
import Autocomplete, { Option } from "@/components/Autocomplete.vue";
import useCourses from "@/composables/useCourses";

export default {
  components: {
    Autocomplete,
  },
  setup() {
    const { courses, filterCourses, isEligible } = useCourses();
    const role = ref("professor"); // Mocked role constant
    const searchTerm = ref("");

    if (role.value !== "professor") {
      console.error("Access Denied: User is not a professor.");
    }

    const filteredCourses = computed(() => filterCourses(searchTerm.value));

    const onCourseSelect = (selectedCourse: Option) => {
      console.log("Selected Course:", selectedCourse);
    };

    return {
      searchTerm,
      courses,
      filteredCourses,
      onCourseSelect,
      isEligible,
    };
  },
};
</script>
