<script setup lang="ts">
import { ref, onMounted, watch, computed } from "vue";
import CourseSearchBox from "@/components/CourseSearchBox.vue";
import ExamDateDropdown from "@/components/ExamDateDropdown.vue";
import CourseCard from "@/components/CourseCard.vue";
import { useGroups } from "@/composables/useGroups";

const { getCourses, getGroupCount } = useGroups();

const course = ref("");
const examDate = ref("");

const courses = ref<
  { id: number; name: string; exams: { date: string; groupCount: number }[] }[]
>([]);
const selectedCourseExamDates = ref<string[]>([]);
const groupCounts = ref<Record<string, number>>({}); // To store group counts for each course

// Watcher to update exam dates when a course is selected
watch(course, (newCourseName) => {
  const matchedCourse = courses.value.find(
    (c) => c.name.toLowerCase() === newCourseName.toLowerCase(),
  );
  if (!matchedCourse) {
    selectedCourseExamDates.value = [];
    examDate.value = "";
  } else {
    selectedCourseExamDates.value = matchedCourse.exams.map((exam) => exam.date);
  }
});

// Function to calculate total group count for each course
const fetchGroupCounts = async () => {
  for (const course of courses.value) {
    try {
      const response = await getGroupCount(course.name);
      groupCounts.value[course.name] = response.count;
    } catch (error) {
      console.error(`Error fetching group count for ${course.name}:`, error);
      groupCounts.value[course.name] = 0;
    }
  }
};

// Fetch courses from the API
const fetchCourses = async () => {
  try {
    const response = await getCourses();
    courses.value = response.map((course: any, index: number) => ({
      id: index,
      name: course.name,
      exams: course.exams,
    }));
    await fetchGroupCounts(); // Fetch group counts after fetching courses
  } catch (error) {
    console.error("Error fetching courses:", error);
    courses.value = [];
  }
};

// Computed property to filter displayed courses
const filteredCourses = computed(() => {
  // if (!course.value) return courses.value; // Show all courses if no course is selected
  return courses.value.filter((c) => c.name.toLowerCase() === course.value.toLowerCase());
});

onMounted(fetchCourses);
</script>

<template>
  <div class="flex justify-center items-center min-h-[80vh] bg-gray-100 py-6">
    <div class="container mx-auto max-w-5xl h-[90vh] bg-white shadow-lg rounded-lg p-8 overflow-y-auto">
      <h1 class="text-3xl font-semibold mb-6 text-center">
        Professor Dashboard
      </h1>

      <!-- Course SearchBox -->
      <div class="mb-6">
        <label for="course" class="block mb-2 text-sm font-medium">
          Course
        </label>
        <CourseSearchBox
          id="course"
          :items="courses"
          placeholder="Enter course name"
          v-model="course"
          @select="
            (selectedCourse) => {
              course = selectedCourse.name;
              examDate = '';
              selectedCourseExamDates = selectedCourse.exams.map((e) => e.date);
            }
          "
        />
      </div>

      <!-- Exam Date Dropdown -->
      <div class="mb-6">
        <ExamDateDropdown
          :examDates="selectedCourseExamDates"
          v-model:selectedDate="examDate"
          :disabled="selectedCourseExamDates.length === 0"
        />
      </div>

      <!-- Course Cards Grid -->
      <div v-if="filteredCourses.length" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        <CourseCard
          v-for="course in filteredCourses"
          :key="course.id"
          :course="course"
          :groupCount="groupCounts[course.name] || 0"
        />
      </div>
      <div v-else class="text-center text-gray-500 mt-8">
        Select a course to view details
      </div>
    </div>
  </div>
</template>
