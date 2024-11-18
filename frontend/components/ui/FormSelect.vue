<template>
  <div class="formSelect">
    <label>{{ label }}</label>
    <select v-model="selectedValue">
      <option disabled value="">Select from your courses</option>
      <option v-for="option in options" :key="option" :value="option">
        {{ option }}
      </option>
    </select>
  </div>
</template>

<script>
export default {
  name: "FormSelect",
  props: ["label", "options", "value"],
  computed: {
    selectedValue: {
      get() {
        return this.value;
      },
      set(value) {
        this.$emit("input", value);
      },
    },
  },
};
</script>

<style scoped>
.formSelect {
  margin-bottom: 1em;
}

.formSelect label {
  display: block;
  margin-bottom: 0.5em;
  font-weight: bold;
}

.formSelect input[type="text"],
.formSelect select,
.formSelect textarea {
  width: 100%;
  padding: 0.5em;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.formSelect textarea {
  resize: vertical;
}
</style>
