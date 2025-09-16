<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { auth } from '@/firebase'
import { useAuthStore } from '@/stores/authStore'
import { useNotificationStore } from '@/stores/notificationStore'
import { getErrorMessage } from '@/utils'
import SettingIcon from '@/assets/icons/Setting.svg'

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

const isOpen = ref(false);
const toggleMenu = () => { isOpen.value = !isOpen.value; };

// 項目をクリックしたときにメニューを閉じる関数
const closeMenu = () => { isOpen.value = false; }

// --- メニュー外のクリックを検知して閉じる処理 ---
// 6. テンプレートのdiv要素を参照するためのref
const menuContainer = ref(null);

// 7. 外側がクリックされたかを判定する関数
const handleClickOutside = (event) => {
  if (menuContainer.value && !menuContainer.value.contains(event.target)) {
    isOpen.value = false;
  }
};

onMounted(() => {
  document.addEventListener('mousedown', handleClickOutside);
});
onBeforeUnmount(() => {
  document.removeEventListener('mousedown', handleClickOutside);
});

</script>

<template>
  <header class="px-6 sm:px-12 shadow-sm bg-neutral-white dark:bg-neutral-800">
    <div class="py-4">
      <div class="flex justify-between items-center max-w-[1200px] mx-auto">
        <div class="text-3xl sm:text-4xl">LOGO HERE</div>
        <nav class="flex items-center gap-4">
          <div v-if="!authStore.isLoggedIn" class="flex items-center justify-center gap-4">
            <RouterLink  :to="{name:'login'}">Login</RouterLink>
          </div>
          <div v-else class="flex items-center justify-center gap-4">

            <div class="relative inline-block" ref="menuContainer">
              <!-- 2. アイコンをクリック可能なbutton要素に変更 -->
              <button @click="toggleMenu" type="button" aria-label="Open the setting menue">
                <SettingIcon class="size-5" />
              </button>

              <!-- 3. v-ifでメニューの表示・非表示を制御 -->
              <transition
                enter-active-class="transition duration-200 ease-out"
                enter-from-class="transform opacity-0 scale-95"
                enter-to-class="transform opacity-100 scale-100"
                leave-active-class="transition duration-150 ease-in"
                leave-from-class="transform opacity-100 scale-100"
                leave-to-class="transform opacity-0 scale-95"
              >
                <div
                  v-if="isOpen"
                  class="absolute top-full left-1/2 -translate-x-1/2 mt-2 w-max
                        bg-neutral-300/60 rounded-sm drop-shadow-xs
                        [&>*]:block [&>*]:py-2 [&>*]:border-b [&>*]:border-neutral-100 [&>*]:last:border-none
                        [&>*]:hover:bg-neutral-400 [&>*]:px-4 [&>*]:transition [&>*]:duration-200 [&>*]:whitespace-nowrap"
                >
                  <RouterLink :to="{name: 'user-info'}" @click="closeMenu">Your Info</RouterLink>
                  <RouterLink :to="{name: 'change-email'}" @click="closeMenu">Change Email</RouterLink>
                  <RouterLink :to="{name: 'change-password'}" @click="closeMenu">Change Password</RouterLink>
                  <RouterLink :to="{name: 'change-profile'}" @click="closeMenu">Change Profile</RouterLink>
                </div>
              </transition>
            </div>

            <button  type="button" @click="handleLogout" class="">LogOut</button>
          </div>

        </nav>
      </div>
    </div>
  </header>
</template>