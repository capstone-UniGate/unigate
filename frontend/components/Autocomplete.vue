<template>
  <div class="relative w-full">
    <!-- Input Field -->
    <input
      v-model="search"
      @input="filterOptions"
      @focus="openDropdown = true"
      @blur="closeDropdown"
      :placeholder="placeholder"
      class="w-full border rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
    />

    <!-- Dropdown -->
    <ul
      v-if="openDropdown && filteredOptions.length > 0"
      class="absolute z-10 w-full bg-white border rounded-md shadow-md mt-1"
    >
      <li
        v-for="(option, index) in filteredOptions"
        :key="index"
        @mousedown.prevent="selectOption(option)"
        class="px-4 py-2 cursor-pointer hover:bg-gray-100"
      >
        {{ option.name }}
      </li>
    </ul>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, watch } from "vue";

export interface Option {
  id: number;
  name: string;
}

export default defineComponent({
  props: {
    options: {
      type: Array as () => Option[],
      required: true,
    },
    placeholder: {
      type: String,
      default: "Search...",
    },
    modelValue: {
      type: String,
      default: "",
    },
  },
  emits: ["update:modelValue", "select"],
  setup(props, { emit }) {
    const search = ref(props.modelValue);
    const filteredOptions = ref<Option[]>([]);
    const openDropdown = ref(false);

    const filterOptions = () => {
      filteredOptions.value = props.options.filter((option) =>
        option.name.toLowerCase().includes(search.value.toLowerCase()),
      );
    };

    const selectOption = (option: Option) => {
      emit("update:modelValue", option.name);
      emit("select", option);
      search.value = option.name;
      openDropdown.value = false;
    };

    const closeDropdown = () => {
      // Delay closing to allow option selection
      setTimeout(() => (openDropdown.value = false), 100);
    };

    watch(
      () => props.modelValue,
      (newValue) => {
        search.value = newValue;
        filterOptions();
      },
    );

    return {
      search,
      filteredOptions,
      openDropdown,
      filterOptions,
      selectOption,
      closeDropdown,
    };
  },
});
</script>
