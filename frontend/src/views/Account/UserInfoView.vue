<script setup>
  import { onMounted, ref } from 'vue'
  import { apiClient } from '@/api'
  import UserInfoField from '@/components/ui/UserInfoField.vue'
  import UserInfoButton from '@/components/ui/UserInfoButton.vue'

  import { useRouter } from 'vue-router'
  import { useNotificationStore } from '@/stores/notificationStore'
  import { useConfirmationStore } from '@/stores/confirmationStore'

  import Loader from '@/assets/icons/Loader.svg'
  import UserIcon from '@/assets/icons/User.svg'
  import PasswordIcon from '@/assets/icons/Password.svg'
  import EmailIcon from '@/assets/icons/Email.svg'
  import DeleteIcon from '@/assets/icons/Delete.svg'

  const userProfile = ref(null)
  const isLoading = ref(false)
  const router = useRouter()
  const confirmationStore = useConfirmationStore()
  const notificationStore = useNotificationStore()

  const handleDeleteAccount = async()=>{
    const answer = await confirmationStore.showConfirmation(
      'Are you sure you wanna delete your account?',
      [
        { text: 'yes', value: true, style: 'primary' },
        { text: 'cancel', value: false, style: 'secondary' }
      ]
    )

    if (answer){
      try{
        await apiClient.delete('/api/v1/me')
        notificationStore.showNotification('Your accout has been deleted.', 'success')
        router.push({name: 'home'})
      }catch(error){
        console.error('Failed to delete user:', error.response?.data || error.message)
        notificationStore.showNotification('Failed to delete your account. Please try again later.', 'error')
      }
    }
  }

  onMounted(async()=>{
    try{
      isLoading.value = true
      const { data: {user_profile: userProfileData} } = await apiClient.get('/api/v1/me')
      userProfile.value = userProfileData
      console.log('Fetched UserProfile:', userProfileData)

    }catch(error){
      console.error('Failed to fetch user data in onMounted:', error.response?.data || error.message)
      notificationStore.showNotification('Failed to fetch user profile. Please try again later.', 'error')
    }finally{
      isLoading.value = false
    }
  })

</script>

<template>
  <div class="px-4 sm:px-8 pb-10 mb-14 bg-neutral-700/80 backdrop-blur-xs rounded-lg">
    <h1 class="text-4xl text-center py-10">Users Info</h1>
    <Loader v-if="isLoading" class="size-12 animate-spin block mx-auto mt-4" />
    <div v-else>
        <!-- <RouterLink :to="{name:'delete-account'}" class="button-layout-neutral">Delete Account</RouterLink> -->
      <div class="space-y-10">
        <!-- ユーザー情報セクション -->
        <div class="grid gap-4 sm:gap-8">
          <UserInfoField label="User Name" :fieldValue="userProfile?.user_name" />
          <UserInfoField label="Email" :fieldValue="userProfile?.email" />
          <UserInfoField label="Birthday" :fieldValue="userProfile?.birthday" />
          <UserInfoField label="Favorite Color" :fieldValue="userProfile?.favorite_color" />
        </div>

        <!-- アクションボタンセクション -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">

          <router-link :to="{name:'change-profile'}">
            <UserInfoButton baseColor="purple" buttonTitle="Change Profile">
              <UserIcon />
            </UserInfoButton>
          </router-link>

          <router-link :to="{name:'change-email'}">
            <UserInfoButton baseColor="teal" buttonTitle="Change Email">
              <EmailIcon />
            </UserInfoButton>
          </router-link>

          <router-link :to="{name:'change-password'}">
            <UserInfoButton baseColor="emerald" buttonTitle="Change Password">
              <PasswordIcon />
            </UserInfoButton>
          </router-link>

          <button @click="handleDeleteAccount">
            <UserInfoButton baseColor="red" buttonTitle="Delete Account">
              <DeleteIcon />
            </UserInfoButton>
          </button>

        </div>
      </div>
    </div>

  </div>
</template>