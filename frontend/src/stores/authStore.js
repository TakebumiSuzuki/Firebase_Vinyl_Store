import { defineStore } from "pinia";
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('authStore', ()=>{

  const user = ref(null)
  const isLoggedIn = computed(()=>{
    return Boolean(user.value)
  })
  const isAdmin = ref(null)
  const userName = ref(null)

  function setUser(newUser){
    user.value = newUser
  }

  return {
    user,
    isLoggedIn,
    isAdmin,
    userName,
    setUser,
  }

})