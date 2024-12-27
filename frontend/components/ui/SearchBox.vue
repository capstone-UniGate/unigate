<script setup lang="ts">
import { ref, computed, watch, defineEmits, defineProps } from 'vue';

// Props
const props = defineProps({
  placeholder: {
    type: String,
    default: 'Search...',
  },
  items: {
    type: Array as () => { name: string }[],
    default: () => [],
  },
  modelValue: {
    type: String,
    default: '',
  },
});

// Emit events
const emit = defineEmits(['update:modelValue', 'select']);

// Local refs
const inputValue = ref(props.modelValue);
const showDropdown = ref(false); // Controls the visibility of the dropdown
const filteredItems = computed(() => {
  if (!inputValue.value) return [];
  return props.items.filter((item) =>
    item.name.toLowerCase().includes(inputValue.value.toLowerCase())
  );
});
const noResultsFound = computed(() => {
  return inputValue.value && filteredItems.value.length === 0;
});

// Watch for external changes
watch(
  () => props.modelValue,
  (newValue) => {
    inputValue.value = newValue;
  }
);

// Update value on input
const updateValue = () => {
  emit('update:modelValue', inputValue.value);
  showDropdown.value = true; // Show dropdown when typing
};

// Select an item
const selectItem = (item: { name: string }) => {
  emit('select', item);
  inputValue.value = item.name;
  emit('update:modelValue', item.name);
  showDropdown.value = false; // Hide dropdown after selection
};

// Handle blur to close the dropdown when clicking outside
const handleBlur = () => {
  setTimeout(() => {
    showDropdown.value = false;
  }, 200); // Delay to allow click event to register
};
</script>

<template>
  <div class="relative">
    <input
      :placeholder="placeholder"
      v-model="inputValue"
      @input="updateValue"
      @focus="showDropdown = true"
      @blur="handleBlur"
      class="w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring focus:ring-blue-200 focus:border-blue-500"
    />
    <!-- Dropdown for filtered items -->
    <ul
      v-if="showDropdown && filteredItems.length"
      class="absolute w-full bg-white border border-gray-300 rounded-lg shadow-lg mt-2 z-10"
    >
      <li
        v-for="item in filteredItems"
        :key="item.name"
        class="px-4 py-2 hover:bg-gray-100 cursor-pointer"
        @click="selectItem(item)"
      >
        {{ item.name }}
      </li>
    </ul>
    <!-- No results found message -->
    <p v-if="showDropdown && noResultsFound" class="mt-2 text-red-500">No results found</p>
  </div>
</template>
