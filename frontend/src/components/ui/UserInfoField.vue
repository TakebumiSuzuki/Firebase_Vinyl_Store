<script setup>

  defineProps({
    label: {
      type: String,
      required: true
    },
    fieldValue: {
      type: String,
      default: ''
    }
  })

</script>


<template>
  <div class="group relative">

    <div class="absolute inset-0 bg-gradient-to-r from-violet-500/20 to-purple-500/20 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>

    <div class="relative bg-neutral-800/50 rounded-lg p-4 border border-neutral-700/50 hover:border-violet-400/30 transition-all duration-300">

      <label class="block text-sm font-medium text-violet-300 mb-2">{{label}}</label>
      <p class="text-lg font-semibold text-white break-all">{{ fieldValue || '--' }}</p>

    </div>

  </div>
</template>