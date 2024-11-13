<template>
  <div class="formTextArea">
    <label>{{ label }}</label>
    <textarea v-model="inputValue"></textarea>
  </div>
</template>

<script>
export default {
  name: 'FormTextArea',
  props: ['label', 'value'],
  computed: {
    inputValue: {
      get() {
        return this.value;
      },
      set(value) {
        this.$emit('input', value);
      },
    },
  },
};
</script>s

<style scoped>
.formTextArea {
    margin-bottom: 1em;
  }

.formTextArea label {
    display: block;
    margin-bottom: 0.5em;
    font-weight: bold;
  }

  .formTextArea input[type="text"],
  .formTextArea select,
  .formTextArea textarea {
    width: 100%;
    padding: 0.5em;
    border: 1px solid #ccc;
    border-radius: 4px;
  }

  .formTextArea textarea {
    resize: vertical;
  }
</style>
