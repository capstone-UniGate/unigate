<template>
    <div class="w-2/3 mx-auto margin-top-custom">
      <form class="space-y-6" @submit.prevent="onSubmit">
        <!-- Name Field -->
        <FormField v-slot="{ componentField }" name="name">
          <FormItem>
            <FormLabel>Name</FormLabel>
            <FormControl>
              <Input type="text" placeholder="Group Name" v-bind="componentField" />
            </FormControl>
            <FormMessage />
          </FormItem>
        </FormField>

        <!-- Course Field -->
        <FormField v-slot="{ componentField }" name="course">
          <FormItem>
            <FormLabel>Course</FormLabel>
            <FormControl>
              <select v-bind="componentField" class="form-select">
                <option value="">Select from student's courses</option>
                <option value="course1">Course 1</option>
                <option value="course2">Course 2</option>
                <!-- Add other courses as needed -->
              </select>
            </FormControl>
            <FormMessage />
          </FormItem>
        </FormField>

        <!-- Privacy Type (Public or Private) -->
        <div>
        <FormField v-slot="{ componentField, errorMessage }" name="isPublic">
            <FormItem>
            <div class="flex items-center space-x-4">
                <label class="inline-flex items-center">
                <input type="radio" value="public" v-bind="componentField" />
                <span class="ml-2">Public</span>
                </label>
                <label class="inline-flex items-center">
                <input type="radio" value="private" v-bind="componentField" />
                <span class="ml-2">Private</span>
                </label>
            </div>
            <!-- Display "Required" message only if there's an error -->
            <FormMessage v-if="errorMessage">{{ errorMessage }}</FormMessage>
            </FormItem>
        </FormField>
        </div>

        <!-- Description Field -->
        <FormField v-slot="{ componentField }" name="description">
          <FormItem>
            <FormLabel>Description</FormLabel>
            <FormControl>
              <textarea v-bind="componentField" placeholder="Describe your group" class="form-textarea"></textarea>
            </FormControl>
            <FormMessage />
          </FormItem>
        </FormField>

        <!-- Tags Field -->
        <FormField v-slot="{ componentField }" name="tags">
          <FormItem>
            <FormLabel>Tags</FormLabel>
            <FormControl>
              <Input type="text" placeholder="Enter tags" v-bind="componentField" />
            </FormControl>
            <FormMessage />
          </FormItem>
        </FormField>

        <!-- Error Message Placeholder -->
        <div v-if="errorMessage" class="text-red-600">{{ errorMessage }}</div>

        <!-- Buttons -->
        <div class="flex justify-end space-x-4 margin-bottom-custom">
          <Button type="button" @click="onCancel"  variant="destructive">
            Cancel
          </Button>
          <Button type="submit" :disabled="formHasErrors">
            Create
          </Button>
        </div>
      </form>
    </div>
  </template>

  <script setup lang="ts">
  import { Button } from '@/components/ui/button'
  import {
    FormControl,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
  } from '@/components/ui/form'
  import { Input } from '@/components/ui/input'
  import { toast } from '@/components/ui/toast'
  import { toTypedSchema } from '@vee-validate/zod'
  import { useForm } from 'vee-validate'
  import * as z from 'zod'

  // Define the schema for validation
  const formSchema = toTypedSchema(z.object({
    name: z.string().min(2, "Name must be at least 2 characters long").max(50),
    course: z.string().nonempty("Course is required"),
    isPublic: z.enum(["public", "private"]),
    description: z.string().optional(),
    tags: z.string().optional(),
  }))

  const { handleSubmit, errors } = useForm({
    validationSchema: formSchema,
  })

  const errorMessage = ref("")

  const onSubmit = handleSubmit((values) => {
    if (checkForDuplicateGroup(/*values.name, values.course*/)) {
      errorMessage.value = "Duplicate group name or already enrolled in a group for that course"
    } else {
      toast({
        title: 'Group Created Successfully',
        description: `You created a group with the following details: ${JSON.stringify(values)}`,
      })
      errorMessage.value = ""
    }
  })

  const onCancel = () => {
        history.go(-1)

  }

  const checkForDuplicateGroup = (/*name, course*/) => {
    // Placeholder function to check if the group already exists
    // Replace with actual check logic
    return false
  }

  const formHasErrors = computed(() => Object.keys(errors.value).length > 0)
  </script>

  <style scoped>
  .form-select, .form-textarea {
    width: 100%;
    padding: 0.5rem;
    border: 1px solid #ddd;
    border-radius: 0.25rem;
  }

  .text-red-600 {
    color: #e3342f;
  }

  .margin-bottom-custom {
  padding-bottom: 3px; /* o qualsiasi valore desiderato */
}

 .margin-top-custom {
  padding-top: 6px; /* o qualsiasi valore desiderato */
 }



  </style>