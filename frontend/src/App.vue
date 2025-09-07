<script setup>
  import TheHeader from '@/components/layout/TheHeader.vue'
  import TheFooter from '@/components/layout/TheFooter.vue'
  import AppConfirmation from '@/components/ui/AppConfirmation.vue'
  import AppNotification from '@/components/ui/AppNotification.vue'
</script>

<template>
  <AppConfirmation />
  <AppNotification />

  <div class="flex flex-col min-h-screen text-neutral-600 dark:text-neutral-50">
    <TheHeader />
    <RouterView class="grow h-[1px]" />
    <TheFooter />
  </div>
</template>

