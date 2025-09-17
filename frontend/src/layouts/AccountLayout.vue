<script setup>
</script>

<template>

  <div class="h-full bg-linear-120 dark:from-neutral-600 dark:to-neutral-800 bg-neutral-50">
    <div class="bg-linear-90 from-red-400 to-pink-500 text-center  font-medium">
      <RouterLink :to="{name:'admin-users-list'}">Go Admin Page</RouterLink>
    </div>
    <div class="px-4 sm:px-8">
      <div class="py-4 sm:py-10">
        <div class="w-full max-w-[600px] mx-auto shadow-2xl rounded-xl">
          <RouterView/>
        </div>
      </div>
    </div>
  </div>
</template>