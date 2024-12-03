<template>
    <div class="flex min-h-screen items-center justify-center bg-gray-100">
      <div class="w-full max-w-sm p-4 bg-white rounded-lg shadow-md">
        <h2 class="text-xl font-bold text-center text-gray-700 mb-4">Login</h2>
        <Form @submit.prevent="handleLogin">
          <!-- Username Field -->
          <FormField name="username">
            <FormLabel for="username">Username</FormLabel>
            <Input
              id="username"
              v-model="form.username"
              placeholder="Enter your username"
              :type="'text'"
              @input="validateInput"
            />
          </FormField>
  
          <!-- Password Field -->
          <FormField name="password">
            <FormLabel for="password">Password</FormLabel>
            <Input
              id="password"
              v-model="form.password"
              placeholder="Enter your password"
              :type="'password'"
              @input="validateInput"
            />
          </FormField>
  
          <Button 
            type="submit" 
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
  
  export default {
    components: {
      Form,
      FormField,
      FormLabel,
      Button,
    },
    setup() {
      const form = ref({
        username: "",
        password: "",
      });
  
      const isFormValid = computed(() => {
        return form.value.username.trim() !== "" && form.value.password.trim() !== "";
      });
  
      const validateInput = () => {
        // This function can be expanded for more complex validation if needed
      };
  
      const handleLogin = () => {
        // Handle login logic here
      };
  
      return {
        form,
        isFormValid,
        validateInput,
        handleLogin,
      };
    },
  };
  </script>
  
  