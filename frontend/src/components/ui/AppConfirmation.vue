<script setup>
  // <Transition>がVueに組み込まれたコンポーネントであり、<script setup>内で明示的にインポートする必要がない
  //import { Transition } from 'vue';
  import { useConfirmationStore } from '@/stores/confirmationStore';
  const confirmationStore = useConfirmationStore();

  const getButtonClasses = (style) => {
    switch (style) {
      case 'primary':
          return 'bg-teal-500 text-neutral-50 hover:bg-teal-600';
      case 'danger':
          return 'bg-red-500 text-neutral-50 hover:bg-red-600';
      case 'secondary':
          return 'bg-gray-200 text-gray-800 hover:bg-gray-300';
      case 'cancel':
          return 'bg-transparent text-gray-600 hover:bg-gray-100 border border-gray-300';
      default:
          return 'bg-gray-200 text-gray-800 hover:bg-gray-300';
    }
  };
</script>


<template>
  <Transition name="fade">
    <!-- 暗い背景 -->
    <div v-if="confirmationStore.isVisible"
        class="fixed inset-0 bg-black/60 z-[9999] flex justify-center items-center p-4"
        @click="confirmationStore.handleOverlayClick"
    >
      <!-- アラートのモーダル本体 -->
      <div class="backdrop-blur-xs bg-white/60 rounded-lg shadow-xl p-6 max-w-sm w-full relative"
          @click.stop
      >
        <p class="text-lg text-center text-neutral-700 mb-6 whitespace-pre-wrap">
            {{ confirmationStore.message }}
        </p>

        <div class="flex flex-col md:flex-row justify-center items-center gap-4 md:gap-8 mt-4">
          <button
            v-for="(button, index) in confirmationStore.buttons"
            :key="index"
            @click="confirmationStore.handleButtonClick(button.value)"
            class="px-8 py-2 rounded-md font-medium max-md:w-full transition duration-200 ease-in-out"
            :class="getButtonClasses(button.style)"
        >
            {{ button.text }}
          </button>
        </div>
      </div>
    </div>
  </Transition>
</template>

<style scoped>
  /* フェードアニメーションのためのCSS */
  .fade-enter-active,
  .fade-leave-active {
    transition: opacity 0.3s ease;
  }

  .fade-enter-from,
  .fade-leave-to {
    opacity: 0;
  }
</style>