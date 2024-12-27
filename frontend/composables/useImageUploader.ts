// composables/useImageUploader.ts
import { ref } from "vue";
import { useApiFetch } from "~/composables/useApiFetch";

export function useImageUploader() {
  const previewUrl = ref<string | null>(null);

  // Fetch a presigned URL from the API and upload the image
  const uploadImage = async (file: File): Promise<void> => {
    try {
      // Fetch the presigned URL
      const { url: presignedURL } = await useApiFetch(
        `students/propic-presigned-url/`,
        {
          method: "get",
        },
      );

      const x = await fetch(presignedURL, {
        method: "PUT",
        body: file,
        headers: {
          "Content-Type": file.type,
        },
      });

      console.log("Image uploaded successfully!");
    } catch (error) {
      console.error("Error uploading image:", error);
      throw error;
    }
  };

  // Update the image preview when a file is selected
  const updatePreview = (file: File): void => {
    previewUrl.value = URL.createObjectURL(file);
  };

  return {
    previewUrl,
    uploadImage,
    updatePreview,
  };
}
