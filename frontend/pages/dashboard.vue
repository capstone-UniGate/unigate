<script setup lang="ts">
import { ref, onMounted, watch } from "vue";
import CourseSearchBox from "@/components/CourseSearchBox.vue";
import ExamDateDropdown from "@/components/ExamDateDropdown.vue";
import { useGroups } from "@/composables/useGroups";
import CourseCard from "@/components/CourseCard.vue";

const { getCourses } = useGroups();

const course = ref("");
const examDate = ref("");

const courses = ref<{ name: string; exams: { date: string; groupCount: number }[] }[]>([]);
const selectedCourseExamDates = ref<string[]>([]);


// Watcher to update exam dates and filtered courses when a course is selected
watch(course, (newCourseName) => {
  const matchedCourse = courses.value.find(
    (c) => c.name.toLowerCase() === newCourseName.toLowerCase()
  );
  if (!matchedCourse) {
    selectedCourseExamDates.value = [];
    examDate.value = "";
  } else {
    selectedCourseExamDates.value = matchedCourse.exams.map((exam) => exam.date);
    
  }
});


// Fetch courses from the API
const fetchCourses = async () => {
  try {
    const response = await getCourses();
    courses.value = response.map(
      (course: { name: string; exams: { date: string; groupCount: number }[] }) => ({
        name: course.name,
        exams: course.exams,
      })
    );

  } catch (error) {
    console.error("Error fetching courses:", error);
    courses.value = [];
  }
};

// Fetch courses when the component is mounted
onMounted(fetchCourses);
</script>

<template>
  <div class="p-4">
    <h1 class="text-2xl font-bold mb-4">Professor Dashboard</h1>

    <!-- Course SearchBox -->
    <div class="mb-6">
      <label for="course" class="block mb-2 text-sm font-medium text-gray-700">
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


    <div
      class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4"
    >
      <CourseCard v-for="course in courses" :key="course.id" :course="course" />
    </div>
  </div>
</template>
