<script setup>
import { reactive, ref } from 'vue'
import { auth } from '@/firebase'
import { signInWithEmailAndPassword, signInWithPopup, GoogleAuthProvider } from 'firebase/auth'
import { useNotificationStore } from '@/stores/notificationStore'
import LoaderIcon from '@/assets/icons/Loader.svg'
import axios from 'axios'
import { useAuthStore } from '@/stores/authStore'
import { getErrorMessage } from '@/utils'
import { useRouter } from 'vue-router'
import { apiClient } from '@/api'

const { showNotification } = useNotificationStore()
const authStore = useAuthStore()
const router = useRouter()

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
    router.push({name:'home'})

  } catch(error) {
    const message = getErrorMessage(error);
    console.log(error)
    console.error(message);
    await auth.signOut()

  }finally{
    isLoading.value = false
  }

}

const signInWithGoogle = () => {
  const provider = new GoogleAuthProvider();
  handleSocialLogin(provider);
};

const handleSocialLogin = async (provider) => {
  try {
    // ポップアップを表示して認証を行う。signInWithPopup関数の戻り値は Promiseを返すが、解決すると、
    // UserCredential オブジェクトが得られる。そしてこのオブジェクトには userプロパティが含まれる。
    // Googleからのサインインの場合、この User オブジェクトには基本的に常にメールアドレスが含まれる。
    // また、Googleアカウントは作成時に氏名の登録が必須なので、基本的に常に displayName も含まれる。
    // FirebaseとGoogleアカウントは、初回の認証時以降は継続的な繋がりを持たないため、
    // 初回ログイン後、ユーザーが名前を変更しても、Firebase Authには自動で反映されないことに注意。
    const { user } = await signInWithPopup(auth, provider);
    console.log("signInWithPopupでのログイン成功:", user.displayName);

    await apiClient.post('/api/v1/auth/social-login')
    showNotification(`You have logged in successfully via ${provider.providerId}!`, 'success')
    router.push('/home')

  } catch (error) {
    showNotification('Failed to login.Please try again later.', 'error')
    console.error("ログインエラー:", error.code, error.message);
  }
};

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

      <button
        class="button-layout-neutral"
        @click="signInWithGoogle"
      >
        Googleでログイン
      </button>
    </div>

  </div>
</template>