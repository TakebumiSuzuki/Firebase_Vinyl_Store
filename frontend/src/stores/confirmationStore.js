import { ref } from 'vue';
import { defineStore } from 'pinia';

// Promiseの解決/拒否関数を格納する変数
// ストアのインスタンスはシングルトンなので、これらの変数は一度に一つのアラートの状態を管理します。
let resolvePromise = null;
let rejectPromise = null;

export const useConfirmationStore = defineStore('confirmation', () => {

    const isVisible = ref(false);

    const message = ref('');
    // buttons例:
    // [{ text: 'はい', value: true, style: 'primary' }, { text: 'いいえ', value: false, style: 'secondary' }]
    const buttons = ref([]);
    const overlayClickToClose = ref(true); // 背景クリックでアラートを閉じるか


    const showConfirmation = (msg, btns, options = {}) => {
        // 既にアラートが表示されている場合、前のPromiseを強制的にrejectする
        if (isVisible.value && rejectPromise) {
            rejectPromise(new Error('Confirmation was dismissed by another confirmation request.'));
        }

        // 新しいPromiseを作成し、解決/拒否関数を保存
        return new Promise((resolve, reject) => {
            resolvePromise = resolve;
            rejectPromise = reject;

            message.value = msg;
            buttons.value = btns;
            overlayClickToClose.value = typeof options.overlayClickToClose === 'boolean' ? options.overlayClickToClose : true;
            isVisible.value = true;
        });
    };


    const _hideConfirmation = (result = undefined, isCanceled = false) => {
        isVisible.value = false;
        message.value = '';
        buttons.value = [];

        // Promiseを解決または拒否
        if (resolvePromise && rejectPromise) {
            if (isCanceled) {
                // キャンセル（overlayClickToClose=trueの背景クリック、または強制的なhideConfirmation）
                rejectPromise(new Error('Confirmation was dismissed.'));
            } else {
                // 正常なボタンクリック
                resolvePromise(result);
            }
        }

        // Promiseの参照をクリア
        resolvePromise = null;
        rejectPromise = null;
    };


    const handleButtonClick = (buttonValue) => {
        _hideConfirmation(buttonValue, false); // 正常な解決
    };

    const handleOverlayClick = () => {
        if (overlayClickToClose.value) {
            _hideConfirmation(undefined, true); // キャンセルとして拒否
        }
    };


    return {
        // State
        isVisible,
        message,
        buttons,
        overlayClickToClose,

        // Actions
        showConfirmation,
        handleButtonClick,
        handleOverlayClick,
        // _hideConfirmation は内部的に使用するため、通常は外部に公開しない
    };
});