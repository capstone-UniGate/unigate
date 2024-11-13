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
        <TagsInput class="px-0 gap-0 w-80" :model-value="modelValue">
    <div class="flex gap-2 flex-wrap items-center px-3">

      <TagsInputItem v-for="item in modelValue" :key="item" :value="item">
        <TagsInputItemText />
        <TagsInputItemDelete />
      </TagsInputItem>
    </div>

    <ComboboxRoot v-bind="componentField" v-model="modelValue" v-model:open="open" v-model:search-term="searchTerm" class="w-full">
      <ComboboxAnchor as-child>
        <ComboboxInput placeholder="Framework..." as-child>
          <TagsInputInput class="w-full px-3" :class="modelValue.length > 0 ? 'mt-2' : ''" @keydown.enter.prevent />
        </ComboboxInput>
      </ComboboxAnchor>

      <ComboboxPortal>
        <ComboboxContent>
          <CommandList
            position="popper"
            class="w-[--radix-popper-anchor-width] rounded-md mt-2 border bg-popover text-popover-foreground shadow-md outline-none data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2"
            >
            <CommandEmpty />
            <CommandGroup>
              <CommandItem
                v-for="framework in filteredFrameworks" :key="framework.value" :value="framework.label"
                @select.prevent="(ev) => {
                  if (typeof ev.detail.value === 'string') {
                    searchTerm = ''
                    modelValue.push(ev.detail.value)
                  }

                  if (filteredFrameworks.length === 0) {
                    open = false
                  }
                }"
              >
                {{ framework.label }}
              </CommandItem>
            </CommandGroup>
          </CommandList>
        </ComboboxContent>
      </ComboboxPortal>
    </ComboboxRoot>
  </TagsInput>
</FormControl>
</FormItem>
<FormMessage />
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

  import { CommandEmpty, CommandGroup, CommandItem, CommandList } from '@/components/ui/command'
  import { TagsInput, TagsInputInput, TagsInputItem, TagsInputItemDelete, TagsInputItemText } from '@/components/ui/tags-input'
  import { ComboboxAnchor, ComboboxContent, ComboboxInput, ComboboxPortal, ComboboxRoot } from 'radix-vue'
  import { computed, ref } from 'vue'
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
    description: z.string().min(10, "The description is too short").max(300),
    tags: z.string().min(1, "Set at least one tag"),
  }))

  const { handleSubmit, errors } = useForm({
    validationSchema: formSchema,
  })

  const errorMessage = ref("")

  const frameworks = [
  { value: 'next.js', label: 'Next.js' },
  { value: 'sveltekit', label: 'SvelteKit' },
  { value: 'nuxt', label: 'Nuxt' },
  { value: 'remix', label: 'Remix' },
  { value: 'astro', label: 'Astro' },
]

const modelValue = ref<string[]>([])
const open = ref(false)
const searchTerm = ref('')

const filteredFrameworks = computed(() => frameworks.filter(i => !modelValue.value.includes(i.label)))

  const onSubmit = handleSubmit((values) => {
    if(checkTags(values.tags)){
      errorMessage.value = "Set at least one tag"
    }

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

  const checkTags = (tags: string | undefined) => {
    if(typeof tags === 'undefined'){
      return true;
    }
    let actualTags = tags.split(",");
    console.log(actualTags);
    return actualTags.length < 1;

  }

  const onCancel = () => {
        history.go(-1)
  }

  const checkForDuplicateGroup = (/*name, course*/) => {
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
  padding-bottom: 3px;
}

 .margin-top-custom {
  padding-top: 6px;
 }



  </style>
