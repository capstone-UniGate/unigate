<script setup lang="ts">
import { ref, onMounted, watch, computed } from "vue";
import CourseSearchBox from "@/components/CourseSearchBox.vue";
import ExamDateDropdown from "@/components/ExamDateDropdown.vue";
import CourseTable from "@/components/CourseTable.vue";
import LoadingIndicator from "@/components/LoadingIndicator.vue";
import { useCourses } from "@/composables/useCourses";

const { getAllStats } = useCourses();

const courses = ref();
const isLoading = ref(true); // Track loading state
const courses_stats = ref();
const groupCounts = ref<Record<string, number>>({});
const errorMessage = ref("");

// Fetch professor's courses from the API
const getStats = async () => {
  try {
    courses_stats.value = await getAllStats();
    courses.value = Object.keys(courses_stats.value);
  } catch (error: any) {
    console.error("Error fetching courses:", error);
    if (error.response?.status === 403) {
      errorMessage.value =
        "Access to this page is blocked. You must be authenticated.";
    } else {
      errorMessage.value = "Error fetching courses. Please try again later.";
    }
  } finally {
    isLoading.value = false; // Stop loading after data is fetched or an error occurs
  }
};

onMounted(getStats);
</script>

<template>
  <div>
    <!-- Show loading indicator while loading -->
    <LoadingIndicator v-if="isLoading" />

    <!-- Error message if access is blocked -->
    <div v-else-if="errorMessage" class="text-center">
      <img
        src="/static/images/access-denied.png"
        alt="Access Denied"
        class="w-64 mx-auto mb-4"
      />
      <p class="text-xl text-red-500">{{ errorMessage }}</p>
    </div>

    <!-- Main dashboard content -->
    <div
      v-else
      class="flex justify-center items-center min-h-[80vh] bg-gray-100 py-6"
    >
      <div
        class="container mx-auto max-w-5xl h-[90vh] bg-white shadow-lg rounded-lg p-8 overflow-y-auto"
      >
        <h1 class="text-3xl font-semibold mb-6 text-center">
          Courses Comparison
        </h1>
        <!-- Course Cards Grid -->
        <div
          v-if="courses.length"
          class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4"
        >
          <CourseTable
            v-for="course in courses"
            :key="courses_stats[course].id"
            :course="course"
            :course_data="courses_stats[course]"
          />
        </div>
      </div>
    </div>
  </div>
</template>
