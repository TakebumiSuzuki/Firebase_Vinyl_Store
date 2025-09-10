<script setup>
import { reactive, ref } from 'vue'
import { auth } from '@/firebase'
import { signInWithEmailAndPassword } from 'firebase/auth'
import { useNotificationStore } from '@/stores/notificationStore'
import LoaderIcon from '@/assets/icons/Loader.svg'
import axios from 'axios'
import { useAuthStore } from '@/stores/authStore'
import { getErrorMessage } from '@/utils'

const { showNotification } = useNotificationStore()
const authStore = useAuthStore()

const formDict = reactive({
  email: '',
  password: '',
})
const isLoading = ref(false)

function quickValidate(){
  if (formDict.email === ''){
    return null
  }
  return true
}

const handleSubmit = async()=>{

  isLoading.value = true

  await new Promise((resolve) =>{
    setTimeout(resolve, 2000)
  })

  try{
    // validation
    if (!quickValidate()){return}
    console.log(formDict)
    const userCredential = await signInWithEmailAndPassword(auth, formDict.email, formDict.password)

    console.log(userCredential.user.uid)
    const idToken = await userCredential.user.getIdToken();
    const config = {
      headers: {
        Authorization: `Bearer ${idToken}`
      }
    };

    const { data: { user_profile : user_profile } } = await axios.get('/api/v1/me', config)
    authStore.userName = user_profile.user_name
    authStore.isAdmin =  user_profile.is_admin

    showNotification('You have logged in successfully!', 'success')
    console.log('Signed In Successfully :', userCredential.user);

  } catch(error) {
    const message = getErrorMessage(error);
    console.error(message);
    await auth.signOut()

  }finally{
    isLoading.value = false
  }

}

</script>

<template>
  <div class="px-4 sm:px-8 ">
    <h1 class="text-4xl text-center py-6 ">Login</h1>

    <div class="py-4 ">
      <form @submit.prevent="handleSubmit" novalidate>

        <div class="mb-6">
          <label for="email" class="block mb-1 font-medium">Email:</label>
          <input id="email" type="email" class="input-layout" v-model.trim="formDict.email">
        </div>

        <div class="mb-10">
          <label for="password" class="block mb-1 font-medium">Password:</label>
          <input id="password" type="password" class="input-layout"  v-model="formDict.password">
        </div>

        <div class="mb-6">
          <button type="submit"
            class="button-layout-violet flex items-center justify-center gap-4"
            :class="{'!cursor-not-allowed': isLoading, 'opacity-50': isLoading}"
            :disabled="isLoading"
          >
            <LoaderIcon v-if="isLoading" class="animate-spin size-5" />
            Login
          </button>
        </div>
        <!-- <div>
          <button type="submit" class="button-layout-neutral">
            Cancel
          </button>
        </div> -->


          <p class="text-right mt-2 mb-4">
            You don't have
            <RouterLink :to="{name:'register'}" class="text-violet-400 font-bold">
              account
            </RouterLink>
            yet?
          </p>

      </form>
    </div>

  </div>
</template>