<script setup>
  import { apiClient } from '@/api';
  import { reactive, ref } from 'vue'
  import { useNotificationStore } from '@/stores/notificationStore'
  import { useRouter } from 'vue-router'
  import LoaderIcon from '@/assets/icons/Loader.svg'

  const notificationStore = useNotificationStore()
  const router = useRouter()
  const formDict = reactive({
    password: ''
  })
  const isLoading = ref(false)

  const handleSubmit = async()=>{
    isLoading.value = true
    // validation
    try{
      await apiClient.put('/api/v1/me/password', {password: formDict.password})
      notificationStore.showNotification('Successfully changed your password.', 'success')
      router.push({name: 'home'})
    }catch(error){
      console.log(error)
      notificationStore.showNotification('Failed to change your password. Please try it later again', 'error')
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
        <label for="password" class="mb-1 block">Enter New Password:</label>
        <input id="password" type="password" v-model="formDict.password" class="input-layout">
      </div>
      <div class="mt-8">
        <label for="confirmation" class="mb-1 block">Enter Password Again:</label>
        <input id="confirmation" type="confirmation" v-model="formDict.confirmation" class="input-layout">
      </div>
      <button type="submit" class="button-layout-violet mt-10 sm:!w-1/2 sm:!mx-auto block" :disabled="isLoading">
        <div class="flex gap-2 justify-center items-center">
          <LoaderIcon v-if="isLoading" class="animate-spin size-5" />
          Change Password
        </div>

      </button>

    </form>
  </div>

</template>