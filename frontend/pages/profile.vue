<template>
  <div>
    <input
      id="upload-photo"
      type="file"
      @change="onFileChange"
      :disabled="!usernameStore.length"
      style="display: none"
    />
    <div
      class="mx-auto group relative h-16 w-16 md:w-24 md:h-24 rounded-full bg-black cursor-pointer"
    >
      <img
        class="transition group-hover:opacity-50 rounded-full h-16 w-16 md:w-24 md:h-24"
        :alt="usernameStore"
        :src="previewUrl || defaultUrl"
      />
      <label for="upload-photo">
        <i
          class="opacity-0 transition group-hover:scale-110 absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-dark group-hover:text-white group-hover:opacity-100 text-4xl md:text-6xl bi bi-plus cursor-pointer"
        />
      </label>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from "vue";
import { useImageUploader } from "~/composables/useImageUploader";

// Mocked stores - Replace with your actual stores
const usernameStore = ref("1234567"); // Replace with your actual username store
const defaultUrl = `localhost:9000/propics/${usernameStore.value}`;

// Use the image uploader composable
const { previewUrl, uploadImage, updatePreview } = useImageUploader();

const onFileChange = async (event: Event) => {
  const input = event.target as HTMLInputElement;
  if (input.files && input.files[0]) {
    const file = input.files[0];

    // Update the image preview
    updatePreview(file);

    // Upload the image
    try {
      await uploadImage(usernameStore.value, file);
    } catch (error) {
      console.error("Error during image upload:", error);
    }
  }
};
</script>

<style scoped>
/* Hide input field */
input[type="file"] {
  display: none;
}
</style>
