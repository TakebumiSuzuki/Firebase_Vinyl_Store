<script setup>
  import { apiClient } from '@/api';
  import { reactive, ref } from 'vue'
  import { useNotificationStore } from '@/stores/notificationStore'
  import { useRouter } from 'vue-router'
  import LoaderIcon from '@/assets/icons/Loader.svg'

  const notificationStore = useNotificationStore()
  const router = useRouter()
  const formDict = reactive({
    email: ''
  })
  const isLoading = ref(false)

  const handleSubmit = async()=>{
    isLoading.value = true
    try{
      await apiClient.put('/api/v1/me/email', {email: formDict.email})
      notificationStore.showNotification('Successfully changed your email address.', 'success')
      router.push({name: 'home'})
    }catch(error){
      console.log(error)
      notificationStore.showNotification('Failed to change email. Please try it later again', 'error')
    }finally{
      isLoading.value = false
    }
  }

</script>
<template>
  <div class="px-4 sm:px-8 bg-neutral-600 rounded-lg">
    <h1 class="text-4xl text-center py-10">ChangeEmail</h1>
    <form @submit.prevent="handleSubmit" class="pb-12">
      <div>
        <label for="email" class="mb-1 block">Enter New Email:</label>
        <input id="email" type="email" v-model="formDict.email" class="input-layout">
      </div>
      <button type="submit" class="button-layout-violet mt-10 sm:!w-1/2 sm:!mx-auto block" :disabled="isLoading">
        <div class="flex gap-2 justify-center items-center">
          <LoaderIcon v-if="isLoading" class="animate-spin size-5" />
          Change Email
        </div>

      </button>

    </form>
  </div>

</template>