<script setup lang="ts">
import { ref, computed, defineEmits, onMounted, watch } from "vue";
import { useGroups } from "@/composables/useGroups";
import { Button } from "@/components/ui/button";
import { ChevronDown, ChevronUp, Filter, Trash, X } from "lucide-vue-next";
import CourseSearchBox from "@/components/CourseSearchBox.vue";
import ExamDateDropdown from "@/components/ExamDateDropdown.vue";

const { getCourses, searchGroups, getAllGroups } = useGroups();

const isFilterVisible = ref(false);
const course = ref("");
const examDate = ref("");
const participants = ref<number | null>(null);
const isPublic = ref<boolean | null>(null);
const orderBy = ref(null);
const noResults = ref(false);

const emit = defineEmits(["apply-filters"]);

const defaultFilters = {
  course: "",
  examDate: "",
  participants: null,
  isPublic: null,
  orderBy: null,
};

const appliedFilters = ref([]);
const allCourses = ref<{ name: string; exams: { date: string }[] }[]>([]);
const selectedCourseExamDates = ref<string[]>([]);

// Watcher to update exam dates when a course is selected
watch(course, (newCourseName) => {
  const matchedCourse = allCourses.value.find(
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

// Computed property to check if filters have changed
const areFiltersChanged = computed(() => {
  return (
    course.value !== defaultFilters.course ||
    examDate.value !== defaultFilters.examDate ||
    participants.value !== defaultFilters.participants ||
    isPublic.value !== defaultFilters.isPublic ||
    orderBy.value !== defaultFilters.orderBy ||
    appliedFilters.value.length > 0
  );
});

// Computed property to enable/disable the Apply Filters button
const isApplyEnabled = computed(() => {
  return areFiltersChanged.value && course.value.trim().length > 0;
});

// Fetch courses from the API
const fetchCourses = async () => {
  try {
    const response = await getCourses();
    allCourses.value = response.map(
      (course: { name: string; exams: { date: string }[] }) => ({
        name: course.name,
        exams: course.exams,
      }),
    );
  } catch (error) {
    console.error("Error fetching courses:", error);
    allCourses.value = [];
  }
};

// Toggle the visibility of the filter section
const toggleFilter = () => {
  isFilterVisible.value = !isFilterVisible.value;
};

const applyFilters = async () => {
  try {
    if (areFiltersChanged.value) {
      const filters = {
        course: course.value || undefined,
        exam_date: examDate.value || undefined,
        participants: participants.value || undefined,
        is_public: isPublic.value !== null ? isPublic.value : undefined,
        order: orderBy.value || undefined,
      };

      // Update applied filters with user-friendly labels
      appliedFilters.value = Object.entries(filters)
        .filter(([key, value]) => value !== undefined)
        .map(([key, value]) => {
          let label = "";

          // Map key and value to user-friendly names
          switch (key) {
            case "course":
              label = `Course: ${value}`;
              break;
            case "exam_date":
              label = `Exam Date: ${value}`;
              break;
            case "participants":
              label = `Participants: ${value}`;
              break;
            case "is_public":
              label = `Type: ${value === true ? "Public" : "Private"}`;
              break;
            case "order":
              label = `Order By: ${value === "Newest" ? "Newest" : "Oldest"}`;
              break;
            default:
              label = `${key}: ${value}`;
          }

          return { key, label };
        });

      // Execute the search
      const results = await searchGroups(filters);

      if (results.length === 0) {
        noResults.value = true;
      } else {
        noResults.value = false;
      }
      emit("apply-filters", filters);
    }
  } catch (error) {
    console.error("Error applying filters:", error);
  }
};

// Clear all filters
const clearFilters = () => {
  course.value = "";
  examDate.value = "";
  participants.value = null;
  isPublic.value = null;
  orderBy.value = null;

  appliedFilters.value = [];
  noResults.value = false;
  getAllGroups();

  emit("apply-filters", defaultFilters);
};

// Fetch courses when the component is mounted
onMounted(fetchCourses);
</script>

<template>
  <div class="p-4">
    <!-- Filter Toggle Button and Active Filters -->
    <div class="flex flex-wrap items-center gap-4 mb-4">
      <!-- Filter Toggle Button -->
      <Button
        class="sm:w-auto flex items-center justify-between px-4 py-2 rounded-2xl shadow-lg bg-white text-gray-800 font-semibold hover:bg-gray-100 hover:shadow-xl active:scale-95 transition-all border border-gray-300"
        @click="toggleFilter"
      >
        <span class="flex items-center gap-2">
          <Filter class="w-5 h-5" /> Filter
        </span>
        <ChevronDown v-if="!isFilterVisible" class="w-5 h-5" />
        <ChevronUp v-else class="w-5 h-5" />
      </Button>

      <!-- Active Filters Tags -->
      <div class="flex flex-wrap gap-2">
        <span
          v-for="filter in appliedFilters"
          :key="filter.key"
          class="inline-flex items-center bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-medium"
        >
          {{ filter.label }}
        </span>
      </div>
    </div>

    <!-- Collapsible Filter Section -->
    <div
      v-show="isFilterVisible"
      class="overflow-hidden transition-all duration-500 rounded-lg bg-white shadow-lg border border-gray-200"
      :style="{
        maxHeight: isFilterVisible ? '500px' : '0',
        padding: isFilterVisible ? '16px' : '0',
      }"
    >
      <div
        class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4"
      >
        <!-- Course SearchBox -->
        <div>
          <label
            for="course"
            class="block mb-2 text-sm font-medium text-gray-700"
            >Course<span class="text-red-500 ml-1">*</span></label
          >
          <CourseSearchBox
            id="course"
            :items="allCourses"
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
        <div>
          <ExamDateDropdown
            :examDates="selectedCourseExamDates"
            v-model:selectedDate="examDate"
            :disabled="selectedCourseExamDates.length === 0"
          />
        </div>

        <!-- Number of Participants -->
        <div>
          <label
            for="participants"
            class="block mb-2 text-sm font-medium text-gray-700"
            >Number of Participants</label
          >
          <input
            id="participants"
            v-model.number="participants"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring focus:ring-blue-200 focus:border-blue-500"
            type="number"
            placeholder="e.g., 10"
            min="0"
          />
        </div>

        <!-- Type Dropdown -->
        <div>
          <label
            for="isPublic"
            class="block mb-2 text-sm font-medium text-gray-700"
            >Type</label
          >
          <select
            id="isPublic"
            v-model="isPublic"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring focus:ring-blue-200 focus:border-blue-500"
          >
            <option :value="null">All</option>
            <option :value="true">Public</option>
            <option :value="false">Private</option>
          </select>
        </div>

        <!-- Order By Dropdown -->
        <div>
          <label
            for="orderBy"
            class="block mb-2 text-sm font-medium text-gray-700"
            >Order By</label
          >
          <select
            id="orderBy"
            v-model="orderBy"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring focus:ring-blue-200 focus:border-blue-500"
          >
            <option :value="null">Default</option>
            <option value="Newest">Newest</option>
            <option value="Oldest">Oldest</option>
          </select>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="flex justify-end gap-4 mt-6">
        <!-- Apply Filters Button -->
        <Button
          :disabled="!isApplyEnabled"
          class="w-40 bg-gradient-to-r from-green-500 to-green-600 text-white font-semibold py-2 px-4 rounded-2xl shadow-lg hover:from-green-600 hover:to-green-700 hover:shadow-xl active:scale-95 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
          @click="applyFilters"
        >
          <Filter class="w-4 h-4 mr-2" /> Apply Filters
        </Button>

        <!-- Clear Filters Button -->
        <Button
          :disabled="!areFiltersChanged"
          class="w-40 bg-gradient-to-r from-yellow-400 to-yellow-500 text-white font-semibold py-2 px-4 rounded-2xl shadow-lg hover:from-yellow-500 hover:to-yellow-600 hover:shadow-xl active:scale-95 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
          @click="clearFilters"
        >
          <Trash class="w-4 h-4 mr-2" /> Clear Filters
        </Button>
      </div>
    </div>
    <!-- No Results Message -->
    <div v-if="noResults" class="mt-4 p-4 bg-red-100 text-red-700 rounded-lg">
      No groups found matching your criteria. Please try adjusting the filters.
    </div>
  </div>
</template>
