<script setup lang="ts">
import { ref, onMounted, watch, computed } from "vue";
import CourseSearchBox from "@/components/CourseSearchBox.vue";
import ExamDateDropdown from "@/components/ExamDateDropdown.vue";
import CourseCard from "@/components/CourseCard.vue";
import LoadingIndicator from "@/components/LoadingIndicator.vue";
import { useGroups } from "@/composables/useGroups";
import GroupCreationChart from "@/components/GroupCreationChart.vue";

const {
  getProfessorsCourses,
  getGroupCount,
  getAverageMembers,
  getActiveGroupCount,
  getGroupCreationDistribution,
} = useGroups();

const course = ref("");
const examDate = ref("");
const isLoading = ref(true); // Track loading state
const courses = ref<
  {
    id: number;
    name: string;
    exams: {
      date: string;
      groupCount: number;
      avgMembers: number;
      activeGroupCount: number;
    }[];
  }[]
>([]);
const selectedCourseExamDates = ref<string[]>([]);
const groupCounts = ref<Record<string, number>>({});
const errorMessage = ref("");
const averageMembers = ref<Record<string, number>>({});
const activeGroupsCounts = ref<Record<string, Record<string, number>>>({});
const groupCreationData = ref<{ date: string; count: number }[]>([]);
const isLoadingChart = ref(true);

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
      console.error(
        `Error fetching average members for ${course.name}:`,
        error,
      );
      averageMembers.value[course.name] = 0;
    }
  }
};

//Fetch number of active groups for each course
const fetchNumberOfActiveGroups = async () => {
  for (const course of courses.value) {
    if (!activeGroupsCounts.value[course.name]) {
      activeGroupsCounts.value[course.name] = {};
    }

    for (const exam of course.exams) {
      try {
        const response = await getActiveGroupCount(course.name, exam.date);
        // Count groups with more than 1 student as active
        const activeCount = response.groups_info.filter(
          (group: { super_students: string[] }) =>
            group.super_students.length > 1,
        ).length;

        activeGroupsCounts.value[course.name][exam.date] = activeCount;

        console.log(
          `Active groups for ${course.name} on ${exam.date}: ${activeCount}`,
          `(Total groups: ${response.total_groups})`,
        );
      } catch (error) {
        console.error(
          `Error fetching active group count for ${course.name} on ${exam.date}:`,
          error,
        );
        activeGroupsCounts.value[course.name][exam.date] = 0;
      }
    }
  }
};

// Process group creation data
const processGroupCreationData = (groupsInfo: any[]) => {
  const creationCounts: Record<string, number> = {};

  groupsInfo.forEach((group) => {
    const creationDate = group.creation_date.split("T")[0]; // Extract YYYY-MM-DD
    if (!creationCounts[creationDate]) {
      creationCounts[creationDate] = 0;
    }
    creationCounts[creationDate]++;
  });

  // Convert to chart-friendly format
  return Object.entries(creationCounts).map(([creation_date, count]) => ({
    creation_date,
    count,
  }));
};

const fetchGroupCreationData = async (courseName: string) => {
  try {
    const response = await getGroupCreationDistribution(courseName);
    groupCreationData.value = processGroupCreationData(response.groups_info);
    console.log("Processed Group Creation Data:", groupCreationData.value);
  } catch (error) {
    console.error("Error fetching group creation data:", error);
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
    //await fetchGroupCreationData();
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

// Add a new computed property to get active group count for current selection
const currentActiveGroupCount = computed(() => {
  if (!course.value || !examDate.value) return 0;
  return activeGroupsCounts.value[course.value]?.[examDate.value] || 0;
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
              async (selectedCourse) => {
                course = selectedCourse.name;
                examDate = '';
                selectedCourseExamDates = selectedCourse.exams.map(
                  (e) => e.date,
                );

                // Fetch group creation data for the selected course
                if (course) {
                  //isLoading.value = true;
                  try {
                    console.log(
                      'Fetching group creation data for course:',
                      course,
                    );
                    await fetchGroupCreationData(course);
                  } catch (error) {
                    console.error(
                      'Error fetching group creation data for course:',
                      course,
                      error,
                    );
                  } finally {
                    // isLoading.value = false;
                  }
                }
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
            :activeGroupCount="currentActiveGroupCount"
          />
        </div>
        <div v-else class="text-center text-gray-500 mt-8">
          Select a course to view details
        </div>

        <!-- Group Creation Chart -->
        <div
          v-if="filteredCourses.length && groupCreationData.length > 0"
          class="mt-8"
        >
          <h2 class="text-2xl font-bold mb-6">Group Creation Over Time</h2>
          <GroupCreationChart :data="groupCreationData" />
        </div>
      </div>
    </div>
  </div>
</template>
