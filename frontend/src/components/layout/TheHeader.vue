<script setup>
import { auth } from '@/firebase'
import { useAuthStore } from '@/stores/authStore'

const authStore = useAuthStore()

const handleLogout = async ()=>{
  try{
    // クライアントに保存されているIDトークンやリフレッシュトークンなどの認証情報を削除するだけ。
    // 端末紛失や盗難など "即時に全端末から切りたい" 場合は Admin SDK の
    // revokeRefreshTokens(uid) をバックエンドで呼ぶ必要がある。
    await auth.signOut()
    console.log('LOGOUT成功')

  }catch(error){
    console.log('failed to log out', error)
    console.log('LOGOUT失敗')
  }

}
</script>

<template>
  <header class="px-4 sm:px-8 shadow-sm bg-neutral-white dark:bg-neutral-700">
    <div class="py-4">
      <div class="flex justify-between items-center">
        <div class="text-3xl sm:text-4xl">LOGO HERE</div>
        <nav class="flex items-center gap-4">
          <RouterLink v-if="!authStore.isLoggedIn" :to="{name:'login'}">Login</RouterLink>
          <button v-else type="button" @click="handleLogout" class="">LogOut</button>
        </nav>
      </div>
    </div>
  </header>
</template>