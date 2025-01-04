<template>
  <Toaster />
  <div class="container mx-auto px-4 py-8 mt-16">
    <div class="max-w-2xl mx-auto bg-white rounded-lg shadow-md p-6">
      <!-- User Profile Header with Edit Button -->
      <div class="flex justify-between items-start mb-6">
        <div class="flex items-center space-x-4">
          <!-- Read-only Avatar (when not editing) -->
          <div class="relative" v-if="!isEditing">
            <Avatar class="w-20 h-20">
              <AvatarImage
                :src="
                  previewUrl || photoUrl || 'https://github.com/radix-vue.png'
                "
                alt="@radix-vue"
              />
              <AvatarFallback>{{ getInitials }}</AvatarFallback>
            </Avatar>
          </div>

          <!-- Editable Avatar (when editing) -->
          <div
            v-else
            class="relative group cursor-pointer"
            @click="triggerFileInput"
            v-if="!isUploading"
          >
            <Avatar class="w-20 h-20">
              <AvatarImage
                :src="
                  previewUrl || photoUrl || 'https://github.com/radix-vue.png'
                "
                alt="@radix-vue"
              />
              <AvatarFallback>{{ getInitials }}</AvatarFallback>
            </Avatar>
            <div
              class="absolute inset-0 bg-black bg-opacity-40 rounded-full opacity-0 group-hover:opacity-100 flex items-center justify-center transition-opacity"
            >
              <span class="text-white text-sm">Change Photo</span>
            </div>
          </div>

          <!-- Loading spinner (when uploading) -->
          <div
            v-if="isUploading"
            class="w-20 h-20 rounded-full bg-gray-100 flex items-center justify-center"
          >
            <span class="animate-spin">⌛</span>
          </div>
          <input
            id="upload-photo"
            type="file"
            ref="fileInput"
            class="hidden"
            accept="image/*"
            @change="handleFileUpload"
          />
          <div>
            <h1 class="text-2xl font-bold text-gray-900">
              {{ currentStudent?.name }} {{ currentStudent?.surname }}
            </h1>
            <p class="text-gray-500">
              Student Number: {{ currentStudent?.number }}
            </p>
            <span
              :class="[
                'inline-block px-3 py-1 mt-2 rounded-full text-sm font-medium',
                userRole === 'Student'
                  ? 'bg-blue-100 text-blue-800'
                  : 'bg-purple-100 text-purple-800',
              ]"
            >
              {{ userRole }}
            </span>
          </div>
        </div>

        <!-- Edit Button -->
        <Button
          @click="isEditing = true"
          class="bg-blue-500 hover:bg-blue-600 text-white"
          v-if="!isEditing"
        >
          Edit Profile
        </Button>
      </div>

      <!-- User Details -->
      <div class="space-y-4" v-if="!isEditing">
        <div class="border-t pt-4">
          <h2 class="text-lg font-semibold text-gray-900 mb-2">
            Contact Information
          </h2>
          <p class="text-gray-600">Email: {{ currentStudent?.email }}</p>
          <p class="text-gray-600">Role: {{ userRole }}</p>
        </div>
      </div>

      <!-- Edit Form -->
      <div v-else class="space-y-4">
        <div class="border-t pt-4">
          <h2 class="text-lg font-semibold text-gray-900 mb-4">Edit Profile</h2>
          <form @submit.prevent="handleSubmit" class="space-y-4">
            <div class="space-y-2">
              <label class="text-sm font-medium text-gray-700">Name</label>
              <input
                v-model="editForm.name"
                type="text"
                class="w-full p-2 border rounded-md"
                disabled
              />
            </div>

            <div class="space-y-2">
              <label class="text-sm font-medium text-gray-700">Surname</label>
              <input
                v-model="editForm.surname"
                type="text"
                class="w-full p-2 border rounded-md"
                disabled
              />
            </div>

            <div class="space-y-2">
              <label class="text-sm font-medium text-gray-700">Email</label>
              <input
                v-model="editForm.email"
                type="email"
                class="w-full p-2 border rounded-md bg-gray-100"
                disabled
              />
            </div>

            <div class="space-y-2">
              <label class="text-sm font-medium text-gray-700"
                >Student Number</label
              >
              <input
                v-model="editForm.number"
                type="text"
                class="w-full p-2 border rounded-md bg-gray-100"
                disabled
              />
            </div>

            <div class="flex space-x-4 pt-4">
              <Button
                type="submit"
                class="bg-green-500 hover:bg-green-600 text-white"
                :disabled="isSubmitting"
              >
                Save Changes
              </Button>
              <Button type="button" @click="cancelEdit" variant="outline">
                Cancel
              </Button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useCurrentStudent } from "@/composables/useCurrentStudent";
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { useToast } from "@/components/ui/toast/use-toast";
import { Toaster } from "@/components/ui/toast";
import { useImageUploader } from "~/composables/useImageUploader";
import { eventBus } from "~/utils/eventBus";

const router = useRouter();
const config = useRuntimeConfig();
const { currentStudent, getCurrentStudent } = useCurrentStudent();
const { toast } = useToast();
const isEditing = ref(false);
const fileInput = ref<HTMLInputElement | null>(null);
const isUploading = ref(false);
const isSubmitting = ref(false);

// Remove usernameStore and create a computed photo URL
const photoUrl = computed(() => {
  if (!currentStudent.value?.number) return null;
  return `${config.public.minioURL}/unigate/propics/${currentStudent.value.number}`;
});

// Use the image uploader composable
const { previewUrl, uploadImage, updatePreview, getPhoto } = useImageUploader();

// Edit form state
const editForm = ref({
  name: "",
  surname: "",
  email: "",
  number: "",
});

// Compute user role based on email prefix
const userRole = computed(() => {
  if (!currentStudent.value?.email) return "Unknown";
  const emailPrefix = currentStudent.value.email.charAt(0).toLowerCase();
  return emailPrefix === "s"
    ? "Student"
    : emailPrefix === "p"
      ? "Professor"
      : "Unknown";
});

// Compute initials from student name
const getInitials = computed(() => {
  if (!currentStudent.value?.name) return "U";
  const names =
    `${currentStudent.value.name} ${currentStudent.value.surname}`.split(" ");
  return names
    .map((name) => name[0])
    .join("")
    .toUpperCase();
});

// Initialize edit form with current user data
const initializeEditForm = () => {
  if (currentStudent.value) {
    editForm.value = {
      name: currentStudent.value.name,
      surname: currentStudent.value.surname,
      email: currentStudent.value.email,
      number: currentStudent.value.number,
    };
  }
};

// Cancel edit mode
const cancelEdit = () => {
  isEditing.value = false;
};

const triggerFileInput = () => {
  fileInput.value?.click();
};

const handleFileUpload = async (event: Event) => {
  const target = event.target as HTMLInputElement;
  const file = target.files?.[0];

  if (!file) return;

  try {
    isUploading.value = true;
    // Update the image preview
    updatePreview(file);

    await uploadImage(file);
    // After successful upload, update the previewUrl to the server URL
    // Inside handleFileUpload, after uploading:
    if (currentStudent.value?.number) {
      const newPhotoUrl = `${config.public.minioURL}/unigate/propics/${currentStudent.value.number}?t=${Date.now()}`;
      previewUrl.value = newPhotoUrl;
      eventBus.updatePhoto(newPhotoUrl);
    }

    toast({
      title: "Success",
      description: "Profile photo updated successfully",
    });
  } catch (error) {
    toast({
      title: "Error",
      description: "Failed to update profile photo",
      variant: "destructive",
    });
    console.error("Error uploading avatar:", error);
  } finally {
    isUploading.value = false;
    if (fileInput.value) fileInput.value.value = ""; // Reset file input
  }
};

const handleSubmit = async () => {
  isSubmitting.value = true;
  try {
    toast({
      title: "Success",
      description: "Profile updated successfully",
    });
    isEditing.value = false;
  } catch (error) {
    toast({
      title: "Error",
      description: "Failed to update profile",
      variant: "destructive",
    });
    console.error("Error updating profile:", error);
  } finally {
    isSubmitting.value = false;
  }
};

onMounted(async () => {
  if (!currentStudent.value) {
    await getCurrentStudent();
  }
  initializeEditForm();

  // Set initial preview URL
  if (currentStudent.value?.number) {
    const currentPhotoUrl = `${config.public.minioURL}/unigate/propics/${currentStudent.value.number}`;
    eventBus.updatePhoto(currentPhotoUrl);
  }
});
</script>
