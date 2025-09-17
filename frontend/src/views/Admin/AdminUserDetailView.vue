<script setup>
  import { ref, onMounted } from 'vue'
  import { apiClient } from '@/api';

  const user_info = ref(null)
  const props = defineProps({
    uid: { type: String, required: true }
  })

  onMounted(async()=>{
    try{
      const {data: {unified_user_info: unified_user_info}} = await apiClient.get(`/api/v1/admin-user/${props.uid}`)
      user_info.value = unified_user_info
      console.log('うまいこと情報ゲットした')
    }catch(error){
      console.log('情報取得失敗 ', error)
    }
  })

</script>


<template>
  <div v-if="user_info">
    {{ user_info }}
  </div>
</template>