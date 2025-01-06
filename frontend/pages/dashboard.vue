<script setup lang="ts">
import { ref, onMounted, watch, computed } from "vue";
import CourseSearchBox from "@/components/CourseSearchBox.vue";
import ExamDateDropdown from "@/components/ExamDateDropdown.vue";
import CourseCard from "@/components/CourseCard.vue";
import LoadingIndicator from "@/components/LoadingIndicator.vue";
import { useGroups } from "@/composables/useGroups";

const { getProfessorsCourses, getGroupCount, getAverageMembers } = useGroups();

const course = ref("");
const examDate = ref("");
const isLoading = ref(true); // Track loading state
const courses = ref<
  { id: number; name: string; exams: { date: string; groupCount: number ; avgMembers: number}[] }[]
>([]);
const selectedCourseExamDates = ref<string[]>([]);
const groupCounts = ref<Record<string, number>>({});
const errorMessage = ref("");
const averageMembers = ref<Record<string, number>>({});
const activeGroupsCounts = ref<Record<string, number>>({});


// Watcher to update exam dates when a course is selected
watch(course, (newCourseName) => {
  const matchedCourse = courses.value.find(
    (c) => c.name.toLowerCase() === newCourseName.toLowerCase(),
  );
  if (!matchedCourse) {
    selectedCourseExamDates.value = [];
    examDate.value = "";
  } else {
    selectedCourseExamDates.value = matchedCourse.exams.map(
      (exam) => exam.date,
    );
  }
});

// Fetch group counts for each course
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

//Fetch group average members for each course
const fetchAverageMembers = async () => {
  for (const course of courses.value) {
    try {
      const response = await getAverageMembers(course.name);
      averageMembers.value[course.name] = (response as { avg: number }).avg;
    } catch (error) {
        console.error(`Error fetching average members for ${course.name}:`, error);
        averageMembers.value[course.name] = 0;
    }
  }
};

//Fetch group average members for each course
const fetchNumberOfActiveGroups = async () => {
  for (const course of courses.value) {
    try {
      const response = await getAverageMembers(course.name);
      averageMembers.value[course.name] = (response as { avg: number }).avg;
    } catch (error) {
        console.error(`Error fetching active group count for ${course.name}:`, error);
        averageMembers.value[course.name] = 0;
    }
  }
};

// Fetch professor's courses from the API
const fetchProfessorsCourses = async () => {
  try {
    const response = await getProfessorsCourses();
    courses.value = response.map((course: any, index: number) => ({
      id: index,
      name: course.name,
      exams: course.exams,
    }));
    await fetchGroupCounts();
    await fetchAverageMembers();
    await fetchNumberOfActiveGroups();
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

// Computed property to filter displayed courses
const filteredCourses = computed(() => {
  return courses.value.filter(
    (c) => c.name.toLowerCase() === course.value.toLowerCase(),
  );
});

onMounted(fetchProfessorsCourses);
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
          Professor Dashboard
        </h1>
        <div>
          <!-- Course SearchBox -->
          <div class="mb-6">
            <label for="course" class="block mb-2 text-sm font-medium"
              >Course</label
            >
            <CourseSearchBox
              id="course"
              :items="courses"
              placeholder="Enter course name"
              v-model="course"
              @select="
                (selectedCourse) => {
                  course = selectedCourse.name;
                  examDate = '';
                  selectedCourseExamDates = selectedCourse.exams.map(
                    (e) => e.date,
                  );
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
          <div
            v-if="filteredCourses.length"
            class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4"
          >
            <CourseCard
              v-for="course in filteredCourses"
              :key="course.id"
              :course="course"
              :groupCount="groupCounts[course.name] || 0"
              :avgMembers="averageMembers[course.name] || 0"
              :activeGroupCount="activeGroupsCounts[course.name] || 0"
            />
          </div>
          <div v-else class="text-center text-gray-500 mt-8">
            Select a course to view details
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
