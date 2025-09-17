<script setup>
  import { onMounted, ref } from 'vue'
  import { apiClient } from '@/api'

  const users = ref(null)

  onMounted(async()=>{
    try{
      const {data: {user_profiles: user_profiles}} = await apiClient.get('/api/v1/admin-user')
      console.log(user_profiles)
      users.value = user_profiles
    }catch(error){
      console.log(error)
    }
  })

</script>

<template>
  <h1 class="text-4xl text-center py-2">Users Info</h1>

  <div>
    <div v-if="users">
      <div v-for="user_profile in users" :key="user_profile.uid">
        <RouterLink :to="{name: 'admin-user-detail', params:{uid: user_profile.uid}}">{{ user_profile.email }}</RouterLink>
      </div>
    </div>
    <div v-else>
      Couldnt find user
    </div>
  </div>


</template>