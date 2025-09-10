<script setup>
import { reactive, ref } from 'vue'
import { auth } from '@/firebase'
import { createUserWithEmailAndPassword } from 'firebase/auth'
import { useNotificationStore } from '@/stores/notificationStore'
import LoaderIcon from '@/assets/icons/Loader.svg'
import axios from 'axios'
import { useAuthStore } from '@/stores/authStore'
import { getErrorMessage } from '@/utils'

const { showNotification } = useNotificationStore()
const authStore = useAuthStore()

const formDict = reactive({
  userName: '',
  email: '',
  password: '',
  confirmation: '',
})
const isLoading = ref(false)

function quickValidate(){
  if (formDict.email === ''){
    return null
  }
  if (formDict.password !== formDict.confirmation){
    return null
  }
  return true
}

const handleSubmit = async()=>{
  isLoading.value = true

  await new Promise((resolve) =>{
    setTimeout(resolve, 2000)
  })
  let userCredential;
  try{
    // validation
    if (!quickValidate()){return}
    userCredential = await createUserWithEmailAndPassword(auth, formDict.email, formDict.password)
    // userCredential.userと、onAuthStateChangedで渡される user は同じ。

    console.log('Successfully user account has been created in Firebase Authentication:', userCredential.user);

    try{
      const user = userCredential.user
      const idToken = await user.getIdToken()
      const payload = { uid: user.uid, user_name: formDict.userName }
      const { data: {user_profile: user_profile} } = await axios.post(
        '/api/v1/auth/add-user-profile',
        payload,
        {headers: {Authorization: `Bearer ${idToken}`}},
      )
      authStore.isAdmin = user_profile.is_admin
      authStore.userName = user_profile.user_name

      showNotification('User registration have successfully done!', 'success')
      console.log('Successfully logged in:', user_profile);

    }catch(error){
      console.error('Failed to fetch user_profile from flask server:');
      throw error
    }

  }catch (error) {
    const message = getErrorMessage(error);
    console.error(message);

  }finally{
    isLoading.value = false
  }

}

</script>

<template>
  <div class="px-4 sm:px-8 ">
    <h1 class="text-4xl text-center py-6 ">Register</h1>

    <div class="py-4 ">
      <form @submit.prevent="handleSubmit" novalidate>

        <div class="mb-6">
          <label for="user-name" class="block mb-1 font-medium">User Name:</label>
          <input id="user-name" type="text" class="input-layout" v-model.trim="formDict.userName">
        </div>

        <div class="mb-6">
          <label for="email" class="block mb-1 font-medium">Email:</label>
          <input id="email" type="email" class="input-layout" v-model.trim="formDict.email">
        </div>

        <div class="mb-6">
          <label for="password" class="block mb-1 font-medium">Password:</label>
          <input id="password" type="password" class="input-layout" v-model="formDict.password">
        </div>

        <div class="mb-12">
          <label for="confirmation" class="block mb-1 font-medium">Confirmation:</label>
          <input id="confirmation" type="password" class="input-layout" v-model="formDict.confirmation">
        </div>

        <div class="mb-6">
          <button type="submit"
            class="button-layout-violet flex items-center justify-center gap-4"
            :class="{'!cursor-not-allowed': isLoading, 'opacity-50': isLoading}"
            :disabled="isLoading"
          >
            <LoaderIcon v-if="isLoading" class="animate-spin size-5" />
            Create Account
          </button>
        </div>
        <!-- <div>
          <button type="submit" class="button-layout-neutral">
            Cancel
          </button>
        </div> -->


          <p class="text-right mt-2 mb-4">
            You've already had
            <RouterLink :to="{name:'login'}" class="text-violet-400 font-bold">
              account?
            </RouterLink>
          </p>

      </form>
    </div>

  </div>
</template>