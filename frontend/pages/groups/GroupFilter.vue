<script setup lang="ts">
import { ref, computed, defineEmits, onMounted, watch } from 'vue';
import { useGroups } from '@/composables/useGroups';
import { Button } from '@/components/ui/button';
import { ChevronDown, ChevronUp, Filter, Trash, X } from 'lucide-vue-next';

const { getCourses } = useGroups();

const isFilterVisible = ref(false);
const course = ref('');
const examDate = ref('');
const participants = ref<number | null>(null);
const isPublic = ref<boolean | null>(null);
const orderBy = ref(null);

const emit = defineEmits(['apply-filters']);

const defaultFilters = {
  course: '',
  examDate: '',
  participants: null,
  isPublic: null,
  orderBy: null,
};

const appliedFilters = ref([]);
const allCourses = ref<{ name: string; exams: { date: string }[] }[]>([]);
const selectedCourseExamDates = ref<string[]>([]);

// Computed property to filter courses based on the input
const filteredCourses = computed(() => {
  if (!course.value) return [];
  return allCourses.value.filter((c) =>
    c.name.toLowerCase().includes(course.value.toLowerCase())
  );
});

// Computed property to check if no results are found
const noResultsFound = computed(() => {
  return course.value && filteredCourses.value.length === 0;
});

// Watcher to update exam dates when a course is selected
watch(course, (newCourseName) => {
  const matchedCourse = allCourses.value.find(
    (c) => c.name.toLowerCase() === newCourseName.toLowerCase()
  );
  if (!matchedCourse) {
    selectedCourseExamDates.value = [];
    examDate.value = '';
  } else {
    selectedCourseExamDates.value = matchedCourse.exams.map((exam) => exam.date);
  }
});

// Computed property to check if filters have changed
const areFiltersChanged = computed(() => {
  return (
    course.value !== defaultFilters.course ||
    examDate.value !== defaultFilters.examDate ||
    participants.value !== defaultFilters.participants ||
    isPublic.value !== defaultFilters.isPublic ||
    orderBy.value !== defaultFilters.orderBy
  );
});

// Fetch courses from the API
const fetchCourses = async () => {
  try {
    const response = await getCourses();
    allCourses.value = response.map((course: { name: string; exams: { date: string }[] }) => ({
      name: course.name,
      exams: course.exams,
    }));
  } catch (error) {
    console.error('Error fetching courses:', error);
    allCourses.value = [];
  }
};

// Toggle the visibility of the filter section
const toggleFilter = () => {
  isFilterVisible.value = !isFilterVisible.value;
};

// Apply the selected filters
const applyFilters = () => {
  if (areFiltersChanged.value) {
    emit('apply-filters', {
      course: course.value,
      examDate: examDate.value,
      participants: participants.value,
      isPublic: isPublic.value,
      orderBy: orderBy.value,
    });

    const filters = [];
    if (course.value) filters.push({ label: `Course: ${course.value}`, key: 'course' });
    if (examDate.value) filters.push({ label: `Exam Date: ${examDate.value}`, key: 'examDate' });
    if (participants.value !== null) filters.push({ label: `Participants: ${participants.value}`, key: 'participants' });
    if (isPublic.value !== null) filters.push({ label: `Type: ${isPublic.value ? 'Public' : 'Private'}`, key: 'isPublic' });
    if (orderBy.value) filters.push({ label: `Order By: ${orderBy.value}`, key: 'orderBy' });
    appliedFilters.value = filters;
  }
};

// Clear all filters
const clearFilters = () => {
  course.value = '';
  examDate.value = '';
  participants.value = null;
  isPublic.value = null;
  orderBy.value = null;

  appliedFilters.value = [];

  emit('apply-filters', defaultFilters);
};

// Remove a specific filter
const removeFilter = (key) => {
  if (key === 'course') {
    course.value = '';
    examDate.value = '';
  }
  if (key === 'examDate') examDate.value = '';
  if (key === 'participants') participants.value = null;
  if (key === 'isPublic') isPublic.value = null;
  if (key === 'orderBy') orderBy.value = null;

  appliedFilters.value = appliedFilters.value.filter((filter) => filter.key !== key && !(key === 'course' && filter.key === 'examDate'));

  emit('apply-filters', {
    course: course.value,
    examDate: examDate.value,
    participants: participants.value,
    isPublic: isPublic.value,
    orderBy: orderBy.value,
  });
};

// Select a course from the filtered list
const selectCourse = (selectedCourse: { name: string; exams: { date: string }[] }) => {
  course.value = selectedCourse.name;
  selectedCourseExamDates.value = selectedCourse.exams.map((exam) => exam.date);
  examDate.value = '';
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
          <button
            @click="removeFilter(filter.key)"
            class="ml-2 text-blue-800 hover:text-blue-500"
          >
            <X class="w-4 h-4" />
          </button>
        </span>
      </div>
    </div>

    <!-- Collapsible Filter Section -->
    <div
      v-show="isFilterVisible"
      class="overflow-hidden transition-all duration-500 rounded-lg bg-white shadow-lg border border-gray-200"
      :style="{ maxHeight: isFilterVisible ? '500px' : '0', padding: isFilterVisible ? '16px' : '0' }"
    >
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        <!-- Course Input -->
        <div>
          <label for="course" class="block mb-2 text-sm font-medium text-gray-700">Course</label>
          <input
            id="course"
            v-model="course"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring focus:ring-blue-200 focus:border-blue-500"
            placeholder="Enter course name"
          />
          <!-- Dropdown for filtered courses -->
          <ul
            v-if="filteredCourses.length && !selectedCourseExamDates.length"
            class="bg-white border border-gray-300 rounded-lg shadow-lg mt-2"
          >
            <li
              v-for="filteredCourse in filteredCourses"
              :key="filteredCourse.name"
              class="px-4 py-2 hover:bg-gray-100 cursor-pointer"
              @click="selectCourse(filteredCourse)"
            >
              {{ filteredCourse.name }}
            </li>
          </ul>
          <!-- No results found message -->
          <p v-if="noResultsFound" class="mt-2 text-red-500">No results found</p>
        </div>

        <!-- Exam Date Dropdown -->
        <div>
          <label for="examDate" class="block mb-2 text-sm font-medium text-gray-700">Exam Date</label>
          <select
            id="examDate"
            v-model="examDate"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring focus:ring-blue-200 focus:border-blue-500"
            :disabled="selectedCourseExamDates.length === 0"
          >
            <option value="" disabled>Select Exam Date</option>
            <option v-for="date in selectedCourseExamDates" :key="date" :value="date">
              {{ date }}
            </option>
          </select>
        </div>

        <!-- Number of Participants -->
        <div>
          <label for="participants" class="block mb-2 text-sm font-medium text-gray-700">Number of Participants</label>
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
          <label for="isPublic" class="block mb-2 text-sm font-medium text-gray-700">Type</label>
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
          <label for="orderBy" class="block mb-2 text-sm font-medium text-gray-700">Order By</label>
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
          :disabled="!areFiltersChanged"
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
  </div>
</template>