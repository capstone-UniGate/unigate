<template>
    <!-- Success Message --> 
  <div class="justify-center bg-gray-100">
   <p
      v-if="$route.query.message"
      class="mb-4 p-3 bg-blue-100 text-blue-800 border border-blue-300 rounded-lg text-center shadow"
    >
      {{ $route.query.message }}
    </p>
  </div>
  <div class="flex min-h-screen items-center justify-center bg-gray-100">
    <div class="w-full max-w-sm p-4 bg-white rounded-lg shadow-md">
      <h2 class="text-xl font-bold text-center text-gray-700 mb-4">Login</h2>
      <Form>
        <!-- Username Field -->
        <FormField name="username">
          <FormLabel for="username">Username</FormLabel>
          <div class="relative">
            <Input
              id="username"
              v-model="form.username"
              placeholder="Enter your username"
              :type="'text'"
            />
            <button
              v-if="form.username"
              @click="clearInput('username')"
              class="absolute right-2 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
              type="button"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-5 w-5"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path
                  fill-rule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                  clip-rule="evenodd"
                />
              </svg>
            </button>
          </div>
        </FormField>

        <!-- Password Field -->
        <FormField name="password">
          <FormLabel for="password">Password</FormLabel>
          <div class="relative">
            <Input
              id="password"
              v-model="form.password"
              placeholder="Enter your password"
              :type="'password'"
            />
            <button
              v-if="form.password"
              @click="clearInput('password')"
              class="absolute right-2 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
              type="button"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-5 w-5"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path
                  fill-rule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                  clip-rule="evenodd"
                />
              </svg>
            </button>
          </div>
          <p v-if="passwordError" class="text-red-500 text-sm mt-2">
            {{ passwordError }}
          </p>
        </FormField>

        <Button
          @click="handleLogin"
          type="button"
          class="mt-6 w-full bg-blue-600 hover:bg-blue-700 text-white"
          :disabled="!isFormValid"
        >
          Login
        </Button>
      </Form>
    </div>
  </div>
</template>

<script>
import { ref, computed } from "vue";
import { Form, FormField, FormLabel } from "@/components/ui/form";
import Button from "@/components/ui/button/Button.vue";
import Input from "@/components/ui/input/Input.vue";

export default {
  components: {
    Form,
    FormField,
    FormLabel,
    Button,
    Input,
  },
  setup() {
    const form = ref({
      username: "",
      password: "",
    });

    const passwordError = ref("");

    const isFormValid = computed(() => {
      return (
        form.value.username.trim() !== "" && form.value.password.trim() !== ""
      );
    });

    const isPasswordStrong = (password) => {
      return password.length >= 8 && /(?=.*[a-zA-Z])(?=.*\d)/.test(password);
    };

    const handleLogin = () => {
      if (!isPasswordStrong(form.value.password)) {
        passwordError.value =
          "Password is not strong enough. It must be at least 8 characters long and contain both letters and numbers.";
        return;
      }
      passwordError.value = "";
    };

    const clearInput = (field) => {
      form.value[field] = "";
    };

    return {
      form,
      isFormValid,
      handleLogin,
      passwordError,
      clearInput,
    };
  },
};
</script>
