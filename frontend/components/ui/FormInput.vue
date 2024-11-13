<template>
  <div class="formInput">
    <label>{{ label }}</label>
    <input type="text" v-model="inputValue" />
  </div>
</template>

<script>
export default {
  name: 'FormInput',
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
</script>

<style scoped>
.formInput {
    margin-bottom: 1em;
}
  
.formInput label {
    display: block;
    margin-bottom: 0.5em;
    font-weight: bold;
}
  
.formInput input[type="text"],
.formInput select,
.formInput textarea {
    width: 100%;
    padding: 0.5em;
    border: 1px solid #ccc;
    border-radius: 4px;
}
  
.formInput textarea {
    resize: vertical;
}
</style>
