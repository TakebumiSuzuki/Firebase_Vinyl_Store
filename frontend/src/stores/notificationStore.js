import { ref } from 'vue';
import { defineStore } from 'pinia';

export const useNotificationStore = defineStore('notification', () => {

  const isVisible = ref(false);

  const message = ref(null);
  const type = ref(null); // 'success', 'error', 'info' など
  const _timeoutId = ref(null); // 通知を自動で消すためのタイマーID
  let pendingNotification = ref(null)

  const showNotification = (msg, msgType = 'info', duration = 3000) => {
    // 既にタイマーが既に設定されている場合はクリア
    if (_timeoutId.value) {
        clearTimeout(_timeoutId.value);
    }

    message.value = msg;
    type.value = msgType;
    isVisible.value = true;

    // 指定時間後に通知を非表示にする
    _timeoutId.value = setTimeout(() => {
        hideNotification(); // 直接関数を呼び出し
    }, duration);
  };

  const hideNotification = () => {
    isVisible.value = false;
    message.value = null;
    type.value = null;
    if (_timeoutId.value) {
        clearTimeout(_timeoutId.value);
        _timeoutId.value = null;
    }
  };


  return {
    isVisible,
    message,
    type,
    showNotification,
    hideNotification,
    pendingNotification,
    // timeoutId は内部的に使うだけなので、通常は公開しない
  };
});