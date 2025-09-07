import { defineStore } from "pinia";
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('authStore', ()=>{

  const user = ref(null)
  const isLoggedIn = computed(()=>{
    return Boolean(user)
  })
  const isAdmin = ref(null)

  function setUser(user){
    user.value = user
  }

  return {
    user,
    isLoggedIn,
    isAdmin,
    setUser,
  }

})