<script setup>
  import { computed } from 'vue';
  import { useNotificationStore } from '@/stores/notificationStore';
  // <Transition>がVueに組み込まれたコンポーネントであり、<script setup>内で明示的にインポートする必要がない
  // import { Transition } from 'vue';

  import successIcon from '@/assets/icons/Success.svg';      // 成功用
  import errorIcon from '@/assets/icons/Error.svg';      // エラー用 (例: xmark.svgなど)
  import infoIcon from '@/assets/icons/Info.svg';        // 情報用 (例: info-circle.svgなど)
  import closeIcon from '@/assets/icons/Close.svg';      // 閉じるボタン用 (例: xmark.svgを流用も可)

  const notificationStore = useNotificationStore();
  const isVisible = computed(() => notificationStore.isVisible);
  const message = computed(() => notificationStore.message);
  const type = computed(() => notificationStore.type);

  const currentIcon = computed(() => {
    switch (type.value) {
      case 'success':
        return successIcon;
      case 'error':
        return errorIcon;
      case 'info':
        return infoIcon;
      default:
        return null;
    }
  });

  const closeNotification = () => {
    notificationStore.hideNotification();
  };

</script>

<template>
  <Transition name="fade">
    <div
      v-if="isVisible"
      class="fixed top-4 right-6 z-50 flex flex-col items-center min-w-[250px] backdrop-blur-xs bg-black/60 p-4 rounded-lg shadow-lg text-neutral-50/80"
    >
      <component
        v-if="currentIcon"
        :is="currentIcon"
        class="size-12"
        :class="{
          'text-teal-400/80': type==='success',
          'text-pink-400/80': type==='error',
          'text-yellow-400/80': type==='info'
        }"
      />

      <p class="pt-2">
        {{ message }}
      </p>

      <!-- 閉じるボタンのアイコン表示 -->
      <button
        @click="closeNotification"
        class="absolute top-2 right-2 cursor-pointer hover:opacity-70"
      >
        <component :is="closeIcon" class="size-6.5" />
      </button>

    </div>
  </Transition>

</template>

<style scoped>
  /* 通知の表示/非表示時のトランジション */
  .fade-enter-active,
  .fade-leave-active {
      transition: opacity 0.5s ease;
  }
  .fade-enter-from,
  .fade-leave-to {
      opacity: 0;
  }
</style>