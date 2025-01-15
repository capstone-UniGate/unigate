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
  getYearlyStats,
  getTotalMembers,
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
const studentNames = ref<string[]>([]);
const yearlyStats = ref<{ [key: number]: number }>({});
const totalMembers = ref<number | null>(null);

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

const fetchYearlyStats = async () => {
  if (!course.value) {
    console.error("Course value is empty, skipping fetchYearlyStats.");
    return;
  }
  try {
    console.log(`Fetching yearly stats for course: ${course.value}`);
    const response = await getYearlyStats(course.value);
    console.log("Yearly stats response:", response);
    yearlyStats.value = response as { [key: number]: number };
  } catch (error) {
    console.error("Error fetching yearly stats:", error);
  }
};

const fetchTotalMembers = async () => {
  if (!course.value) return;
  try {
    const response = await getTotalMembers(course.value);
    totalMembers.value = response;
    console.log("Total Members:", totalMembers.value);
  } catch (error) {
    console.error("Error fetching total members:", error);
  }
};

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
  console.log("Starting fetchNumberOfActiveGroups");
  for (const course of courses.value) {
    if (!activeGroupsCounts.value[course.name]) {
      activeGroupsCounts.value[course.name] = {};
    }

    for (const exam of course.exams) {
      try {
        const response = await getActiveGroupCount(course.name, exam.date);
        console.log("Response for", course.name, exam.date, ":", response);

        // Store student names when it matches the current selection
        if (course.name === course.value && exam.date === examDate.value) {
          studentNames.value = response.student_names;
        }

        // Count groups that have more than one student
        const activeGroupCount = response.groups.filter(
          (group: { students: string[] }) => group.students.length > 1,
        ).length;

        activeGroupsCounts.value[course.name][exam.date] = activeGroupCount;

        console.log(
          `Active groups for ${course.name} on ${exam.date}: ${activeGroupCount}`,
          `(Total groups with >1 student: ${activeGroupCount} out of ${response.groups.length} total groups)`,
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
  console.log("Final activeGroupsCounts:", activeGroupsCounts.value);
};

// Add watcher to update student names when course or exam date changes
watch([course, examDate], async ([newCourse, newExamDate]) => {
  if (newCourse && newExamDate) {
    try {
      const response = await getActiveGroupCount(newCourse, newExamDate);
      studentNames.value = response.student_names;
    } catch (error) {
      console.error("Error fetching student names:", error);
      studentNames.value = [];
    }
  } else {
    studentNames.value = [];
  }
});

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
                    await fetchYearlyStats();
                    await fetchTotalMembers();
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

        <!-- Add Student Names Section before Group Creation Chart -->
        <div
          v-if="filteredCourses.length && studentNames.length > 0"
          class="mt-8 mb-8"
        >
          <h2 class="text-2xl font-bold mb-4">Enrolled Students</h2>
          <div class="bg-gray-50 p-4 rounded-lg">
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
              <div
                v-for="(student, index) in studentNames"
                :key="index"
                class="bg-white p-3 rounded shadow-sm"
              >
                {{ student }}
              </div>
            </div>
            <div class="mt-4 text-gray-600 text-sm">
              Total Students: {{ studentNames.length }}
            </div>
          </div>
        </div>

        <!-- Group Creation Chart -->
        <div
          v-if="filteredCourses.length && groupCreationData.length > 0"
          class="mt-8"
        >
          <h2 class="text-2xl font-bold mb-6">Group Creation Over Time</h2>
          <GroupCreationChart :data="groupCreationData" />
        </div>

        <!-- Yearly Group Enrollment and Participation -->
        <div
          id="yearly_group_creation_chart"
          v-if="filteredCourses.length && Object.keys(yearlyStats).length > 0"
          class="mt-8"
        >
          <h2 class="text-2xl font-bold mb-6">
            Yearly Group Enrollment and Participation
          </h2>
          <table
            class="table-auto w-full text-left border-collapse border border-gray-200"
          >
            <thead>
              <tr>
                <th class="border border-gray-300 px-4 py-2">Year</th>
                <th class="border border-gray-300 px-4 py-2">Total Groups</th>
                <th class="border border-gray-300 px-4 py-2">Total Members</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="[year, totalGroups] in Object.entries(yearlyStats)"
                :key="year"
              >
                <td class="border border-gray-300 px-4 py-2">{{ year }}</td>
                <td class="border border-gray-300 px-4 py-2">
                  {{ totalGroups }}
                </td>
                <td class="border border-gray-300 px-4 py-2">
                  {{ totalMembers }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>
