<script setup>
import { reactive, ref } from 'vue'
import { auth } from '@/firebase'
import { createUserWithEmailAndPassword } from 'firebase/auth'
import { useNotificationStore } from '@/stores/notificationStore'
import LoaderIcon from '@/assets/icons/Loader.svg'
import axios from 'axios'

const { showNotification } = useNotificationStore()

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
    console.log(formDict)
    userCredential = await createUserWithEmailAndPassword(auth, formDict.email, formDict.password)
    // userCredential.userと、onAuthStateChangedで渡される user は同じ。
    showNotification('User registration have successfully done!', 'success')
    console.log('FIREBASE AUTH登録成功:', userCredential.user);

    try{
      const user = userCredential.user
      const idToken = await user.getIdToken()
      const payload = { uid: user.uid, email: user.email, displayName: formDict.userName }
      const response = await axios.post(
        '/api/v1/auth/add-userporfile',
        payload,
        {headers: {Authorization: `Bearer ${idToken}`}},
      )
      console.log('USERPROFILE登録成功:', response.data);
    }catch(error){
      console.error('登録エラー:', error.message);
    }

  }catch(error){
    console.error('登録エラー:', error.message);
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
            class="button-layout-violet flex items-center justify-center"
            :class="{'!cursor-not-allowed': isLoading, 'opacity-50': isLoading}"
            :disabled="isLoading"
          >
            <LoaderIcon v-if="isLoading" class="animate-spin size-5 gap-4" />
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