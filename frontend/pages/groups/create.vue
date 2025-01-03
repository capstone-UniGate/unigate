<template>
  <Toaster />
  <div
    class="container mx-auto my-8 max-w-3xl p-6 bg-white shadow-md rounded-lg"
  >
    <form class="space-y-6" @submit.prevent="onSubmit">
      <!-- Name Field -->
      <FormField v-slot="{ componentField }" name="name">
        <FormItem>
          <FormLabel> Name<span class="text-red-500 ml-1">*</span> </FormLabel>
          <FormControl>
            <input
              type="text"
              placeholder="Enter Group Name"
              v-bind="componentField"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring focus:ring-blue-200 focus:border-blue-500"
            />
          </FormControl>
          <FormMessage />
        </FormItem>
      </FormField>

      <!-- Course SearchBox -->
      <FormField v-slot="{ componentField }" name="course">
        <FormItem>
          <FormLabel>
            Course<span class="text-red-500 ml-1">*</span>
          </FormLabel>
          <FormControl>
            <div class="relative">
              <input
                type="text"
                placeholder="Enter Course Name"
                v-bind="componentField"
                @input="(e) => handleCourseInput(e, componentField)"
                @focus="showCourseDropdown = true"
                @blur="handleCourseBlur"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring focus:ring-blue-200 focus:border-blue-500"
              />
              <!-- Dropdown for filtered items -->
              <ul
                v-if="showCourseDropdown && filteredCourses.length"
                class="absolute w-full bg-white border border-gray-300 rounded-lg shadow-lg mt-2 z-10"
              >
                <li
                  v-for="course in filteredCourses"
                  :key="course.name"
                  class="px-4 py-2 hover:bg-gray-100 cursor-pointer"
                  @click="selectCourse(course, componentField)"
                >
                  {{ course.name }}
                </li>
              </ul>
            </div>
          </FormControl>
          <FormMessage />
        </FormItem>
      </FormField>

      <!-- Exam Date Dropdown -->
      <div>
        <ExamDateDropdown
          :examDates="selectedCourseExamDates"
          v-model:selectedDate="examDate"
          :disabled="selectedCourseExamDates.length === 0"
        />
      </div>

      <!-- Privacy Type -->
      <div>
        <FormField v-slot="{ componentField, errorMessage }" name="isPublic">
          <FormItem>
            <FormLabel>
              Privacy<span class="text-red-500 ml-1">*</span>
            </FormLabel>
            <div class="flex items-center space-x-6">
              <label class="flex items-center space-x-2">
                <input
                  type="radio"
                  value="Public"
                  v-bind="componentField"
                  class="form-radio h-4 w-4 text-blue-600 focus:ring focus:ring-blue-500"
                />
                <span>Public</span>
              </label>
              <label class="flex items-center space-x-2">
                <input
                  type="radio"
                  value="Private"
                  v-bind="componentField"
                  class="form-radio h-4 w-4 text-blue-600 focus:ring focus:ring-blue-500"
                />
                <span>Private</span>
              </label>
            </div>
            <FormMessage v-if="errorMessage">{{ errorMessage }}</FormMessage>
          </FormItem>
        </FormField>
      </div>

      <!-- Description Field -->
      <FormField v-slot="{ componentField }" name="description">
        <FormItem>
          <FormLabel>
            Description<span class="text-red-500 ml-1">*</span>
          </FormLabel>
          <FormControl>
            <textarea
              v-bind="componentField"
              placeholder="Describe your group"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring focus:ring-blue-200 focus:border-blue-500"
              style="min-height: 100px"
            ></textarea>
          </FormControl>
          <FormMessage />
        </FormItem>
      </FormField>

      <!-- Tags Field -->
      <FormField v-slot="{ componentField }" name="tags">
        <FormItem>
          <FormLabel> Tags<span class="text-red-500 ml-1">*</span> </FormLabel>
          <FormControl>
            <div class="space-y-2">
              <div class="flex flex-wrap gap-2">
                <span
                  v-for="(tag, index) in tags"
                  :key="index"
                  class="inline-flex items-center bg-blue-100 text-blue-800 text-sm font-medium px-3 py-1 rounded-full"
                >
                  {{ tag }}
                  <button
                    type="button"
                    @click="removeTag(index)"
                    class="ml-2 text-blue-600 hover:text-blue-500"
                  >
                    ×
                  </button>
                </span>
              </div>
              <div class="flex items-center space-x-2">
                <input
                  type="text"
                  v-model="tagInput"
                  @keydown.enter.prevent="addTag"
                  @keydown.delete="removeLastTag"
                  @input="filterSuggestions"
                  placeholder="Add tags..."
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring focus:ring-blue-200 focus:border-blue-500"
                />
                <button
                  type="button"
                  @click="addTag"
                  class="px-4 py-2 bg-green-500 text-white rounded-md hover:bg-green-600 focus:ring focus:ring-green-500"
                >
                  +
                </button>
              </div>
              <p class="text-sm text-gray-500">
                Press Enter or click "+" to add tags
              </p>
              <ul
                v-if="filteredSuggestions.length"
                class="bsolute w-full bg-white border border-gray-300 rounded-lg shadow-lg mt-2 z-10 scrollbar overflow-y-auto max-h-40"
              >
                <li
                  v-for="(suggestion, index) in filteredSuggestions"
                  :key="index"
                  @click="selectSuggestion(suggestion)"
                  class="px-4 py-2 hover:bg-gray-100 cursor-pointer"
                >
                  {{ suggestion }}
                </li>
              </ul>
            </div>
          </FormControl>
          <FormMessage />
        </FormItem>
      </FormField>

      <!-- Buttons -->
      <div class="flex justify-start space-x-4">
        <button
          type="submit"
          :disabled="formHasErrors || isLoading"
          class="w-40 bg-gradient-to-r from-green-500 to-green-600 text-white font-semibold py-2 px-4 rounded-md shadow-lg hover:from-green-600 hover:to-green-700 hover:shadow-xl active:scale-95 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {{ isLoading ? "Creating..." : "Create" }}
        </button>
        <button
          type="button"
          @click="onCancel"
          class="w-40 bg-gradient-to-r from-red-500 to-red-600 text-white font-semibold py-2 px-4 rounded-md shadow-lg hover:from-red-600 hover:to-red-700 hover:shadow-xl active:scale-95 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Cancel
        </button>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from "vue";
import { useRouter } from "vue-router";
import { toTypedSchema } from "@vee-validate/zod";
import { useForm } from "vee-validate";
import * as z from "zod";
import { useToast } from "@/components/ui/toast/use-toast";
import { useGroups } from "@/composables/useGroups";

const { toast } = useToast();
const router = useRouter();
const { createGroup, isLoading, getCourses } = useGroups();

const formSchema = toTypedSchema(
  z.object({
    name: z.string().min(2, "Name must be at least 2 characters long").max(50),
    course: z.string().nonempty("Please enter a valid course name"),
    isPublic: z.enum(["Public", "Private"]),
    description: z.string().min(10, "The description is too short").max(300),
    tags: z.array(z.string()).min(1, "Please add at least one tag"),
  }),
);

const course = ref("");
const showCourseDropdown = ref(false);
let isDropdownItemClicked = false;
const selectedCourseExamDates = ref<string[]>([]);
const allCourses = ref<{ name: string; exams: { date: string }[] }[]>([]);
const filteredCourses = computed(() =>
  course.value
    ? allCourses.value.filter((c) =>
        c.name.toLowerCase().includes(course.value.toLowerCase()),
      )
    : [],
);
const noCourseResultsFound = computed(
  () => course.value && filteredCourses.value.length === 0,
);

const examDate = ref("");
const tags = ref<string[]>([]);
const tagInput = ref("");
const filteredSuggestions = ref<string[]>([]);
const errorMessage = ref("");

const allSuggestions = [
  "JavaScript",
  "Vue.js",
  "React",
  "Angular",
  "Svelte",
  "Next.js",
  "Nuxt.js",
  "TypeScript",
  "Webpack",
  "Rollup",
];

const { handleSubmit, errors, setFieldValue } = useForm({
  validationSchema: formSchema,
});

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

const updateCourseValue = () => {
  showCourseDropdown.value = true;
};

watch(course, (newCourseName) => {
  const matchedCourse = allCourses.value.find(
    (c) => c.name.toLowerCase() === newCourseName.toLowerCase(),
  );

  if (!matchedCourse) {
    // If no matching course is found, reset exam dates
    selectedCourseExamDates.value = [];
    examDate.value = "";
  } else {
    // Update exam dates based on the selected course
    selectedCourseExamDates.value = matchedCourse.exams.map((e) => e.date);
    if (!selectedCourseExamDates.value.includes(examDate.value)) {
      examDate.value = ""; // Reset if current exam date is not valid
    }
  }
});

const handleCourseInput = (event: Event, componentField: any) => {
  const inputValue = (event.target as HTMLInputElement).value;
  componentField.value = inputValue; // Update vee-validate's internal value
  course.value = inputValue; // Update local state
  showCourseDropdown.value = true; // Show dropdown
  examDate.value = ""; // Reset exam date on input change
};

const selectCourse = (selectedCourse, componentField) => {
  isDropdownItemClicked = true; // Set flag to prevent blur handling
  componentField.value = selectedCourse.name;
  course.value = selectedCourse.name;
  selectedCourseExamDates.value = selectedCourse.exams.map((e) => e.date);
  showCourseDropdown.value = false;
};

const handleCourseBlur = () => {
  setTimeout(() => {
    if (!isDropdownItemClicked) {
      // Validate the course name only if no dropdown item was clicked
      const matchedCourse = allCourses.value.find(
        (c) => c.name.toLowerCase() === course.value.toLowerCase(),
      );

      if (course.value.length > 0 && !matchedCourse) {
        errorMessage.value = "Please enter a valid course name";
        course.value = "";
        setFieldValue("course", course.value);
      } else {
        errorMessage.value = "";
      }

      showCourseDropdown.value = false; // Hide dropdown
    }
    isDropdownItemClicked = false; // Reset flag
  }, 200);
};

const addTag = () => {
  const newTag = tagInput.value.trim();
  if (newTag && !tags.value.includes(newTag)) {
    tags.value.push(newTag);
    setFieldValue("tags", tags.value);
  }
  tagInput.value = "";
  filteredSuggestions.value = [];
};

const removeTag = (index: number) => {
  tags.value.splice(index, 1);
  setFieldValue("tags", tags.value);
};

const removeLastTag = (event: KeyboardEvent) => {
  if (
    tagInput.value === "" &&
    tags.value.length &&
    (event.key === "Backspace" || event.key === "Delete")
  ) {
    tags.value.pop();
    setFieldValue("tags", tags.value);
  }
};

const filterSuggestions = () => {
  const query = tagInput.value.toLowerCase();
  filteredSuggestions.value = allSuggestions.filter(
    (suggestion) =>
      suggestion.toLowerCase().includes(query) &&
      !tags.value.includes(suggestion),
  );
};

const selectSuggestion = (suggestion: string) => {
  if (!tags.value.includes(suggestion)) {
    tags.value.push(suggestion);
    setFieldValue("tags", tags.value);
  }
  tagInput.value = "";
  filteredSuggestions.value = [];
};

const formHasErrors = computed(() => Object.keys(errors.value).length > 0);

const onSubmit = handleSubmit(async (values) => {
  try {
    const payload = {
      name: values.name,
      description: values.description,
      course_name: course.value,
      category: course.value,
      exam_date: examDate.value || null,
      type: values.isPublic,
      tags: tags.value,
    };

    console.log("Payload for submission:", payload);

    await createGroup(payload);

    toast({
      variant: "success",
      description: "Group created successfully!",
    });

    setTimeout(() => {
      router.push({ name: "groups" });
    }, 1500);
  } catch (error) {
    console.error("Error creating group:", error);

    toast({
      variant: "destructive",
      description: "Failed to create group. Please try again.",
    });
  }
});

const onCancel = () => {
  router.push({ name: "groups" });
};

// Fetch courses when the component is mounted
onMounted(fetchCourses);
</script>
