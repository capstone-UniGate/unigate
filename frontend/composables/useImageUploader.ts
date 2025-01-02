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
        `students/propic-presigned-url`,
        {
          method: "GET",
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

  // Get the photo from db and set it to previewUrl
  const getPhoto = async () => {
    try {
      const response = await useApiFetch(`students/propic-presigned-url`, {
        method: "GET",
      });

      if (response.data?.propic) {
        // Create a blob from the URL to handle it like a file
        const imageResponse = await fetch(response.data.propic);
        const imageBlob = await imageResponse.blob();

        previewUrl.value = URL.createObjectURL(imageBlob);
      } else {
        previewUrl.value = null;
      }
    } catch (error) {
      console.error("Error fetching profile photo:", error);
      previewUrl.value = null;
      throw error;
    }
  };

  return {
    previewUrl,
    uploadImage,
    updatePreview,
    getPhoto,
  };
}
