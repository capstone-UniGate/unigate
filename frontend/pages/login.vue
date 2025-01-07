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
      <Form id="login-form">
        <!-- Username Field -->
        <FormField name="username">
          <FormLabel for="username">Username</FormLabel>
          <div class="relative">
            <Input
              id="username"
              v-model="form.username"
              placeholder="Enter your username"
              :type="'text'"
              tabindex="1"
            />
            <button
              v-if="form.username"
              @click="clearInput('username')"
              class="absolute right-2 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
              type="button"
              tabindex="-1"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-5 w-5"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path
                  fill-rule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 00-1.414-1.414L10 8.586 8.707 7.293z"
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
              tabindex="1"
            />
            <button
              v-if="form.password"
              @click="clearInput('password')"
              class="absolute right-2 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
              type="button"
              tabindex="-1"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-5 w-5"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path
                  fill-rule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 101.414 1.414L10 11.414l1.293 1.293a1 1 001.414-1.414L11.414 10l1.293-1.293a1 1 00-1.414-1.414L10 8.586 8.707 7.293z"
                  clip-rule="evenodd"
                />
              </svg>
            </button>
          </div>
          <p v-if="passwordError" class="text-red-500 text-sm mt-2">
            {{ passwordError }}
          </p>
          <!-- Password Strength Progress Bar -->
          <!-- <div class="mt-2">
            <Progress
              :modelValue="passwordStrength"
              :colorClass="passwordStrengthColorClass"
            />
            <p class="text-sm mt-1" :class="passwordStrengthTextClass">
              {{ passwordStrengthText }}
            </p>
          </div>-->
        </FormField>

        <Button
          @click="handleLogin"
          id="login_button"
          type="button"
          class="mt-6 w-full bg-blue-600 hover:bg-blue-700 text-white"
          :disabled="!isFormValid"
          tabindex="3"
        >
          Login
        </Button>
      </Form>
    </div>
  </div>
</template>

<script lang="ts">
import { ref, computed } from "vue";
import { useRouter } from "vue-router";
import { Form, FormField, FormLabel } from "@/components/ui/form";
import Button from "@/components/ui/button/Button.vue";
import Input from "@/components/ui/input/Input.vue";
import Progress from "@/components/ui/progress/Progress.vue";
import { useAuth } from "@/composables/useAuth";

export default {
  components: {
    Form,
    FormField,
    FormLabel,
    Button,
    Input,
    Progress,
  },
  setup() {
    const router = useRouter();
    const { login } = useAuth();

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

    const passwordStrength = computed(() => {
      const password = form.value.password;
      let strength = 0;
      const hasLowercase = /[a-z]/.test(password);
      const hasUppercase = /[A-Z]/.test(password);
      const hasNumber = /\d/.test(password);
      const hasSpecial = /[^a-zA-Z0-9]/.test(password);

      if (password.length >= 8) strength += 20;
      if (hasLowercase) strength += 20;
      if (hasUppercase) strength += 20;
      if (hasNumber) strength += 20;
      if (hasSpecial) strength += 20;

      return strength;
    });

    const passwordStrengthText = computed(() => {
      if (passwordStrength.value < 40) return "Very Weak";
      if (passwordStrength.value < 60) return "Weak";
      if (passwordStrength.value < 80) return "Moderate";
      if (passwordStrength.value < 100) return "Strong";
      return "Very Strong";
    });

    const passwordStrengthTextClass = computed(() => {
      if (passwordStrength.value < 40) return "text-red-500";
      if (passwordStrength.value < 60) return "text-yellow-500";
      if (passwordStrength.value < 80) return "text-blue-500";
      if (passwordStrength.value < 100) return "text-green-500";
      return "text-green-700";
    });

    const passwordStrengthColorClass = computed(() => {
      if (passwordStrength.value < 40) return "bg-red-500";
      if (passwordStrength.value < 60) return "bg-yellow-500";
      if (passwordStrength.value < 80) return "bg-blue-500";
      if (passwordStrength.value < 100) return "bg-green-500";
      return "bg-green-700";
    });

    const handleLogin = async () => {
      const password = form.value.password;
      // if (
      //   passwordStrength.value < 100 ||
      //   !/[A-Z]/.test(password) ||
      //   !/[a-z]/.test(password) ||
      //   !/\d/.test(password) ||
      //   !/[^a-zA-Z0-9]/.test(password)
      // ) {
      //   passwordError.value =
      //     'Password must contain at least 8 characters, including uppercase, lowercase, a number, and a special character.'
      //   return
      // }
      passwordError.value = "";

      try {
        await login({
          username: form.value.username,
          password: form.value.password,
        });
        // Check if user is professor (PXXXXXXX) or student (SXXXXXXX)
        if (form.value.username.startsWith("P")) {
          router.push("/dashboard");
        } else {
          router.push("/groups");
        }
      } catch (error: any) {
        passwordError.value = error?.data?.message || "Login failed.";
        clearInput("username");
        clearInput("password");
      }
    };

    const clearInput = (field: "username" | "password") => {
      form.value[field] = "";
    };

    return {
      form,
      isFormValid,
      handleLogin,
      passwordError,
      clearInput,
      passwordStrength,
      passwordStrengthText,
      passwordStrengthTextClass,
      passwordStrengthColorClass,
    };
  },
};
</script>
