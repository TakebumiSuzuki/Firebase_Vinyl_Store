<script setup>
import { auth } from '@/firebase'
import { useAuthStore } from '@/stores/authStore'
import { useNotificationStore } from '@/stores/notificationStore'
import { getErrorMessage } from '@/utils'

const authStore = useAuthStore()
const notificationStore = useNotificationStore()

const handleLogout = async ()=>{
  try{
    // クライアントに保存されているIDトークンやリフレッシュトークンなどの認証情報を削除するだけ。
    // 端末紛失や盗難など "即時に全端末から切りたい" ような場合は Admin SDK の
    // revokeRefreshTokens(uid) をバックエンドで呼ぶ必要がある。
    await auth.signOut()
    notificationStore.showNotification('You have logged out.', 'success')

  }catch(error){
    const message = getErrorMessage(error)
    notificationStore.showNotification('Failed to log out.Please try it later again.', 'error')
    console.log(message)
  }
}
</script>

<template>
  <header class="px-8 shadow-sm bg-neutral-white dark:bg-neutral-700">
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