<template>
  <div class="formRadio">
    <input type="radio" :name="name" :value="value" v-model="selectedValue" />
    <label>{{ label }}</label>
  </div>
</template>

<script>
export default {
  name: "FormRadio",
  props: ["label", "name", "value", "modelValue"],
  computed: {
    selectedValue: {
      get() {
        return this.modelValue;
      },
      set(value) {
        this.$emit("update:modelValue", value);
      },
    },
  },
};
</script>

<style scoped>
.formRadio {
  margin-bottom: 1em;
}

.formRadio label {
  display: inline;
  margin-bottom: 0.5em;
  font-weight: bold;
}

.formRadio input[type="text"],
.formRadio select,
.formRadio textarea {
  width: 100%;
  padding: 0.5em;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.formRadio textarea {
  resize: vertical;
}
</style>
