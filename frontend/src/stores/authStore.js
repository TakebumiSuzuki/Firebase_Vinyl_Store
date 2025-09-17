import { defineStore } from "pinia";
import { ref, computed } from 'vue'
import { apiClient } from "@/api";

export const useAuthStore = defineStore('authStore', ()=>{

  const user = ref(null)
  const isLoggedIn = computed(()=>{
    return Boolean(user.value)
  })
  const isAdmin = ref(null)
  const userName = ref(null)

  async function setUser(newUser){
    user.value = newUser
    try{
      const {data:{user_profile:user_profile}} = await apiClient.get('/api/v1/me')
      console.log(user_profile)
      isAdmin.value = user_profile.is_admin
      userName.value = user_profile.user_name
    }catch(error){
      console.info(error)
    }
  }

  return {
    user,
    isLoggedIn,
    isAdmin,
    userName,
    setUser,
  }

})