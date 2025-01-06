<script setup lang="ts">
import { ref, watch, defineProps, defineEmits } from "vue";

const props = defineProps({
  examDates: {
    type: Array as () => string[],
    required: true,
  },
  selectedDate: {
    type: String,
    default: "",
  },
  disabled: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(["update:selectedDate"]);

// Local state for selected date
const localSelectedDate = ref(props.selectedDate);

// Watch for prop changes and update local state
watch(
  () => props.selectedDate,
  (newVal) => {
    localSelectedDate.value = newVal;
  },
);

// Emit selected date when it changes
watch(localSelectedDate, (newVal) => {
  emit("update:selectedDate", newVal);
});
</script>

<template>
  <div>
    <label for="examDate" class="block mb-2 text-sm font-medium text-gray-700">
      Exam Date
    </label>
    <select
      id="examDate"
      v-model="localSelectedDate"
      class="w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring focus:ring-blue-200 focus:border-blue-500"
      :disabled="disabled"
    >
      <!-- Allow the user to reset the selection -->
      <option id="data_0" value="">Select Exam Date</option>
      <option :id="'data_' + (index + 1)"  
      v-for="(date, index) in examDates" :key="date" :value="date">
        {{ date }}
      </option>
    </select>
  </div>
</template>
