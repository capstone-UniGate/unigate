<template>
  <Toaster/>
 <Button type="button" @click="onJoin" :disabled="joined">{{ join }}</Button>
</template>

<script setup lang="ts">

  import { Toaster } from '@/components/ui/toast'
  import { useToast } from '@/components/ui/toast/use-toast'
  import { Button } from '@/components/ui/button'

  import {ref,computed} from 'vue';

  const {toast} = useToast()
  let ciao = false;
  let joined = ref(false);


  const onJoin = () => {
    if(ciao){
      toast({
        variant: "destructive",
        title: 'Failure',
        description: 'You are already in a team for the same course',
      });
    }else{
      toast({
          title: 'Success',
          description: 'You joined the team',
        });
        joined.value=true;
    }
  }

  const join = computed(() => (joined.value? 'Joined':'Join'))
</script>
