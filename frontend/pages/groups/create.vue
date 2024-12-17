<template>
  <Toaster />
  <div class="w-2/3 mx-auto margin-top-custom">
    <form class="space-y-6" @submit.prevent="onSubmit">
      <!-- Name Field -->
      <FormField v-slot="{ componentField }" name="name">
        <FormItem>
          <FormLabel>Name</FormLabel>
          <FormControl>
            <Input
              type="text"
              placeholder="Group Name"
              v-bind="componentField"
              id="group-name-input"
            />
          </FormControl>
          <FormMessage />
        </FormItem>
      </FormField>

      <!-- Course Field -->
      <FormField v-slot="{ componentField }" name="course">
        <FormItem>
          <FormLabel>Course</FormLabel>
          <FormControl>
            <select
              v-bind="componentField"
              class="form-select"
              id="course-select"
            >
              <option value="">Select from student's courses</option>
              <option value="course1">Course 1</option>
              <option value="course2">Course 2</option>
              <!-- Add other courses as needed -->
            </select>
          </FormControl>
          <FormMessage />
        </FormItem>
      </FormField>

      <!-- Privacy Type (Public or Private) -->
      <div>
        <FormField v-slot="{ componentField, errorMessage }" name="isPublic">
          <FormItem>
            <div class="flex items-center space-x-4">
              <label class="inline-flex items-center">
                <input
                  type="radio"
                  value="Public"
                  v-bind="componentField"
                  id="privacy-public"
                />
                <span class="ml-2">Public</span>
              </label>
              <label class="inline-flex items-center">
                <input
                  type="radio"
                  value="Private"
                  v-bind="componentField"
                  id="privacy-private"
                />
                <span class="ml-2">Private</span>
              </label>
            </div>
            <!-- Display "Required" message only if there's an error -->
            <FormMessage v-if="errorMessage">{{ errorMessage }}</FormMessage>
          </FormItem>
        </FormField>
      </div>

      <!-- Description Field -->
      <FormField v-slot="{ componentField }" name="description">
        <FormItem>
          <FormLabel>Description</FormLabel>
          <FormControl>
            <textarea
              v-bind="componentField"
              placeholder="Describe your group"
              class="form-textarea"
              id="group-description"
            ></textarea>
          </FormControl>
          <FormMessage />
        </FormItem>
      </FormField>

      <!-- Updated Tags Field -->
      <FormField v-slot="{ componentField }" name="tags">
        <FormItem>
          <FormLabel>Tags</FormLabel>
          <FormControl>
            <div class="tags-input-container">
              <div class="tags">
                <span v-for="(tag, index) in tags" :key="index" class="tag">
                  {{ tag }}
                  <button
                    type="button"
                    @click="removeTag(index)"
                    class="remove-tag-button"
                  >
                    &times;
                  </button>
                </span>
              </div>
              <input
                type="text"
                v-model="tagInput"
                @keydown.enter.prevent="addTag"
                @keydown.delete="removeLastTag"
                @input="filterSuggestions"
                placeholder="Add tags..."
                class="tags-input"
                id="tags-input"
              />
              <ul v-if="filteredSuggestions.length" class="suggestions-list">
                <li
                  v-for="(suggestion, index) in filteredSuggestions"
                  :key="index"
                  @click="selectSuggestion(suggestion)"
                  class="suggestion-item"
                >
                  {{ suggestion }}
                </li>
              </ul>
            </div>
          </FormControl>
          <FormMessage />
        </FormItem>
      </FormField>

      <!-- Error Message Placeholder -->
      <div v-if="errorMessage" class="text-red-600">{{ errorMessage }}</div>

      <!-- Buttons -->
      <div class="flex justify-start space-x-4 margin-bottom-custom">
        <Button
          type="submit"
          :disabled="formHasErrors || isLoading"
          id="create-group-button"
        >
          {{ isLoading ? "Creating..." : "Create" }}
        </Button>
        <Button
          type="button"
          @click="onCancel"
          variant="destructive"
          id="cancel-button"
          :disabled="isLoading"
        >
          Cancel
        </Button>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { Button } from "@/components/ui/button";
import {
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Toaster } from "@/components/ui/toast";
import { useToast } from "@/components/ui/toast/use-toast";
import { computed, ref, watch } from "vue";
import { useRouter } from "vue-router";
import { toTypedSchema } from "@vee-validate/zod";
import { useForm } from "vee-validate";
import {} from "@/composables/useGroups";
import * as z from "zod";

const { toast } = useToast();
const router = useRouter();
const { createGroup, isLoading, isError } = useGroups();
const { currentStudent } = useCurrentStudent();

const formSchema = toTypedSchema(
  z.object({
    name: z.string().min(2, "Name must be at least 2 characters long").max(50),
    course: z.string().nonempty("Course is required"),
    isPublic: z.enum(["Public", "Private"]),
    description: z.string().min(10, "The description is too short").max(300),
    tags: z.array(z.string()).min(1, "Please add at least one tag"),
  }),
);

const { handleSubmit, errors, setFieldValue } = useForm({
  validationSchema: formSchema,
});

const errorMessage = ref("");
const tags = ref<string[]>([]);
const tagInput = ref("");
const filteredSuggestions = ref<string[]>([]);

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

// Handle form submission
const onSubmit = handleSubmit(async (values) => {
  try {
    await ensureAuthenticated();
    let result = await createGroup({
      name: values.name,
      description: values.description,
      category: values.course,
      type: values.isPublic,
      tags: tags.value,
    });
    console.log(result);
    toast({
      variant: "success",
      description: "Group created successfully!",
      duration: 1500,
    });

    setTimeout(() => {
      router.push({ name: "groups" });
    }, 1500);
  } catch (error) {
    toast({
      variant: "destructive",
      description: "Failed to create group. Please try again.",
      duration: 1500,
    });
  }
});

const onCancel = () => {
  router.push({ name: "groups" });
};
</script>

<style scoped>
.form-select,
.form-textarea {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 0.25rem;
}

.text-red-600 {
  color: #e3342f;
}

.margin-bottom-custom {
  padding-bottom: 3px;
}

.margin-top-custom {
  padding-top: 6px;
}

.tags-input-container {
  position: relative;
  border: 1px solid #ddd;
  padding: 0.5rem;
  border-radius: 0.25rem;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.tag {
  background-color: #e2e8f0;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  display: flex;
  align-items: center;
}

.remove-tag-button {
  background: none;
  border: none;
  margin-left: 0.25rem;
  cursor: pointer;
}

.tags-input {
  border: none;
  outline: none;
  width: 100%;
  margin-top: 0.5rem;
}

.suggestions-list {
  position: absolute;
  top: calc(100% + 0.5rem);
  left: 0;
  right: 0;
  background: white;
  border: 1px solid #ddd;
  max-height: 150px;
  overflow-y: auto;
  z-index: 1000;
  border-radius: 0.25rem;
  padding: 0;
  list-style: none;
}

.suggestion-item {
  padding: 0.5rem;
  cursor: pointer;
}

.suggestion-item:hover {
  background-color: #f1f5f9;
}
</style>
