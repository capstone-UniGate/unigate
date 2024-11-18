<template>
  <div v-if="message" class="error-message">
    {{ message }}
  </div>
</template>

<script>
export default {
  props: {
    message: String,
  },
};
</script>

<style>
.error-message {
  color: red;
  font-size: 0.9em;
  margin-bottom: 1em;
}
</style>
